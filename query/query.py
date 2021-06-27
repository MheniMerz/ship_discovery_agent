class Query:
    def __init__(device: str, cmd: str):
        self.device = device
        self.cmd = cmd
        self.result = None

    def send_query(ssh_client):
        stdin, stdout, stderr = ssh_client.exec_command(self.cmd)
        self.result = stdout.read.decode("utf8")
        stdin.close()
        stdout.close()
        stderr.close()



