# -*- coding: utf-8 -*-
## Imports
import json
import time
import warnings
from getpass import getpass

from cobra.mit import access, request, session  # for accessing the APIC object
from cobra.mit.request import CommitError, RestError
from cobra.model import ctrlr, fabric, pol  # for creating new fv objects
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from rich import print

import nodes


def register_fabric_nodes():  # sourcery skip: extract-method
    # Suppress HTTPS warning
    warnings.filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")

    ## Inputs
    nodes_file = input("Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
    apic = input("APIC IP Address: ").strip() or "sandboxapicdc.cisco.com"
    usr = input("Username: ").strip() or "admin"
    pwd = getpass(prompt="Password: ").strip() or "!v3G@!4@Y"

    ## Processing
    apic_session = session.LoginSession(
        controllerUrl=f"https://{apic}",
        user=usr,
        password=pwd,
        secure=False,
        requestFormat="json",
    )
    moDir = access.MoDirectory(session=apic_session)

    try:
        print(f"\nAccessing {apic_session.controllerUrl}...", end="\r")
        moDir.login()
    except (HTTPError, ConnectionError, InvalidURL) as e:
        raise SystemExit(e) from e
    else:
        print(f"[green]Successfully accessed APIC as {apic_session.user}")

        # select the top level object
        polUni = pol.Uni(parentMoOrDn="")
        ctrlrInst = ctrlr.Inst(parentMoOrDn=polUni)

        fabric_nodes = nodes.read(nodes_file)  # read ACI Nodes from Excel file

        start_time = time.perf_counter()
        # register fabric nodes
        for node in fabric_nodes:
            fabricNodeIdentPol = fabric.NodeIdentPol(parentMoOrDn=ctrlrInst)
            fabricNodeIdentP = fabric.NodeIdentP(
                parentMoOrDn=fabricNodeIdentPol,
                name=node.get("name").strip(),
                serial=node.get("serial").strip(),
                podId=node.get("pod_id") or "1",
                nodeId=node.get("node_id"),
                nodeType=node.get("type").lower().strip(),
                role=node.get("role").lower().strip(),
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
                    f"[red]{json.loads(e.reason).get('imdata')[0].get('error').get('attributes').get('text')}"
                )
            else:
                if response.status_code in (200, 201):
                    print(
                        f"[magenta]Registered {fabricNodeIdentP.name} with ID {fabricNodeIdentP.nodeId} and serial number {fabricNodeIdentP.serial}"
                    )
        print(f"EET: {time.perf_counter() - start_time:.2f} second")

        if moDir.session.cookie:
            moDir.logout()  # logout
            print("[yellow]Logged out")


if __name__ == "__main__":
    register_fabric_nodes()
