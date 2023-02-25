# -*- coding: utf-8 -*-
from typing import Dict, List

import pandas as pd
import requests


def read(__nodes_file: str, /) -> List[Dict[str, str]]:
    """
    Read Fabric nodes from Excel file

    Parameters
    ----------
    __nodes_file : str
        Fabric nodes Excel file name. e.g. "Fabric-Nodes.xlsx"

    Returns
    -------
    List[Dict[str, str]]
        List of dictionaries of Fabric nodes
    """
    nodes = pd.read_excel(io=__nodes_file, sheet_name=0, engine="openpyxl")
    df = pd.DataFrame(data=nodes)
    return (
        df.fillna(value="")  # Fill nan cells with empty string
        .drop_duplicates(subset=["Serial Number"])
        .rename(
            columns={
                "Node Type": "node_type",
                "Node Role": "role",
                "POD ID": "pod_id",
                "Serial Number": "serial",
                "Node Name": "name",
                "Node ID": "node_id",
            }
        )
        .to_dict(orient="records")
    )


def register(
    apic: str, headers: Dict[str, str], node: Dict[str, str]
) -> requests.Response:
    """
    Register Fabric node to ACI Fabric

    Parameters
    ----------
    apic : str
        APIC IP Address. e.g. "sandboxapicdc.cisco.com"

    headers : Dict[str, str]
        Headers from APIC login

    node : Dict[str, str]
        Fabric node

    Returns
    -------
    requests.Response
        Response from APIC register node API
    """
    url = f"https://{apic}/api/mo/uni/controller/nodeidentpol.json"
    payload = {
        "fabricNodeIdentP": {
            "attributes": {
                "nodeId": str(node.get("node_id")),
                "nodeType": node.get("node_type"),
                "role": node.get("role"),
                "name": node.get("name").strip(),
                "serial": node.get("serial").strip(),
            }
        },
        "fabricNodePEp": {
            "attributes": {
                "tDn": f"topology/pod-{node.get('pod_id', 1)}/{node.get('name')}",
            }
        },
    }
    r = requests.post(url=url, headers=headers, json=payload, verify=False)
    r.raise_for_status()
    return r
