import os
from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()

#load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
client.load_system_host_keys()

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

# read config file and foreach host create connection

#run commands
# show arp
# show ip route
# show acl table, show acl rules
