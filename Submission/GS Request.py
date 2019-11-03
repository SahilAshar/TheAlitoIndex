import requests
import json

client_id = r'07597d01c4a647278eee197b16f25b90'
client_secret = r'b6eb791792918051097310c26953b80c6afd65e3ad945a50c1360d041bb3446b'

auth_data = {
    'grant_type'    : 'client_credentials',
    'client_id'     : client_id,
    'client_secret' : client_secret,
    'scope'         : 'read_content read_financial_data read_product_data read_user_profile'
}

# create session instance
session = requests.Session()

# make a POST to retrieve access_token
auth_request = session.post('https://idfs.gs.com/as/token.oauth2', data = auth_data)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict['access_token']

# update session headers
session.headers.update({'Authorization':'Bearer '+ access_token})

# test API connectivity
request_url = 'https://api.marquee.gs.com/v1/assets/data/query'
request_query = {"where": {"gsid":[
"75154"]}, "fields": ["tags"]}
request = session.post(url=request_url, json=request_query)
print(request.text)