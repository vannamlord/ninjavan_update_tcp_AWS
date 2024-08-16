#!/usr/bin/env python
import subprocess
import threading
import time
import serial
import os
import psutil
import socket
from datetime import datetime
from pynput import keyboard
import requests
import json
import ast
################################################################################
aws_instance_ip = '3.1.64.39' # public IP
tool_check = "1.6"
soft_check = "1.1.12"
time_get_data = str(datetime.now()).split(' ')[0]
time_zone_check ="Asia/Ho_Chi_Minh"
connection_type_check = "LAN"
SSD_total = 200
hcm_checking = {"HCM offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
hn_checking = {"HN offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
dng_checking = {"DNG offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
khh_checking = {"KHH offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
dak_checking = {"DAK offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
gil_checking = {"GIL offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
nga_checking = {"NGA offline Status:":'',"Check_LAN": '',"Check_latest_version": '', "Check_time_zone": '', "Check_tool_version":'',"Check_SSD_Storegare":'',"Check_journal_Status":'',"Error_Journal_Cammand":''}
total_machine_hcm=0
total_machine_hn=0
total_machine_dng=0
total_machine_khh=0
total_machine_dak=0
total_machine_gil=0
total_machine_nga=0
hcm_machine_id_deploy = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",\
    "16","17","18","19","20","21B","22B","23B","24B","25B","26B","27B","28B","29","30"]
hn_machine_id_deploy = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",\
    "16","17","18","19","20","21","22","23","24","25","26B","27B","28B","29B","30B","31B","32B","33B",\
        "34","35","36","37","38","39"]
dng_machine_id_deploy = ["01","02","03","04B"]
khh_machine_id_deploy = ["01","02","04B"]
dak_machine_id_deploy = ["01","02B"]
gil_machine_id_deploy = ["01","02B"]
nga_machine_id_deploy = ["01"]
# AWS instance public IP address and port
aws_instance_port = 3000  # Replace with the port your server is listening on

# Data to be sent to the server
data_to_send = "Check-status-DWS-VN"

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_to_write = ''
file_path = 'D:\\WORKING_FILE\Working_File\\Software_Dev\size_check_project\\ninjavan_update_7_tcp_AWS\\dws_ops_VN.txt'
try:
    # Open the file in write mode ('w')
    with open(file_path, 'w') as file:
        # Write the data to the file
        file.write(data_to_write)
    file.close()
except:
    pass
try:
    try:
        # Connect to the server
        client_socket.connect((aws_instance_ip, aws_instance_port))

        # Send data to the server
        client_socket.sendall(data_to_send.encode('utf-8'))
    except:
        print('Something Wrong')

    # Receive the response from the server
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        if (response == ''):
            break
        try:
            response = response.replace('(high=100.0,crit=100.0)','')
            data_re = dict(ast.literal_eval(response))
            machine_id = str(next(iter(data_re)))
            time_record = str(data_re[machine_id]["time"]).split(' ')[0]
            if('=' not in response):
                if("HCM" == machine_id.split('-')[1]):
                    hcm_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_hcm = total_machine_hcm + 1
                    if(time_record != time_get_data):
                        hcm_checking["HCM offline Status:"] = hcm_checking["HCM offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        hcm_checking["Check_LAN"] = hcm_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        hcm_checking["Check_latest_version"] = hcm_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        hcm_checking["Check_time_zone"] = hcm_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        hcm_checking["Check_SSD_Storegare"] = hcm_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        hcm_checking["Check_journal_Status"] = hcm_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        hcm_checking["Error_Journal_Cammand"] = hcm_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            hcm_checking["Check_tool_version"] = hcm_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("HN" == machine_id.split('-')[1]):
                    hn_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_hn = total_machine_hn + 1
                    if(time_record != time_get_data):
                        hn_checking["HN offline Status:"] = hn_checking["HN offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        hn_checking["Check_LAN"] = hn_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        hn_checking["Check_latest_version"] = hn_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        hn_checking["Check_time_zone"] = hn_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        hn_checking["Check_SSD_Storegare"] = hn_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        hn_checking["Check_journal_Status"] = hn_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        hn_checking["Error_Journal_Cammand"] = hn_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            hn_checking["Check_tool_version"] = hn_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("DNG" == machine_id.split('-')[1]):
                    dng_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_dng = total_machine_dng + 1
                    if(time_record != time_get_data):
                        dng_checking["DNG offline Status:"] = dng_checking["DNG offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        dng_checking["Check_LAN"] = dng_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        dng_checking["Check_latest_version"] = dng_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        dng_checking["Check_time_zone"] = dng_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        dng_checking["Check_SSD_Storegare"] = dng_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        dng_checking["Check_journal_Status"] = dng_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        dng_checking["Error_Journal_Cammand"] = dng_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            dng_checking["Check_tool_version"] = dng_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("KHH" == machine_id.split('-')[1]):
                    khh_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_khh = total_machine_khh + 1
                    if(time_record != time_get_data):
                        khh_checking["KHH offline Status:"] = khh_checking["KHH offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        khh_checking["Check_LAN"] = khh_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        khh_checking["Check_latest_version"] = khh_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        khh_checking["Check_time_zone"] = khh_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        khh_checking["Check_SSD_Storegare"] = khh_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        khh_checking["Check_journal_Status"] = khh_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        khh_checking["Error_Journal_Cammand"] = khh_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            khh_checking["Check_tool_version"] = khh_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("DAK" == machine_id.split('-')[1]):
                    dak_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_dak = total_machine_dak + 1
                    if(time_record != time_get_data):
                        dak_checking["DAK offline Status:"] = dak_checking["DAK offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        dak_checking["Check_LAN"] = dak_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        dak_checking["Check_latest_version"] = dak_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        dak_checking["Check_time_zone"] = dak_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        dak_checking["Check_SSD_Storegare"] = dak_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        dak_checking["Check_journal_Status"] = dak_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        dak_checking["Error_Journal_Cammand"] = dak_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            dak_checking["Check_tool_version"] = dak_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("GIL" == machine_id.split('-')[1]):
                    gil_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_gil = total_machine_gil + 1
                    if(time_record != time_get_data):
                        gil_checking["GIL offline Status:"] = gil_checking["GIL offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        gil_checking["Check_LAN"] = gil_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        gil_checking["Check_latest_version"] = gil_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        gil_checking["Check_time_zone"] = gil_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        gil_checking["Check_SSD_Storegare"] = gil_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        gil_checking["Check_journal_Status"] = gil_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        gil_checking["Error_Journal_Cammand"] = gil_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            gil_checking["Check_tool_version"] = gil_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
                elif ("NGA" == machine_id.split('-')[1]):
                    nga_machine_id_deploy.remove(machine_id.split('-')[2])
                    total_machine_nga = total_machine_nga + 1
                    if(time_record != time_get_data):
                        nga_checking["NGA offline Status:"] = nga_checking["NGA offline Status:"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["net_sta"] != connection_type_check):
                        nga_checking["Check_LAN"] = nga_checking["Check_LAN"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["latest_ver"] != soft_check):
                        nga_checking["Check_latest_version"] = nga_checking["Check_latest_version"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["time_zone"] != time_zone_check):
                        nga_checking["Check_time_zone"] = nga_checking["Check_time_zone"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["SSD_storegare"] < SSD_total):
                        nga_checking["Check_SSD_Storegare"] = nga_checking["Check_SSD_Storegare"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][0] == True):
                        nga_checking["Check_journal_Status"] = nga_checking["Check_journal_Status"] + ';' + machine_id.split('-')[2]
                    if(data_re[machine_id]["journal_status"][2] == True):
                        nga_checking["Error_Journal_Cammand"] = nga_checking["Error_Journal_Cammand"] + ';' + machine_id.split('-')[2]
                    try:
                        if(data_re[machine_id]["tool_version"] != tool_check):
                            nga_checking["Check_tool_version"] = nga_checking["Check_tool_version"] + ';' + machine_id.split('-')[2]
                    except:
                        pass
        except:
            pass
except:
    pass
client_socket.close()
list_checking = [hcm_checking,hn_checking,dng_checking,khh_checking,dak_checking,gil_checking,nga_checking]
for x in list_checking:
    # Open the file in write mode ('a')
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(str(x) + '\n')
        time.sleep(0.1)
    file.close()

record_number_machine = "HCM: "+ str(total_machine_hcm) + ',' +"HN: "+ str(total_machine_hn) + ',' \
    +"DNG: "+ str(total_machine_dng) + ',' + "KHH: "+ str(total_machine_khh) + ',' \
        +"DAK: "+ str(total_machine_dak) + ',' + "GIL: "+ str(total_machine_gil) + ',' + "NGA: "+ str(total_machine_nga)

# Open the file in write mode ('a')
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write(record_number_machine + '\n')
file.close()
# Open the file in write mode ('a')
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("HCM: "+ str(hcm_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("HN: "+ str(hn_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("DNG: "+ str(dng_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("KHH: "+ str(khh_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("DAK: "+ str(dak_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("GIL: "+ str(gil_machine_id_deploy) + '\n')
file.close()
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write("NGA: "+ str(nga_machine_id_deploy) + '\n')
file.close()

