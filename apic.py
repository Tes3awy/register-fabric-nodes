import requests


def login(apic: str, usr: str, pwd: str) -> requests.Response:
    url = f"https://{apic}/api/aaaLogin.json?gui-token-request=yes"
    payload = {"aaaUser": {"attributes": {"name": usr, "pwd": pwd}}}
    r = requests.post(url=url, json=payload, timeout=10.0, verify=False)
    r.raise_for_status()
    return r


def logout(apic: str, headers: dict, usr: str) -> requests.Response:
    r = requests.post(
        url=f"https://{apic}/api/aaaLogout.json",
        headers=headers,
        json={"aaaUser": {"attributes": {"name": usr}}},
        verify=False,
    )
    r.raise_for_status()
    return r
