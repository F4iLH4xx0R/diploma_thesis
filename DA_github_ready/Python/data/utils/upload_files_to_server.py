# Script to upload files to server via scp and start batch via ssh


import time
import os 
import unicodedata
from scp import SCPClient
import paramiko

server = ""
user = ""
password = ""
port = 22
#local_path = ""
#server_path = ""
#commands = []
#commands = ["sbatch run_dyna.sh"]

##########################
# Upload Files to Server #
##########################

def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def upload_files_and_start_run(server, port, user, password, local_path, server_path, command):
    print("Start Upload Process")

    ssh = create_ssh_client(server, port, user, password)
    stdin, stdout, stderr = ssh.exec_command("mkdir " + server_path)
    lines = stdout.readlines()
    print(lines)
    scp = SCPClient(ssh.get_transport())
    scp.put(local_path, remote_path=server_path , recursive=True)
    scp.close()

    print("Uploading Done")
    print("START SIMULATIONS")
    stdin, stdout, stderr = ssh.exec_command(command)
    print("EXECUTING: ", command)
    lines = stdout.readlines()
    print(lines)
    ssh.close()
    print("SIMULATION STARTED.")


def exec_commands(server, port, user, password, commands, stop, start = 0):
    ssh = create_ssh_client(server, port, user, password)

    for i in range(start, stop):
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command.format(i))
            print("EXECUTING: ", command.format(i))
            lines = stdout.readlines()
            print(lines)
    ssh.close()
    print("DONE")


def exec_commands_2(server, port, user, password, commands):
    ssh = create_ssh_client(server, port, user, password)
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print("Executing: ", command)
        lines = stdout.readlines()
        print(lines)
    ssh.close()
    print("DONE")


if __name__ == "__main__":
    #upload_files_and_start_run(server, port, user, password, "", "", commands)
    commands = ["sbatch run_dyna.sh"]
    exec_commands(server, port, user, password, commands, 101, 1)
    
    pass

