# -*- coding: utf-8 -*-
## Imports
import json
import time
import warnings
from getpass import getpass

from cobra.mit import access, request, session  # for accessing the APIC
from cobra.mit.request import CommitError, RestError
from cobra.model import ctrlr, fabric, pol  # for creating new fv objects
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from rich import print

import nodes


def register_fabric_nodes():
    # Suppress HTTPS warning
    warnings.filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")

    ## Inputs
    nodes_file = input("Fabric Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
    apic = input("APIC IP Address: ").strip() or "sandboxapicdc.cisco.com"
    username = input("Username: ").strip() or "admin"
    password = getpass(prompt="Password: ").strip() or "!v3G@!4@Y"

    ## Processing
    apic_session = session.LoginSession(
        controllerUrl=f"https://{apic}",
        user=username,
        password=password,
        secure=False,
        timeout=10,  # optional (default 90 seconds)
        requestFormat="json",  # optional but recommended (default xml)
    )
    moDir = access.MoDirectory(session=apic_session)

    try:
        print("\nLogging in into APIC...", end="\r")
        moDir.login()
    except (HTTPError, ConnectionError, InvalidURL) as e:
        raise SystemExit(print(f"[red]{e}")) from e
    else:
        print(f"[green]Logged into APIC as {apic_session.user}")

        # select the top level object
        polUni = pol.Uni(parentMoOrDn="")

        fabric_nodes = nodes.read(nodes_file)  # read ACI Nodes from Excel file

        start_time = time.perf_counter()
        # register fabric nodes
        for node in fabric_nodes:
            ctrlrInst = ctrlr.Inst(parentMoOrDn=polUni)
            fabricNodeIdentPol = fabric.NodeIdentPol(parentMoOrDn=ctrlrInst)
            fabricNodeIdentP = fabric.NodeIdentP(
                parentMoOrDn=fabricNodeIdentPol,
                name=node["name"].strip(),
                serial=node["serial"].strip(),
                podId=node["pod_id"] or "1",
                nodeId=node["node_id"],
                nodeType=node["type"].lower().strip(),
                role=node["role"].lower().strip(),
            )

            ## Output

            # Queuing the new configuration
            cfg_request = request.ConfigRequest()
            try:
                cfg_request.addMo(mo=polUni)  # offline validation
                # Equavilant to POST request
                # Commiting (Submitting) new configuration
                response = moDir.commit(configObject=cfg_request)
            except (CommitError, RestError) as e:
                print(
                    f"[red]{json.loads(e.reason)['imdata'][0]['error']['attributes']['text']}"
                )
            else:
                if response.status_code in (200, 201) and response.ok:
                    print(
                        f"[magenta]Registered {fabricNodeIdentP.name} (ID {fabricNodeIdentP.nodeId}) with serial number {fabricNodeIdentP.serial} to APIC"
                    )
        print(f"EET: {time.perf_counter() - start_time:.2f} second")
    finally:
        # check if logged in already to logout
        if moDir.session.cookie:
            moDir.logout()  # logout
            print("[yellow]Logged out")


if __name__ == "__main__":
    register_fabric_nodes()
