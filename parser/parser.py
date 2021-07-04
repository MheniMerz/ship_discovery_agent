import textfsm

class Parser:
    def parse_show_arp(self, query_result: str):
        with open('templates/show_arp.template') as template:
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseText(query_result)
            return result


