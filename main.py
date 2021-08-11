import os
import json
import time
import collections
import concurrent
import requests
from concurrent.futures import ThreadPoolExecutor
from paramiko import SSHClient, AutoAddPolicy
from config.config import Config
from query.query import Query
from parser.parser import Parser
from request.request import Request
from pathlib import Path
import glob

client = SSHClient()
parser = Parser()
deviceList = []
query_dictionary = {}
jsonDict = {}

# list of commands that will be run for each node on network
commandList = ['show arp', 'show ip route', 'show acl table', 'show acl rule', 'show lldp table', 'show vlan config',
               'vtysh -c "show interface"', 'show ip bgp neighbors']
headerList = ['arp', 'ipRoute', 'aclTable', 'aclRule', 'lldp', 'vlan', 'interface', 'bgp']

def loadSSH():
    # load host ssh keys
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    # known_hosts policy
    client.set_missing_host_key_policy(AutoAddPolicy())
    print(glob.glob("/*"))
    direcList = glob.glob("/*")
    for direc in direcList:
        print(glob.glob("/" + direc + "/*"))
def collectData():
    # read config file and foreach host create connection
    conf = "/ship_discovery_agent/config/config.ini"
    for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
        client.connect(
            device,
            username=cfg.conf_file_contents['AUTH']['username'],
            password=cfg.conf_file_contents['AUTH']['password'])
        deviceList.append(device)
        for i in commandList:
            current_query = Query(device, i)
            current_query.send_query(client)
            query_dictionary[current_query.device + '.' + current_query.cmd] = current_query
    client.close()

def jsonParse():
    outputDict = {}
    n = 0
    # parsing data into JSON
    for i in query_dictionary:
        result = parser.parse_query_result(query_dictionary[i])
        outputDict[headerList[n % len(headerList)]] = result
        if ((n+1) % len(headerList)) == 0:
            jsonDict[deviceList[int(n / len(headerList))]] = outputDict
            outputDict = {}
        n += 1
    json_network = json.dumps(jsonDict)

    # saving JSON output to a JSON file
    jsonFile = open("data.json", "w+")
    jsonFile.write(json_network)
    jsonFile.close()

def jsonSend():
    filename = 'data.json'

    # uploading JSON file to controller
    current_request = Request()
    current_request.postRequest(cfg.controller_url, filename)

if __name__ == '__main__':
    cfg = Config()
    #load ssh keys and set up known_hosts
    loadSSH()
    if(cfg.repeat_timer == None):
        collectData()
        jsonParse()
        jsonSend()
    else:
        while(True):
            collectData()
            jsonParse()
            jsonSend()
            time.sleep(int(cfg.repeat_timer))
