import unittest
import tempfile
import os
from ssh_gpu import SSHClient
from ssh_gpu.sftp import SFTPClient, SFTPAttributes

class TestSFTPClient(unittest.TestCase):
    def setUp(self):
        self.client = SSHClient()
        # Mock connection
        self.client.transport = type('obj', (object,), {
            '_send_message': lambda self, x: None,
            '_recv_message': lambda self: b'OK'
        })()
        self.sftp = SFTPClient.from_transport(self.client.transport)

    def test_put(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = temp_file.name

        try:
            result = self.sftp.put(temp_file_path, '/remote/path')
            self.assertTrue(result)
        finally:
            os.unlink(temp_file_path)

    def test_get(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            self.client.transport._recv_message = lambda self: b'10'
            result = self.sftp.get('/remote/path', temp_file_path)
            self.assertEqual(result, temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_listdir(self):
        self.client.transport._recv_message = lambda self: b'file1\nfile2\nfile3'
        result = self.sftp.listdir('/remote/path')
        self.assertEqual(result, ['file1', 'file2', 'file3'])

    def test_mkdir(self):
        result = self.sftp.mkdir('/remote/new_dir')
        self.assertTrue(result)

    def test_remove(self):
        result = self.sftp.remove('/remote/file')
        self.assertTrue(result)

    def test_rename(self):
        result = self.sftp.rename('/remote/old_name', '/remote/new_name')
        self.assertTrue(result)

    def test_stat(self):
        attrs_str = "33188:1024:1000:1000:1621234567.89:1621234567.89"
        self.client.transport._recv_message = lambda self: attrs_str.encode()
        result = self.sftp.stat('/remote/file')
        self.assertIsInstance(result, SFTPAttributes)
        self.assertEqual(result.st_mode, 33188)
        self.assertEqual(result.st_size, 1024)

if __name__ == '__main__':
    unittest.main()
