# Ship Discovery Agent
Discovery agent  for SONiC spine leaf network

## Project Overview
[ANTD](https://www.nist.gov/itl/antd) is building the next network management system, [the multiverse network management system](https://github.com/multiverse-nms) which will support multiple networking paradigmes, essentially IP and NDN networks.
The main conponent is the multiverse controller that defines the models and standards to describe and managed the network. The controller exposes APIs for Agents to communicate with it.
the Agents role is to report about the state of the network or run commands issued by the controller to change a network configuration.

![full_project_overview](docs/full_project_overview.png)

## Project Details
The goal of this project is to build an agent that can run commands remotely on SONiC network devices through the SSH protocol, Retrieve multiple tables describing the state of the network (ARP table, Routing table, CAM table, Acess lists ...etc.), and parse the collected tables into a `JSON` format.

![overview_diagram](docs/overview.png)

### Requirements

⋅⋅* git
⋅⋅* docker (>=19.03)

### Setting up the Environment

1. Create an account with [https://air.nvidia.com/](https://air.nvidia.com/)
2. Click on `Build Simulation` and choose `SONiC demo`
3. Wait for the nodes to become available

Once the SONiC demo network is created, it comes with a default configuration.
However, we want to load our own configuration. To achieve that follow these steps.

```
	git clone https://gitlab.com/hani.merzouki/sonic-demo
	cd sonic-demo/automation
	ansible-playbook -i inventory/pod1/hosts playbooks/restore_sonic.yml
	ansible-playbook -i inventory/pod1/hosts playbooks/restore_files.yml
```
Note: Running the ansible-playbooks may take a while.

### Getting and Running the Agent

1. Clone the repo
```
	git clone https://github.com/MheniMerz/ship_discovery_agent
	cd ship_discovery_agent/
```
2. Build the docker image
```
	docker build -t agent .
```
3. Run the docker container
```
	docker run -t -i --network host agent
```
