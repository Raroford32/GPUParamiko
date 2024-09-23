import socket
import struct
import os
from .crypto import RSA, AES

class Transport:
    def __init__(self, sock):
        self.sock = sock
        self.session_id = None
        self.server_key = None
        self.session_key = None

    def start_client(self):
        # Perform key exchange
        self._key_exchange()

    def _key_exchange(self):
        # Simplified key exchange (not secure, for demonstration only)
        client_rsa = RSA()
        client_rsa.generate_keys()

        # Send client public key
        self._send_message(b"SSH-2.0-SSH_GPU_0.1")
        self._send_message(str(client_rsa.public_key.public_numbers().n).encode())
        self._send_message(str(client_rsa.public_key.public_numbers().e).encode())

        # Receive server public key
        server_version = self._recv_message()
        server_n = int(self._recv_message().decode())
        server_e = int(self._recv_message().decode())
        self.server_key = RSA()
        self.server_key.public_key = rsa.RSAPublicNumbers(server_e, server_n).public_key()

        # Generate and exchange session key
        self.session_key = os.urandom(32)
        encrypted_session_key = self.server_key.encrypt(self.session_key)
        self._send_message(encrypted_session_key)

        self.session_id = os.urandom(16)

    def auth_password(self, username, password):
        message = f"{username}\0{password}".encode()
        encrypted_message = AES(self.session_key).encrypt(message)
        self._send_message(b"password")
        self._send_message(encrypted_message)
        response = self._recv_message()
        return response == b"OK"

    def auth_publickey(self, username, pkey):
        # Implement public key authentication
        pass

    def open_session(self):
        return Channel(self)

    def _send_message(self, data):
        self.sock.sendall(struct.pack("!I", len(data)) + data)

    def _recv_message(self):
        size = struct.unpack("!I", self.sock.recv(4))[0]
        return self.sock.recv(size)

    def close(self):
        self.sock.close()

class Channel:
    def __init__(self, transport):
        self.transport = transport
        self.channel_id = os.urandom(4)

    def exec_command(self, command):
        encrypted_command = AES(self.transport.session_key).encrypt(command.encode())
        self.transport._send_message(b"exec")
        self.transport._send_message(self.channel_id)
        self.transport._send_message(encrypted_command)

    def recv_exit_status(self):
        response = self.transport._recv_message()
        if response == b"exit_status":
            status = struct.unpack("!I", self.transport._recv_message())[0]
            return status
        return None

    def makefile(self, mode, bufsize):
        return ChannelFile(self, mode)

    def makefile_stderr(self, mode, bufsize):
        return ChannelFile(self, mode, is_stderr=True)

class ChannelFile:
    def __init__(self, channel, mode, is_stderr=False):
        self.channel = channel
        self.mode = mode
        self.is_stderr = is_stderr
        self.buffer = b""

    def read(self, size=-1):
        while size == -1 or len(self.buffer) < size:
            data = self.channel.transport._recv_message()
            if not data:
                break
            self.buffer += AES(self.channel.transport.session_key).decrypt(data)

        if size == -1:
            result = self.buffer
            self.buffer = b""
        else:
            result = self.buffer[:size]
            self.buffer = self.buffer[size:]

        return result
