from .nikto import nikto_rep_generate
from .nmap import nmap_rep_generate
from json import loads

def generate_report(tool_name, rep_json):
    json = loads(rep_json)
    if tool_name is 'nmap':
        return nmap_rep_generate(json)
    elif tool_name is 'nikto':
        return nikto_rep_generate(json)
    else:
        raise ModuleNotFoundError