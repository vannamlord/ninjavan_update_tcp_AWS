import socket
import time
from datetime import datetime
import json
# AWS instance public IP address and port
aws_instance_ip = "13.250.191.21"  # public IP
aws_instance_port = 3000  # Replace with the port your server is listening on
# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set a timeout for the entire connection process (in seconds)
client_socket.settimeout(10)
machine_tag = "VNDWS-Engineer"
dws_ops = [15, 10, 65, [50.0, 50.0, 50.0, 50.0]]
data_to_send = {
    machine_tag: {
        "time": str(datetime.now()),
        "cpu": dws_ops[0],
        "ram": dws_ops[1],
        "storegare": dws_ops[2],
        "tempt": dws_ops[3],
        "net_sta": 'LAN',
        "latest_ver": '1.1.12',
        "time_zone": 'Asia/HoChiMinh',
    }
}
try:
    # Connect to the server
    client_socket.connect((aws_instance_ip, aws_instance_port))
    # Send data to the server
    client_socket.sendall(json.dumps(data_to_send).encode("utf-8"))
except:
    pass
finally:
    # Close the socket
    client_socket.close()
