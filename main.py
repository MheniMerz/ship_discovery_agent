import os
import json
from paramiko import SSHClient, AutoAddPolicy
from config.config import Config

cfg = Config()
client = SSHClient()

#load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

# read config file and foreach host create connection
client.connect(
        'border01', 
        username='admin',
        password='YourPaSsWoRd')
#run the command
stdin, stdout, stderr = client.exec_command('show arp')
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
#run commands
# show arp
# show ip route
# show acl table, show acl rules
