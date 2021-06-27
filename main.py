import concurrent
import os
import json
from concurrent.futures import ThreadPoolExecutor
from paramiko import SSHClient, AutoAddPolicy

from config.config import Config
from query.query import Query

cfg = Config()
client = SSHClient()

# list of commands that will be run for each node on network
commandList = ['show arp', 'show ip route', 'show acl table', 'show acl rule']


def show_commands(device):
    client.connect(
        device,
        username=cfg.conf_file_contents['AUTH']['username'],
        password=cfg.conf_file_contents['AUTH']['password'])
    for i in commandList:
        current_query = Query(device, i)
        print('\n' + device + ': ' + i.split(' ', 1)[1] + '\n')
        current_query.send_query(client)
        print(current_query.result)

with concurrent.futures.ThreadPoolExecutor() as executor:
    # load host ssh keys
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

    # known_hosts policy
    client.set_missing_host_key_policy(AutoAddPolicy())

    for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
        future = executor.submit(show_commands, device=device)

client.close()

# run commands
# show arp
# show ip route
# show acl table, show acl rules
