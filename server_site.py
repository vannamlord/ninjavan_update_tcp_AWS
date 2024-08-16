import socket
import os
import time
import threading
import subprocess
import json
###############################################################################
# Server IP address and port
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 3000  # Choose a port number
FORMAT = 'utf-8'
# Open collect tool
def socket_recv():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            while True:
                try:
                    print('Listen from new machine')
                    conn, addr = server_socket.accept()
                    with conn:
                        while True:
                            try:
                                data = conn.recv(1024).decode('utf-8')
                                if(data == "Check-status-DWS-VN"):
                                    folder_path = '/home/ec2-user/log_file'
                                    # List all files in the folder
                                    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                                    # Read the content of each text file
                                    for file_name in file_list:
                                        print('Processing data and send to Engineer')
                                        file_path = os.path.join(folder_path, file_name)
                                        with open(file_path, 'r') as file:
                                            response_data = file.read()+'\n'
                                            conn.sendall(response_data.encode('utf-8'))
                                            time.sleep(0.1)
                                        file.close()
                                else:
                                    try:
                                        data_dict = dict(json.loads(data))
                                        for key in data_dict.keys():
                                            machine_id = key
                                    except:
                                        machine_id = data.split('=')[1]
                                    file_path = '/home/ec2-user/log_file/' + machine_id
                                    try:
                                        print('Getting data from ' + machine_id)
                                        # Open the file in write mode ('w')
                                        with open(file_path, 'w') as file:
                                            # Write the data to the file
                                            file.write(data)
                                        file.close()
                                    except:
                                        pass
                                conn.close()
                                break
                            except:
                                pass
                except:
                    pass
    except:
        pass
socket_recv()