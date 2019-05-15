import requests
import json

localurl = "http://127.0.0.1:5000/api/v1"
hostedurl = "http://sourin.pythonanywhere.com/api/v1"

url = hostedurl
'''uncomment the below line for using the local api service. This can only be done after api is running locally.'''
# url = localurl

'''Create'''
json_obj = {"name": "Virat_Kohli", "params": ["type", "api_urls.references.reference_lists[0].id", "thumbnail.source"]}
print(requests.post(url=url,headers={"content-type":"application/json"},data=json.dumps(json_obj)).content.decode("utf-8"))

'''Read'''
json_obj = {"name": "Virat_Kohli", "params": ["api_urls.references.reference_lists[0].id", "thumbnail.source"]}
print(requests.get(url=url,headers={"content-type":"application/json"},data=json.dumps(json_obj)).content.decode("utf-8"))

'''Update'''
json_obj = {"name": "Virat_Kohli", "add": ["title"], "remove": ["type"]}
print(requests.put(url=url,headers={"content-type":"application/json"},data=json.dumps(json_obj)).content.decode("utf-8"))

'''Delete'''
json_obj = {"name": "Virat_Kohli"}
print(requests.delete(url=url,headers={"content-type":"application/json"},data=json.dumps(json_obj)).content.decode("utf-8"))