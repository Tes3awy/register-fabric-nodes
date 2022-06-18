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
                "Node Type": "type",
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
    payload = f"""\
    <polUni>
        <ctrlrInst>
            <fabricNodeIdentPol>
                <fabricNodeIdentP nodeType="{node.get("type", "unspecified").lower().strip()}" role="{node.get("role", "unspecified").lower().strip()}" podId="{node.get("pod_id", 1) or 1}" serial="{node.get("serial").strip()}" name="{node.get("name").strip()}" nodeId="{node.get("node_id")}" />
            </fabricNodeIdentPol>
        </ctrlrInst>
    </polUni>
    """
    r = requests.post(
        url=f"https://{apic}/api/policymgr/mo/uni.xml",
        headers=headers,
        data=payload,
        timeout=120.0,
        verify=False,
    )
    r.raise_for_status()
    return r
