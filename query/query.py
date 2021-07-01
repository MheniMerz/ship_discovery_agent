class Query:
    def __init__(self, device: str, cmd: str):
        self.device = device
        self.cmd = cmd
        self.result = ''

    def send_query(self, ssh_client):
        stdin, stdout, stderr = ssh_client.exec_command(self.cmd)
        for line in sdtout:
            self.result += line
        stdin.close()
        stdout.close()
        stderr.close()

    def __str__(self):
        str_value = '{'
        str_value += '\n\t hostname: '+self.device
        str_value += '\n\t command: '+self.cmd
        str_value += '\n\t result: '+self.result
        str_value += '\n}'
        return str_value
