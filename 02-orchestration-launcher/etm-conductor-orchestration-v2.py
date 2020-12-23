#!/usr/bin/env python
# coding: utf-8
import time
import docker
import os

unmosaicked_input = 'out/DelawareRiverBasin/Run12_04_2020'
enduser_cog_output = 'enduser/DelawareRiverBasin/drb150a/'
product='etasw'


# year='1954'
# cmd_opt = '-i ' + unmosaicked_input + ' -o ' + enduser_cog_output + ' -y ' + year + ' ' + product + ' dummy'

NUM_CONTAINERS = 23 # 40 is too high, maybe 25

MAX_LOAD_LEVEL = 220
MIN_MEMORY_AVAILABLE = 4

MAX_CONCURRENT_CONTAINERS = NUM_CONTAINERS

start_year = 2011
#start_year = 2041
end_year = 2099


# # Next Steps
# 1. make this an application so we can run it in tmux
# 2. add logging
# 3. add api - and product looping

# get client
client = docker.from_env()

running_containers = client.containers.list()
for c in running_containers:
    print(c.name)

def start_container(client, docker_image, docker_full_cmd):
    container = client.containers.run(docker_image, docker_full_cmd, detach=True)
    print ( "CONTAINER is ", container.name)
    return(container)

def start_etm(year):
    global unmosaicked_input
    global enduser_cog_output
    global product
    
    cmd_opt = '-i ' + unmosaicked_input + ' -o ' + enduser_cog_output + ' -y ' + year + ' ' + product + ' dummy'
    print(cmd_opt)
    cmd = 'python3 api_etm.py '
    full_cmd = cmd + cmd_opt
    #print(full_cmd)
    docker_image =  "tbutzer/etm_docker_image"
    #print(docker_image)
    c = start_container(client, docker_image, full_cmd)
    print("real name is", c.name)
    print("==="*30)


for yeari in range(start_year, start_year+NUM_CONTAINERS+1):
    print(yeari)
    year=str(yeari)
    start_etm(year)


running_containers = client.containers.list()
for c in running_containers:
    if len(c.attrs['Args']) >7 :
        print(c.name, c.attrs['Args'][6], c.attrs['Args'][7])

def return_cpu_load():
    cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
    return cpu_load




os.cpu_count()




import subprocess
import re

def _return_mem_stat():


    # Memory usage
    total_ram = subprocess.run(['free', '-h'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    used_free_shared_buf_avail = total_ram.split('\n')[1]
    
    return  used_free_shared_buf_avail

def return_available_memory():
    used_free_shared_buf_avail = _return_mem_stat()
    a = re.split('\s+', used_free_shared_buf_avail)
    available_memory = a[3].split('G')[0]
    return float(available_memory)




_return_mem_stat()




available_memory = return_available_memory()
available_memory




os.getloadavg()




def return_num_containers():
    global client
    running_containers = client.containers.list()
    return(len(running_containers))




def event_loop(year_to_process, end_year):
    
    
    while year_to_process <= end_year:
        time.sleep(30)

        mem_avail = return_available_memory()
        cpu_load = return_cpu_load()
        num_running_containers = return_num_containers()
        print(mem_avail, cpu_load, num_running_containers)

        cpu = False
        if (cpu_load < MAX_LOAD_LEVEL):
            print("CPU is FINE")
            cpu=True

        mem = False
        if mem_avail > MIN_MEMORY_AVAILABLE:
            mem = True

        containers = False
        if num_running_containers < MAX_CONCURRENT_CONTAINERS:
            containers = True
        

        if (mem and cpu and containers):
            print("OK to Launch")
            start_etm(str(year_to_process)) ### start mosaic container
            print("starting year", year_to_process)
            year_to_process = year_to_process + 1


cyear = start_year + NUM_CONTAINERS + 1
event_loop(cyear, end_year)






