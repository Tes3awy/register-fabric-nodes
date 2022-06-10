# Register Fabric Inventory Nodes to ACI Fabric

> When you run the application, the system determines if the node exists and, if not, adds it. If the node exists, the system registers it.

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Overview](#overview)
3. [Fabric Inventory Node Discovery Statuses](#fabric-inventory-node-discovery-statuses)
4. [Register Fabric Inventory Nodes](#register-fabric-inventory-nodes)
5. [Bonus](#bonus)

## Directory Structure

```
│   main.py
│   apic_login.py
│   read_nodes.py
│   register_node.py
│   apic_logout.py
│   apic_cobra_register.py
│   Fabric-Nodes.xlsx
│   README.md
└───
```

## Overview

After a switch is registered with the APIC, the switch is part of the APIC-managed fabric inventory. With the
ACI fabric, the APIC is the single point of provisioning, management, and monitoring for switches in the infrastructure.

Switches in the `Nodes Pending Registration` tab table can have the following conditions:
- A newly discovered but unregistered node has a node ID of 0 and has no assigned IP address.
- A manually entered (in APIC) but unregistered switch has an original status of `Undiscovered` until it is physically connected to the network. Once connected, the status changes to `Discovered`.

**Note:** After the node ID is assigned, it cannot be updated.

## Fabric Inventory Node Discovery Statuses

| Status        | Description                                      	    |
|--------------	|------------------------------------------------------ |
| Unknown      	| Node is discovered but no Node ID policy configured. 	|
| Undiscovered 	| Node ID configured but not yet discovered.        	|
| Discovering  	| Node is discovered but IP not yet assigned.          	|
| Unsupported  	| Node is not a supported model.                    	|
| Disabled     	| Node has been decommissioned.                     	|
| Inactive     	| No IP connectivity.                               	|
| Active       	| Node is active.                                   	|

## Register Fabric Inventory Nodes

### Option A

1. Download the repo from GitHub using `Code` button.
2. Unzip the repo.
3. Create a Python virtual environment.
3. Install requirements.

```powershell
register-fabric-nodes-main> python -m venv .venv
register-fabric-nodes-main> python -m pip install --upgrade pip setuptools
register-fabric-nodes-main> python -m pip install -r requirements.txt
```

### Option B

1. Clone the repo from GitHub.
2. Create a Python virtual environment.
3. Install requirements.

```bash
$ git clone https://github.com/Tes3awy/register-fabric-nodes.git
$ cd register-fabric-nodes
$ python -m venv .venv
$ python -m pip install --upgrade pip setuptools
$ python -m pip install -r requirements.txt
```

Add your ACI fabric inventory nodes to the `Fabric-Nodes.xlsx` Excel file.

> The Excel file is already in the repo and is populated with two leafs and two spines from [Getting Started with Cisco ACI 5.2 v1](https://dcloud2-lon.cisco.com/content/demo/505213?returnPathTitleKey=content-view) from Cisco dCloud.

In `Node Type` column (Column A), you can select only one of the following four node types:
1. `unspecified`
2. `tier-2-leaf`
3. `remote-wan-leaf`
4. `virtual`

> If you don't know what to select in the `Node Type` column, select `unspecified`.

In `Node Role` column (Column B), you can select only one of the following three node roles:
1. `spine`
2. `leaf`
3. `unspecified`

After filling all columns in `Fabric-Nodes.xlsx` file, double check your entries.

> After a successful run, the node is removed from the `Nodes Pending Registration` tab table to `Registered Nodes` tab table and you cannot by any means change neither the node type nor node id.

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

---

## Bonus

If you have Cobra SDK installed _(`acicobra` and `acimodel` wheel files installed)_, you can run the application using `apic_cobra_register.py`. It's much faster than the regular application (Around 1.8x faster).
