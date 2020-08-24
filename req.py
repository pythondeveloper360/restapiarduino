import requests


r = requests.post("http://127.0.0.1:5000/alter/eaf3e270-e561-11ea-86c7-f0921c5ba15a/1",auth = ('hanzala','qssa'))

print(r.text)