import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout


def apic_logout(apic: str, headers: dict, usr: str) -> str:
    try:
        r = requests.post(
            url=f"https://{apic}/api/aaaLogout.json",
            headers=headers,
            json={"aaaUser": {"attributes": {"name": usr}}},
            verify=False,
        )
        r.raise_for_status()
    except (HTTPError, ConnectionError, Timeout) as e:
        return f"[red]{e}"
    else:
        return "[yellow]Logged out"
