import requests

url = "https://api.yelp.com/v3/businesses/search"

querystring = {"term":"bars","latitude":"41.8658728","longitude":"-87.6480645","limit":"50"}

headers = {
    'Authorization': "Bearer V7Y0SXB9LoGNt0l72v4jSOimKbEbqVlRaSlIRKQnPH30Rtw0OINENnkB5JGaG2rzTH8qaLtlg037BvyJ1rlja5aqUeINChy0LJBBl7r_XoO4WSgrl-djcdUUV5roXXYx",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "9a5a2a47-0400-4cc1-916e-9457fc180d54,689092e6-6b8e-4486-af3a-17b7582060e4",
    'Host': "api.yelp.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)