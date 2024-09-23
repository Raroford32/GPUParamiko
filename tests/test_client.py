import unittest
from ssh_gpu import SSHClient

class TestSSHClient(unittest.TestCase):
    def setUp(self):
        self.client = SSHClient()

    def test_connect(self):
        # This is a mock test. In a real scenario, you'd use a test SSH server.
        with self.assertRaises(ValueError):
            self.client.connect('localhost')

    def test_exec_command(self):
        # Mock connection
        self.client.transport = type('obj', (object,), {'open_session': lambda: type('obj', (object,), {'exec_command': lambda x: None, 'recv_exit_status': lambda: 0, 'makefile': lambda x,y: type('obj', (object,), {'read': lambda: b'output'})(), 'makefile_stderr': lambda x,y: type('obj', (object,), {'read': lambda: b''})()})()})()

        status, stdout, stderr = self.client.exec_command('echo "test"')
        self.assertEqual(status, 0)
        self.assertEqual(stdout, b'output')
        self.assertEqual(stderr, b'')

    def tearDown(self):
        self.client.close()

if __name__ == '__main__':
    unittest.main()
