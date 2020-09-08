import requests
import json

url = "http://localhost:15672/api/queues"
response = requests.get(url, auth=('guest', 'guest'))

for q in response.json():
    print('name: %s ' % q['name'] )
    print('- consumers: %d' % q['consumers'] )
    print('- messages: %d' % q['messages'] )