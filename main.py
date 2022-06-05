from getpass import getpass
from time import perf_counter
from warnings import filterwarnings

from rich import print

from apic_login import apic_login
from apic_logout import apic_logout
from read_nodes import read_nodes
from register_node import register_node

filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")


def main():
    # Inputs
    nodes_file = input("Fabric Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
    apic = input("APIC IP Address: ").strip() or "198.18.133.200"
    usr = input("Username: ").strip() or "admin"
    pwd = getpass(prompt="Password: ") or "C1sco12345"

    ## Processing
    # Login to APIC and get tokens
    print("Logging into APIC...", end="\r")
    res = apic_login(apic=apic, usr=usr, pwd=pwd)
    if not isinstance(res, str):
        print("[green]Logged into APIC successfully")

        headers = {
            "cookie": res.headers.get("set-cookie"),
            "apic-challenge": res.json()
            .get("imdata")[0]
            .get("aaaLogin")
            .get("attributes")
            .get("urlToken"),
        }

        # Read nodes from Excel file
        nodes = read_nodes(nodes_file)

        start_time = perf_counter()

        # Register all nodes to APIC
        for n, node in enumerate(iterable=nodes, start=1):
            print(f"{n}/{len(nodes)} Registering node {node['name']}...", end="\r")
            reg = register_node(apic=apic, headers=headers, node=node)
            print(reg)

        # Output
        print(f"[green]Registered {n}/{len(nodes)} APIC nodes", end="\n\n")
        print(f"EET: {perf_counter() - start_time:.2f} seconds")

        # Logout of APIC
        status = apic_logout(apic=apic, headers=headers, usr=usr)
        print(status)


if __name__ == "__main__":
    main()
