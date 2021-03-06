[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Tes3awy/register-fabric-nodes)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)
![LICENSE](https://img.shields.io/github/license/Tes3awy/register-fabric-nodes?color=purple&style=flat-square&label=LICENSE)
![Commit Activity](https://img.shields.io/github/commit-activity/m/Tes3awy/register-fabric-nodes/main?logo=github&style=flat-square)

# Register Inventory Nodes to ACI Fabric

> When you run the application, the system determines if the node exists and, if not, adds it. If the node exists, the system registers it.

> The application uses the APIC-Challenge token for a stronger API session security. To learn more about the challenge token, see [Requiring a Challenge Token for an API Session](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/2-x/rest_cfg/2_1_x/b_Cisco_APIC_REST_API_Configuration_Guide/b_Cisco_APIC_REST_API_Configuration_Guide_chapter_01.html#ariaid-title33).

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Overview](#overview)
3. [Fabric Inventory Node Discovery Statuses](#fabric-inventory-node-discovery-statuses)
4. [Installation](#installation)
5. [Register Fabric Inventory Nodes](#register-fabric-inventory-nodes)
6. [Bonus](#bonus)

## Directory Structure

The directory contains the following files:

```
│   main.py
│   apic.py
│   nodes.py
│   apic_cobra.py
│   Fabric-Nodes.xlsx
|   requirements.txt
│   README.md
│   LICENSE
│   .gitignore
├───assets
│       apic_nodes.jpg
│       registered_nodes.jpg
└───
```

1. `apic.py` module contains the APIC functions to connect and have access to the APIC Controller.
2. `nodes.py` module contains the functions to read nodes to be registered and register those nodes.
3. `main.py` module contains the main function to run the application.
4. `Fabric-Nodes.xlsx` is a spreadsheet with the nodes to be registered _(Columns A and B are using [data validation](https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-eff3ce5f7249) Excel feature to restrict the type of data and to show an error alert if values other than those in the drop-down list is entered)_.
5. For `apic_cobra.py` module, check [Bonus](#bonus) section.

## Overview

After a switch is registered with the APIC, the switch is part of the APIC-managed fabric inventory. With the
ACI fabric, the APIC is the single point of provisioning, management, and monitoring for switches in the infrastructure.

Switches in the `Nodes Pending Registration` tab table can have the following conditions:
- A newly discovered but unregistered node has a node ID of 0 and has no assigned IP address.
- A manually entered (in APIC) but unregistered switch has an original status of `Undiscovered` until it is physically connected to the network. Once connected, the status changes to `Discovered`.

![APIC Nodes](assets/apic_nodes.jpg)

**Note:** After the node ID is assigned, it cannot be updated.

## Fabric Inventory Node Discovery Statuses

| Status        | Description                                      	    |
| -------------	| ----------------------------------------------------- |
| Unknown      	| Node is discovered but no Node ID policy configured. 	|
| Undiscovered 	| Node ID configured but not yet discovered.        	|
| Discovering  	| Node is discovered but IP not yet assigned.          	|
| Unsupported  	| Node is not a supported model.                    	|
| Disabled     	| Node has been decommissioned.                     	|
| Inactive     	| No IP connectivity.                               	|
| Active       	| Node is active.                                   	|

## Installation

### Option A

1. Download the repo from GitHub using `Code` button.
2. Unzip the repo.
3. Create a Python virtual environment and activate it.
3. Install requirements.

```powershell
register-fabric-nodes-main> python -m venv .venv --upgrade-deps
register-fabric-nodes-main> .\.venv\Scripts\Activate.ps1
register-fabric-nodes-main> python -m pip install -r requirements.txt
```

### Option B

1. Clone the repo from GitHub.
2. Create a Python virtual environment and activate it.
3. Install requirements.

```bash
$ git clone https://github.com/Tes3awy/register-fabric-nodes.git
$ cd register-fabric-nodes
$ python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ python -m pip install -r requirements.txt
```

## Register Fabric Inventory Nodes

Add your ACI fabric inventory nodes to the `Fabric-Nodes.xlsx` Excel file.

> The Excel file is already in the repo and is populated with two leafs and two spines from [Getting Started with Cisco ACI 5.2 v1](https://dcloud2-lon.cisco.com/content/demo/505213?returnPathTitleKey=content-view) from Cisco dCloud.

> **For non Cisco partners, you can use the application with the [ACI Simulator AlwaysOn - V5](https://devnetsandbox.cisco.com/RM/Diagram/Index/18a514e8-21d4-4c29-96b2-e3c16b1ee62e?diagramType=Topology) from Cisco DevNet Sandbox.**

In `Node Type` column (Column A), you can select only one of the following _four_ valid node types:
1. `unspecified`
2. `tier-2-leaf`
3. `remote-wan-leaf`
4. `virtual`

> If you don't know what to select in the `Node Type` column, select `unspecified`.

In `Node Role` column (Column B), you can select only one of the following _three_ valid node roles:
1. `spine`
2. `leaf`
3. `unspecified`

After filling all columns in `Fabric-Nodes.xlsx` file, double check your entries.

![Registered Nodes](assets/registered_nodes.jpg)

**Note:** After a successful run, the node is removed from the `Nodes Pending Registration` tab table to `Registered Nodes` tab table and you cannot by any means edit neither the node type nor node id.

Finally, run the application.

**Windows**

```powershell
> py main.py
# or
> py -m main
```

**Unix or macOS**

```bash
$ python3 main.py
# or
$ python3 -m main
```

You will be prompted to enter Input Excel file, APIC URL, username, and password.

Example:

```bash
Fabric Nodes Excel file: Fabric-Nodes.xlsx
APIC IP Address: sandboxapicdc.cisco.com
Username: admin
Password: 
```

---

## Bonus

If you have Cobra SDK installed _(`acicobra` and `acimodel` wheel files installed)_, you can run the application using `apic_cobra.py`. It's much faster than the regular application (Around 1.8x faster).

```bash
$ python apic_cobra.py
# or
$ python -m apic_cobra
```
