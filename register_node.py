from typing import Dict
from xml.etree import ElementTree as ET

import requests
from requests.exceptions import HTTPError


def register_node(apic: str, headers: Dict[str, str], node: Dict[str, str]) -> str:
    payload = f"""\
    <polUni>
        <ctrlrInst>
            <fabricNodeIdentPol>
                <fabricNodeIdentP nodeType={node["type"].lower().strip()} role={node["role"].lower().strip()} podId={node["pod_id"]} serial={node["sn"].strip()} name={node["name"].strip()} nodeId={node["node_id"]} />
            </fabricNodeIdentPol>
        </ctrlrInst>
    </polUni>
    """
    try:
        r = requests.post(
            url=f"https://{apic}/api/policymgr/mo/uni.xml",
            headers=headers,
            data=payload,
            timeout=120.0,
            verify=False,
        )
        r.raise_for_status()
    except HTTPError as e:
        return f"[red]{ET.fromstring(text=e.response.text).find(path='.//error').get(key='text')}"
    else:
        if r.ok and r.status_code in [200, 201]:
            return f"[blue]Registered node {node['name']} (ID: {node['node_id']}) with serial number {node['sn']} to APIC"
