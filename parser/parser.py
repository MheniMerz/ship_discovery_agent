import textfsm
import os
import json


class Parser:
    def __init__(self):
        self.headers = []
        self.data = []
        self.json_data = {}

    def parse_query_result(self, query):
        template_name = query.cmd.replace(' ', '_')
        template_name = template_name.replace('"', '')
        template_path = os.path.join(os.path.dirname(__file__),'templates/'+template_name+'.template')
        with open(template_path) as template:
            fsm = textfsm.TextFSM(template)
            self.headers = fsm.header
            self.data = fsm.ParseText(query.result)
            if 'metadata' in query.cmd:
                self.parse_single_row_to_json()
            else:
                self.parse_rows_to_json()
        return self.json_data

    def parse_single_row_to_json(self):
        json_dict = {}
        for header in self.headers:
            json_dict[header] = self.data[0][self.headers.index(header)]
        self.json_data = json_dict

    def parse_rows_to_json(self):
        json_dict_list = []
        json_dict = {}
        for row in self.data:
            json_dict = dict(zip(self.headers, row))
            json_dict_list.append(json_dict)
        self.json_data = json_dict_list

