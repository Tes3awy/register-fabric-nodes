import requests
from requests import Response


def apic_logout(apic: str, headers: dict, usr: str) -> Response:
    r = requests.post(
        url=f"https://{apic}/api/aaaLogout.json",
        headers=headers,
        json={"aaaUser": {"attributes": {"name": usr}}},
        verify=False,
    )
    r.raise_for_status()
    return r
