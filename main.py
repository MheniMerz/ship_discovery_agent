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


def show_commands(device):
    # load host ssh keys
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

    # known_hosts policy
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(
        device,
        username=cfg.conf_file_contents['AUTH']['username'],
        password=cfg.conf_file_contents['AUTH']['password'])
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


with concurrent.futures.ThreadPoolExecutor() as executor:
    for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
        future = executor.submit(show_commands, device=device)

client.close()

# run commands
# show arp
# show ip route
# show acl table, show acl rules
