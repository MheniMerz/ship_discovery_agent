import concurrent
import os
import json
from concurrent.futures import ThreadPoolExecutor
from paramiko import SSHClient, AutoAddPolicy
from config.config import Config
from query.query import Query
from parser.parser import Parser

cfg = Config()
client = SSHClient()
parser = Parser()
query_dictionary = {}

# list of commands that will be run for each node on network
commandList = ['show arp', 'show ip route', 'show acl table', 'show acl rule', 'show lldp table', 'show vlan config',
               'vtysh -c "show interface"']

# load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

# read config file and foreach host create connection
for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
    client.connect(
        device,
        username=cfg.conf_file_contents['AUTH']['username'],
        password=cfg.conf_file_contents['AUTH']['password'])
    for i in commandList:
        current_query = Query(device, i)
        current_query.send_query(client)
        query_dictionary[current_query.device + '.' + current_query.cmd] = current_query.result
        print(current_query)
client.close()

for i in query_dictionary:
    if 'show arp' in i:
        result = parser.parse_show_arp(query_dictionary[i])
        print(result)
