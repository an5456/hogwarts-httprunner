import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
url = ""
multipart_encoder = MultipartEncoder(
    fields={
        'file': ('customerTemp.xlsx', open('D:\模板\customerTemp.xlsx', 'rb'))
    }
)
headers = {
    "Content-Type": multipart_encoder.content_type
}
cookies = {"JSESSIONID": "32FF8D6B394101EAF6095D7F113C804E"}

res = requests.post(url=url, data=multipart_encoder,cookies=cookies,  headers=headers)
print(res.json())








url = "http://testtiger.csjmro.com/webApi/customer/importCustomerInfo"