import textfsm
import os

class Parser:
    def parse_show_arp(self, query_result: str):
        template_path = os.path.join(os.path.dirname(__file__),'templates/show_arp.template')
        with open(template_path) as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseText(query_result)
            return result


