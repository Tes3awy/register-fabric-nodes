# -*- coding: utf-8 -*-
from getpass import getpass
from warnings import filterwarnings

from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
from rich import print

import auth
import nodes

filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")


def get_input(prompt: str, default: str = None):
    """Helper function to get user input with an optional default value"""
    value = input(prompt).strip()
    return default if value == "" else value


def main():
    # Inputs
    nodes_file = get_input("Nodes Excel file: ", default="Fabric-Nodes.xlsx")
    apic_ip = get_input("APIC IP Address: ", default="sandboxapicdc.cisco.com")
    usr = get_input("Username: ", default="admin")
    pwd = getpass(prompt="Password: ") or "!v3G@!4@Y"

    ## Processing
    # Accessing APIC
    print(f"\nAccessing {apic_ip}...", end="\r")
    try:
        r = auth.login(apic=apic_ip, usr=usr, pwd=pwd)
    except (InvalidURL, HTTPError, ConnectionError, Timeout) as e:
        raise SystemExit(e) from e
    else:
        print(f"[green]Accessed {apic_ip} successfully")

        headers = {
            "cookie": r.headers.get("set-cookie"),
            "apic-challenge": r.json()
            .get("imdata")[0]
            .get("aaaLogin")
            .get("attributes")
            .get("urlToken"),
        }

        try:
            # Read nodes from Excel file
            fab_nodes = nodes.read(nodes_file)
        except FileNotFoundError as e:
            raise SystemExit(f"{nodes_file} is not found! Check typos") from e
        else:
            # Register nodes to ACI Fabric
            i, eet = 0, 0.0
            for node in fab_nodes:
                print(f"Registering {node.get('name')}...", end="\r")
                try:
                    reg = nodes.register(apic=apic_ip, headers=headers, node=node)
                    eet += reg.elapsed.total_seconds()
                except HTTPError as e:
                    print(
                        f"[red]{node.get('name')}: {e.response.json().get('imdata')[0].get('error').get('attributes').get('text')}"
                    )
                else:
                    i += 1
                    print(
                        f"[green]Registered {node.get('name')} with ID {node.get('node_id')} and S/N {node.get('serial')}"
                    )

            # Output
            print(
                f"[blue]Registered {i}/{len(fab_nodes)} nodes in {eet:.2f} seconds",
                end="\n\n",
            )

        out_res = auth.logout(apic=apic_ip, headers=headers, usr=usr)
        if out_res.ok and "deleted" in out_res.headers.get("set-cookie"):
            print(f"[magenta]Closed {apic_ip} session")


if __name__ == "__main__":
    main()
