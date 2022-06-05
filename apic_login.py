import requests
from requests import Response
from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout


def apic_login(apic: str, usr: str, pwd: str) -> Response:
    url = f"https://{apic}/api/aaaLogin.json?gui-token-request=yes"
    payload = {"aaaUser": {"attributes": {"name": usr, "pwd": pwd}}}
    try:
        r = requests.post(url=url, json=payload, timeout=8.0, verify=False)
        r.raise_for_status()
    except (InvalidURL, HTTPError, ConnectionError, Timeout) as e:
        return f"[red]{e}"
    else:
        return r
