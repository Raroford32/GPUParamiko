import socket
from .transport import Transport
from .sftp import SFTPClient

class SSHClient:
    def __init__(self):
        self.transport = None

    def connect(self, hostname, port=22, username=None, password=None, pkey=None):
        sock = socket.create_connection((hostname, port))
        self.transport = Transport(sock)
        self.transport.start_client()

        if pkey is not None:
            self.transport.auth_publickey(username, pkey)
        elif password is not None:
            self.transport.auth_password(username, password)
        else:
            raise ValueError("No authentication method provided")

    def exec_command(self, command):
        if not self.transport:
            raise RuntimeError("Not connected")

        channel = self.transport.open_session()
        channel.exec_command(command)
        
        stdout = channel.makefile('rb', -1)
        stderr = channel.makefile_stderr('rb', -1)
        
        return channel.recv_exit_status(), stdout.read(), stderr.read()

    def open_sftp(self):
        if not self.transport:
            raise RuntimeError("Not connected")
        return SFTPClient.from_transport(self.transport)

    def close(self):
        if self.transport:
            self.transport.close()
