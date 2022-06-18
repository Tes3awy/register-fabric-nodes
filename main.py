# -*- coding: utf-8 -*-
from getpass import getpass
from warnings import filterwarnings
from xml.etree import ElementTree as ET

from requests.exceptions import HTTPError, InvalidURL, Timeout
from rich import print

import apic
import nodes

filterwarnings(action="ignore", message=r"Unverified\sHTTPS\srequest\s.*")


def main():
    # Inputs
    nodes_file = input("Fabric Nodes Excel file: ").strip() or "Fabric-Nodes.xlsx"
    apic_ip = input("APIC IP Address: ").strip() or "sandboxapicdc.cisco.com"
    usr = input("Username: ").strip() or "admin"
    pwd = getpass(prompt="Password: ").strip() or "!v3G@!4@Y"

    ## Processing
    # Login to APIC to create a session and get tokens
    print(f"Logging into {apic_ip}...", end="\r")
    try:
        res = apic.login(apic=apic_ip, usr=usr, pwd=pwd)
    except (InvalidURL, HTTPError, ConnectionError, Timeout) as e:
        raise SystemExit(print(f"[red]{e}")) from e
    else:
        print(f"[green]Logged into {apic_ip} successfully")

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
            fab_nodes = nodes.read(nodes_file)
        except FileNotFoundError as e:
            raise SystemExit(
                print(f"[red]{nodes_file} is not found! Check typos in filename")
            ) from e
        else:
            # Register nodes to ACI Fabric
            i, eet = 0, 0.0
            for node in fab_nodes:
                print(f"Registering node {node['name']}...", end="\r")
                try:
                    reg_res = nodes.register(apic=apic_ip, headers=headers, node=node)
                    eet += reg_res.elapsed.total_seconds()
                except HTTPError as e:
                    print(
                        f"[red]{ET.fromstring(text=e.response.text).find(path='.//error').get(key='text')}"
                    )
                else:
                    i += 1
                    print(
                        f"[blue]Registered {node['name']} (ID: {node['node_id']}) with serial number {node['serial']} to APIC"
                    )

            # Output
            print(f"[green]Registered {i}/{len(fab_nodes)} APIC nodes", end="\n\n")
            print(f"EET: {eet:.2f} seconds")
        finally:
            if res is not None:
                # Logout from APIC
                out_res = apic.logout(apic=apic_ip, headers=headers, usr=usr)
                if "deleted" in out_res.headers.get("set-cookie") and out_res.ok:
                    print(f"[magenta]Logged out from {apic_ip}")


if __name__ == "__main__":
    main()
