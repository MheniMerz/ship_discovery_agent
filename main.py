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

client = SSHClient()
parser = Parser()
#nested dict containing query results for each device
query_dictionary = {}
jsonDict = {}

# list of commands that will be run for each node on network
command_dict = {
        'metadata': 'show runningconfiguration all | grep -A 11 -i metadata',
        'arp': 'show arp',
        'ipRoute': 'show ip route',
        'aclTable': 'show acl table',
        'aclRule': 'show acl rule',
        'lldp': 'show lldp table',
        'vlan': 'show vlan config',
        'interface': 'vtysh -c "show interface"',
        'bgp': 'show ip bgp neighbors'
}

def loadSSH():
    # load host ssh keys
    client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    # known_hosts policy
    client.set_missing_host_key_policy(AutoAddPolicy())
def collectData():
    # read config file and foreach host create connection
    for device in json.loads(cfg.conf_file_contents['TARGETS']['devices']):
        client.connect(
            device,
            username=cfg.conf_file_contents['AUTH']['username'],
            password=cfg.conf_file_contents['AUTH']['password'],
            allow_agent=False,
            banner_timeout=10
        )
        #initialize device dict
        query_dictionary[device] = {}
        for key in command_dict:
            current_query = Query(device, command_dict[key], key)
            current_query.send_query(client)
            query_dictionary[current_query.device][current_query.template] = current_query
    client.close()

def jsonParse():
    outputDict = {}
    # parsing data into JSON
    for i in query_dictionary:
        for j in query_dictionary[i]:
            result = parser.parse_query_result(query_dictionary[i][j])
            outputDict[j] = result
        jsonDict[i] = outputDict
        outputDict = {}
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
