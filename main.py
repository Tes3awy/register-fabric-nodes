# -*- coding: utf-8 -*-
from getpass import getpass
from time import perf_counter
from warnings import filterwarnings

from requests.exceptions import HTTPError, InvalidURL, Timeout
from rich import print

from apic_login import apic_login
from apic_logout import apic_logout
from read_nodes import read_nodes
from register_node import register_node

filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")


def main():
    # Inputs
    nodes_file = input("Fabric Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
    apic = input("APIC IP Address: ").strip() or "sandboxapicdc.cisco.com"
    usr = input("Username: ").strip() or "admin"
    pwd = getpass(prompt="Password: ").strip() or "!v3G@!4@Y"

    ## Processing
    # Login to APIC and get tokens
    print(f"Logging into {apic}...", end="\r")
    try:
        res = apic_login(apic=apic, usr=usr, pwd=pwd)
    except (InvalidURL, HTTPError, ConnectionError, Timeout) as e:
        raise SystemExit(print(f"[red]{e}")) from e
    else:
        print(f"[green]Logged into {apic} successfully")

        headers = {
            "cookie": res.headers.get("set-cookie"),
            "apic-challenge": res.json()
            .get("imdata")[0]
            .get("aaaLogin")
            .get("attributes")
            .get("urlToken"),
        }

        try:
            # Read nodes from Excel file
            nodes = read_nodes(nodes_file)
        except FileNotFoundError as e:
            raise SystemExit(
                print(f"[red]{nodes_file} is not found! Check typos in filename")
            ) from e
        else:
            start_time = perf_counter()

            # Register nodes to ACI Fabric
            for n, node in enumerate(iterable=nodes, start=1):
                print(f"{n}/{len(nodes)} Registering node {node['name']}...", end="\r")
                reg = register_node(apic=apic, headers=headers, node=node)
                print(reg)

            # Output
            print(f"[green]Registered {n}/{len(nodes)} APIC nodes", end="\n\n")
            print(f"EET: {perf_counter() - start_time:.2f} seconds")
        finally:
            if res is not None:
                # Logout from APIC
                status = apic_logout(apic=apic, headers=headers, usr=usr)
                if "deleted" in status.headers.get("set-cookie"):
                    print("[yellow]Logged out")


if __name__ == "__main__":
    main()
