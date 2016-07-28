
import time
import requests
from obtain_ip import obtain_ip as op
oip = op.ObtainIP()
url = 'https://starbound-helper.herokuapp.com:443/'
while True:
    data = {'ip':oip.obtain_ip()}
    r = requests.post(url, data=data, allow_redirects=True)
    time.sleep(60)




#from urllib import request
#content = request.urlopen('http://localhost:5000/').read()
#print(content)