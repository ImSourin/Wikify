import json
import requests
import re
import ast

def getvalue(param,url):
    '''This function takes a url and a param as paramters and 
    returns the corresponding entry in the json object fetched from the
    url''' 
    try:
        '''split the param according to a regular expression to 
        recursively get the corresponding data value'''
        paramvalues = re.findall("([a-zA-Z0-9_]+)",param)
        for i in range(len(paramvalues)):
            if paramvalues[i].isdigit():
                '''Any digit signifies a list index. Change it to integer for accessing directly.'''
                paramvalues[i] = int(paramvalues[i])
        '''Initial json object'''
        data = json.loads((requests.get(url)).content)
        for i in range(len(paramvalues)):
            def has_json(url):
                '''This function returns true if the given url returns a 
                valid json object, Flase otherwise.'''
                try:
                    _ = json.loads((requests.get(url)).content)
                except:
                    '''Returns false if json.loads returns an error'''
                    return False
                else:
                    return True
            if has_json(data):
                '''If the data value is a url with a valid json object, then fetch that json object.'''
                data = json.loads((requests.get(data)).content)
            '''Recursively move across the list for the final result.'''
            data = data[paramvalues[i]]    
    except:
        '''In case of any error in the above stages, the returned value will be None and an error will be throws at the caller.'''
        return None
    else:
        '''If there are no errors, return the data value fetched.'''
        return data
