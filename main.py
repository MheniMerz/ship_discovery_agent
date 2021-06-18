import os
from paramiko import SSHClient, AutoAddPolicy

client = SSHClient()

#load host ssh keys
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
client.load_system_host_keys()

# known_hosts policy
client.set_missing_host_key_policy(AutoAddPolicy())

# read config file and foreach host create connection
client.connect('border01', username='admin', password='YourPaSsWoRd')
stdin, stdout, stderr = client.exec_command('show arp')
if stdout.channel.recv_exit_status() == 0:
    print(f'STDOUT: {stdout.read().decode("utf8")}')
else:
    print(f'STDERR: {stderr.read().decode("utf8")}')

stdin.close()
stdout.close()
stderr.close()
#run commands
# show arp
# show ip route
# show acl table, show acl rules
