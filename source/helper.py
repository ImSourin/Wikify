import json
import requests
import re
import ast

def getvalue(param,url):
    try:
        paramvalues = re.findall("([a-zA-Z0-9_]+)",param)
        for i in range(len(paramvalues)):
            if paramvalues[i].isdigit():
                paramvalues[i] = int(paramvalues[i])
        data = json.loads((requests.get(url)).content)
        for i in range(len(paramvalues)):
            def has_json(url):
                try:
                    _ = json.loads((requests.get(url)).content)
                except:
                    return False
                else:
                    return True
            if has_json(data):
                data = json.loads((requests.get(data)).content)
            data = data[paramvalues[i]]    
    except:
        return None
    else:
        return data
