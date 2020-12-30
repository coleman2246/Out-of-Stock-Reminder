import requests 
import urllib.request

url = "https://www.bestbuy.ca/en-ca/product/asus-vivobook-15-6-laptop-slate-grey-intel-core-i5-1035g1-512gb-ssd-16gb-ram-windows-10/14934342"

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
r = requests.get(url,headers = header)



f = open("test.html", "w")
f.write(str(r.text))

f.close()
