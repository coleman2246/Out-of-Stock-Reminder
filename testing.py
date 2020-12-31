import urllib.request

import requests 

url = "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=184760"

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
r = requests.get(url,headers = header)



f = open("test.html", "w")
f.write(str(r.text))

f.close()
