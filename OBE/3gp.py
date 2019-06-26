import shutil
import requests
from requests.auth import HTTPBasicAuth

url = "http://obelab-api.com/api/analysis/vftdown/"
# taskUUID = '0EtpplJy'
# taskUUID = '0jvNPyGr'
taskUUID = '0jvNPyGr'
query = "?taskUUID=0jvNPyGr"

download_url = url+query

r = requests.get(url=download_url, auth=HTTPBasicAuth('admin', 'obe1234'))

print (r)
# print(r.filename)

if r.status_code==200:
    with open('%s.zip' %taskUUID, 'wb') as f:
        f.write(r.content)
        f.close()
    r_d = requests.delete(url=download_url, auth=HTTPBasicAuth('admin', 'obe1234'))