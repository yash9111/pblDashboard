"""
Run:
"""
from mailjet_rest import Client
import os
# api_key = os.environ['MJ_APIKEY_PUBLIC']
# api_secret = os.environ['MJ_APIKEY_PRIVATE']
# print(api_secret)

api_key = "8d668ef429f0c394d4a2fab1f5e91f60"
api_secret = "d4e83a1fc798f66b654adc51421823eb"

mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
				{
						"From": {
								"Email": "ypathak188@gmail.com",
								"Name": "Yash"
						},
						"To": [
								{
										"Email": "skrchaturvedi1@gmail.com",
										"Name": "aashu"
								}
						],
						"Subject": "A test Email!",
						"TextPart": "Hello this  Email was System  generated",
				}
		]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())