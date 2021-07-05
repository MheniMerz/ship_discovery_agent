import concurrent
import os
import json
from concurrent.futures import ThreadPoolExecutor
from paramiko import SSHClient, AutoAddPolicy
from config.config import Config
import re
from io import StringIO
import sys
import textfsm
import ntc_templates
from ntc_templates.parse import parse_output

cfg = Config()
client = SSHClient()
# list of commands that will be run for each node on network
commandList = ['show arp', 'show ip route', 'show acl table', 'show acl rule']

# load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

# read config file and foreach host create connection
nD = {}
rows = []
columns = []
for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
    client.connect(
        device,
        username=cfg.conf_file_contents['AUTH']['username'],
        password=cfg.conf_file_contents['AUTH']['password'])
    for i in commandList:
        print('\n' + device + ': ' + i.split(' ', 1)[1] + '\n')
        stdin, stdout, stderr = client.exec_command(i)
        if stdout.channel.recv_exit_status() == 0:
            string1 = f'{stdout.read().decode("utf8")}'
            print(string1)
            if i == 'show arp' and device == 'border01':
                with open('discovery.template') as template:
                    fsm = textfsm.TextFSM(template)
                    result = fsm.ParseText(string1)
                print(fsm.header)
                print(result)
                #nD[device] = {'type': 'Router', 'interface': {'columns': fsm.header,   'rows': result}}
                #json_network = json.dumps(nD, indent=2)
                #print(json_network)
                arp_parsed = parse_output(platform="cisco_ios", command="show arp", data=string1)
                print(arp_parsed)

        else:
            print('===================================')
            print(f'{stderr.read().decode("utf8")}')
            print('===================================')
    stdin.close()
    stdout.close()
    stderr.close()
client.close()
