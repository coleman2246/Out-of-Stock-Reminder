import requests 


url = "https://www.newegg.ca/black-google-6-gsm-hspa-lte/p/23B-001E-000V8?Item=9SIAKFJ9DY5542"

r = requests.get(url)

print(r.text)
f = open("test.html", "w")
f.write(str(r.text))
f.close()