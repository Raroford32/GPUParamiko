import os
import stat

class SFTPClient:
    def __init__(self, transport):
        self.transport = transport

    @classmethod
    def from_transport(cls, transport):
        return cls(transport)

    def put(self, localpath, remotepath, callback=None, confirm=True):
        file_size = os.path.getsize(localpath)
        with open(localpath, 'rb') as f:
            self.putfo(f, remotepath, file_size, callback, confirm)

    def putfo(self, fl, remotepath, file_size=0, callback=None, confirm=True):
        self.transport._send_message(b"putfo")
        self.transport._send_message(remotepath.encode())
        self.transport._send_message(str(file_size).encode())

        chunk_size = 8192
        bytes_sent = 0
        while True:
            data = fl.read(chunk_size)
            if not data:
                break
            encrypted_data = AES(self.transport.session_key).encrypt(data)
            self.transport._send_message(encrypted_data)
            bytes_sent += len(data)
            if callback:
                callback(bytes_sent, file_size)

        if confirm:
            response = self.transport._recv_message()
            return response == b"OK"
        return True

    def get(self, remotepath, localpath, callback=None):
        self.transport._send_message(b"get")
        self.transport._send_message(remotepath.encode())

        file_size = int(self.transport._recv_message().decode())
        with open(localpath, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                encrypted_data = self.transport._recv_message()
                data = AES(self.transport.session_key).decrypt(encrypted_data)
                f.write(data)
                bytes_received += len(data)
                if callback:
                    callback(bytes_received, file_size)

        return localpath

    def listdir(self, path='.'):
        self.transport._send_message(b"listdir")
        self.transport._send_message(path.encode())

        encrypted_response = self.transport._recv_message()
        response = AES(self.transport.session_key).decrypt(encrypted_response)
        return response.decode().split('\n')

    def mkdir(self, path, mode=511):
        self.transport._send_message(b"mkdir")
        self.transport._send_message(path.encode())
        self.transport._send_message(str(mode).encode())

        response = self.transport._recv_message()
        return response == b"OK"

    def remove(self, path):
        self.transport._send_message(b"remove")
        self.transport._send_message(path.encode())

        response = self.transport._recv_message()
        return response == b"OK"

    def rename(self, oldpath, newpath):
        self.transport._send_message(b"rename")
        self.transport._send_message(oldpath.encode())
        self.transport._send_message(newpath.encode())

        response = self.transport._recv_message()
        return response == b"OK"

    def stat(self, path):
        self.transport._send_message(b"stat")
        self.transport._send_message(path.encode())

        encrypted_response = self.transport._recv_message()
        response = AES(self.transport.session_key).decrypt(encrypted_response)
        return SFTPAttributes.from_string(response.decode())

class SFTPAttributes:
    def __init__(self, st_mode=None, st_size=None, st_uid=None, st_gid=None, st_atime=None, st_mtime=None):
        self.st_mode = st_mode
        self.st_size = st_size
        self.st_uid = st_uid
        self.st_gid = st_gid
        self.st_atime = st_atime
        self.st_mtime = st_mtime

    @classmethod
    def from_string(cls, attr_string):
        attrs = attr_string.split(':')
        return cls(
            st_mode=int(attrs[0]),
            st_size=int(attrs[1]),
            st_uid=int(attrs[2]),
            st_gid=int(attrs[3]),
            st_atime=float(attrs[4]),
            st_mtime=float(attrs[5])
        )

    def __str__(self):
        return f"{self.st_mode}:{self.st_size}:{self.st_uid}:{self.st_gid}:{self.st_atime}:{self.st_mtime}"
