import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
# files = {
#     'file': ('customerTemp.xlsx', open(r'D:\模板\customerTemp.xlsx', 'rb'), 'file/xlsx')
# }
url = "http://testtiger.csjmro.com/webApi/customer/importCustomerInfo"
multipart_encoder = MultipartEncoder(
    fields={
        'file': ('customerTemp.xlsx', open('D:\模板\customerTemp.xlsx', 'rb'))
    }
)
headers = {
    "Content-Type": multipart_encoder.content_type
}
cookies = {"JSESSIONID": "A053F8EE9A61813FB371F6654A34EDEA"}


res = requests.post(url=url, data=multipart_encoder,cookies=cookies,  headers=headers)
print(res.json())