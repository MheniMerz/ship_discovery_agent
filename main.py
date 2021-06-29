import concurrent
import os
import json
from concurrent.futures import ThreadPoolExecutor
from paramiko import SSHClient, AutoAddPolicy
from config.config import Config

cfg = Config()
client = SSHClient()
# list of commands that will be run for each node on network
commandList = ['show arp', 'show ip route', 'show acl table', 'show acl rule']

# load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
print("1")

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())
print("2")

# read config file and foreach host create connection
for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
    print("3")
    client.connect(
        device,
        username=str(cfg.conf_file_contents['AUTH']['username']),
        password=str(cfg.conf_file_contents['AUTH']['password']))
    print("4")
    for i in commandList:
        print('\n' + device + ': ' + i.split(' ', 1)[1] + '\n')
        stdin, stdout, stderr = client.exec_command(i)
        if stdout.channel.recv_exit_status() == 0:
            print(f'{stdout.read().decode("utf8")}')
        else:
            print('===================================')
            print(f'{stderr.read().decode("utf8")}')
            print('===================================')
    stdin.close()
    stdout.close()
    stderr.close()
client.close()
