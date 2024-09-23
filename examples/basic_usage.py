from ssh_gpu import SSHClient

def main():
    client = SSHClient()
    
    try:
        # Connect to the remote server
        client.connect('example.com', username='user', password='password')
        
        # Execute a command
        stdin, stdout, stderr = client.exec_command('ls -l')
        
        # Print the output
        print(stdout.read().decode())
        
        # Close the connection
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
