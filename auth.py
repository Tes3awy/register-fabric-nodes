# -*- coding: utf-8 -*-
import requests


def login(apic: str, usr: str, pwd: str) -> requests.Response:
    """
    APIC login

    Parameters
    ----------
    apic : str
        APIC IP Address. e.g. "sandboxapicdc.cisco.com"
    usr : str
        APIC username. e.g. "admin"
    pwd : str
        APIC password. e.g. "!v3G@!4@Y"

    Returns
    -------
    requests.Response
        APIC login response
    """
    url = f"https://{apic}/api/aaaLogin.json"
    params = {"gui-token-request": "yes"}
    payload = {"aaaUser": {"attributes": {"name": usr, "pwd": pwd}}}
    r = requests.post(url=url, params=params, json=payload, verify=False)
    r.raise_for_status()
    return r


def logout(apic: str, headers: dict, usr: str) -> requests.Response:
    """
    APIC logout

    Parameters
    ----------
    apic : str
        APIC IP Address. e.g. "sandboxapicdc.cisco.com"
    headers : dict
        APIC login headers
    usr : str
        APIC username. e.g. "admin"

    Returns
    -------
    requests.Response
        APIC logout response
    """
    url = f"https://{apic}/api/aaaLogout.json"
    payload = {"aaaUser": {"attributes": {"name": usr}}}
    r = requests.post(url=url, headers=headers, json=payload, verify=False)
    r.close()
    r.raise_for_status()
    return r
