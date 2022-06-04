from typing import Dict, List

import pandas as pd


def read_nodes(nodes_file: str, /) -> List[Dict[str, str]]:
    nodes = pd.read_excel(io=nodes_file, sheet_name=0, usecols="A:F", engine="openpyxl")
    df = pd.DataFrame(data=nodes)
    return (
        df.fillna(value="")
        .drop_duplicates(subset=[df.columns[3]])
        .rename(
            columns={
                df.columns[0]: "type",  # Node Type
                df.columns[1]: "role",  # Node Role
                df.columns[2]: "pod_id",  # Pod ID
                df.columns[3]: "sn",  # Node Serial Number
                df.columns[4]: "name",  # Node Name
                df.columns[5]: "node_id",  # Node ID
            }
        )
        .to_dict(orient="records")
    )