import requests
from requests import Response


def apic_login(apic: str, usr: str, pwd: str) -> Response:
    url = f"https://{apic}/api/aaaLogin.json?gui-token-request=yes"
    payload = {"aaaUser": {"attributes": {"name": usr, "pwd": pwd}}}
    r = requests.post(url=url, json=payload, timeout=10.0, verify=False)
    r.raise_for_status()
    return r
