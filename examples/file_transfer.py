from ssh_gpu import SSHClient

def progress(transferred, total):
    print(f"Transferred: {transferred}/{total}")

def main():
    client = SSHClient()
    
    try:
        # Connect to the remote server
        client.connect('example.com', username='user', password='password')
        
        # Open an SFTP session
        sftp = client.open_sftp()
        
        # Upload a file
        sftp.put('local_file.txt', '/remote/path/file.txt', callback=progress)
        
        # Download a file
        sftp.get('/remote/path/remote_file.txt', 'downloaded_file.txt', callback=progress)
        
        # Close the SFTP session and the connection
        sftp.close()
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
