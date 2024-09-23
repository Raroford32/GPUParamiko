import socket
import paramiko
import threading
import os

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # For demonstration purposes, accept any username/password combination
        # In a real-world scenario, you would implement proper authentication here
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    
    try:
        transport = paramiko.Transport(client_socket)
        host_key = paramiko.RSAKey(filename="server_key.pem")
        transport.add_server_key(host_key)
        
        server = SSHServer()
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            print("No channel opened")
            return

        print(f"Authenticated with {addr}")
        
        while True:
            command = channel.recv(1024).decode()
            if not command:
                break
            
            # Execute the command and send back the output
            # In a real implementation, you would use subprocess or a similar module to execute commands
            output = f"Received command: {command}"
            channel.send(output.encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(port=2222):
    print(f"Starting SSH_GPU server on port {port}")
    
    if not os.path.exists("server_key.pem"):
        print("Server key not found. Please run generate_server_key.py first.")
        return
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)

        print(f"Listening for connections on port {port}...")

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
