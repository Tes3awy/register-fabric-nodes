## Imports
import time
import warnings

from cobra.mit import access, request, session  # for accessing the APIC
from cobra.mit.request import CommitError, RestError
from cobra.model import ctrlr, fabric, pol  # for creating new fv objects
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from rich import print

from read_nodes import read_nodes

warnings.filterwarnings("ignore")  # Suppress all warnings

## Inputs
nodes_file = input("Fabric Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
apic = input("APIC IP Address: ").strip()
username = input("Username: ").strip()
password = input("Password: ").strip()

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
    # session timeout
    print(
        f"[cyan]Session timeouts in {apic_session.refreshTimeoutSeconds/60} minutes",
        end="\n\n",
    )

    # select the top level object
    polUni = pol.Uni(parentMoOrDn="")

    nodes = read_nodes(nodes_file)  # read ACI Nodes from Excel file

    start_time = time.perf_counter()
    # register nodes
    for node in nodes:
        ctrlrInst = ctrlr.Inst(parentMoOrDn=polUni)
        fabricNodeIdentPol = fabric.NodeIdentPol(parentMoOrDn=ctrlrInst)
        fabricNodeIdentP = fabric.NodeIdentP(
            parentMoOrDn=fabricNodeIdentPol,
            nodeType=node["node_type"].lower().strip(),
            podId=node["pod_id"],
            serial=node["node_sn"].strip(),
            name=node["node_name"].strip(),
            nodeId=node["node_id"],
            role=node["node_role"].lower().strip(),
        )

        ## Output

        # Queuing the new configuration
        cfg_request = request.ConfigRequest()
        try:
            # add the new discovery to the configuration request
            cfg_request.addMo(mo=polUni)  # offline validation
            response = moDir.commit(configObject=cfg_request)
        except (CommitError, RestError) as e:
            raise SystemExit(print(f"[red]{e}")) from e
        else:
            # Equavilant to POST request
            # Commiting (Submitting) new configuration
            # check if status code is ok (200) and returns boolean
            if response.ok:
                print(
                    f"[green]Registered {fabricNodeIdentP.name} with serial {fabricNodeIdentP.serial} ands ID {node['node_id']} to APIC"
                )
            else:
                print(
                    f"[red]Failed to register APIC nodes, HTTP Status Code: {response.status_code}. Error: {response.json()}"
                )
    print(f"EET: {time.perf_counter() - start_time:.2f} second")
finally:
    # check if logged in already to logout
    if moDir.session.cookie:
        moDir.logout()  # logout
        print("[yellow]Logged out")
