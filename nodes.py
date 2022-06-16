from typing import Dict, List

import pandas as pd
import requests


def read(__nodes_file: str, /) -> List[Dict[str, str]]:
    nodes = pd.read_excel(
        io=__nodes_file, sheet_name=0, usecols="A:F", engine="openpyxl"
    )
    df = pd.DataFrame(data=nodes)
    return (
        df.fillna(value="")  # Fill empty cells with empty string
        .drop_duplicates(subset=[df.columns[3]])  # Drop duplicates by serial number
        .rename(
            columns={
                df.columns[0]: "type",  # Node Type
                df.columns[1]: "role",  # Node Role
                df.columns[2]: "pod_id",  # Pod ID
                df.columns[3]: "serial",  # Node Serial Number
                df.columns[4]: "name",  # Node Name
                df.columns[5]: "node_id",  # Node ID
            }
        )
        .to_dict(orient="records")
    )


def register(apic: str, headers: Dict[str, str], node: Dict[str, str]) -> str:
    payload = f"""\
    <polUni>
        <ctrlrInst>
            <fabricNodeIdentPol>
                <fabricNodeIdentP nodeType={node["type"].lower().strip()} role={node["role"].lower().strip()} podId={node["pod_id"] or "1"} serial={node["serial"].strip()} name={node["name"].strip()} nodeId={node["node_id"]} />
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
