# ship_discovery_agent
Discovery agent  for SONiC spine leaf network

## project overview
The goal of this project is to build an agent that can run commands remotely on SONiC network devices through the SSH protocol, Retrieve multiple tables describing the state of the network (ARP table, Routing table, CAM table, Acess lists ...etc.), and parse the collected tables into a `JSON` format.

![overview_diagram](docs/overview.png)
