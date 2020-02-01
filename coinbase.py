import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method.upper() + request.path_url + ('')
        #message must be encoded as UTF8 to be encoded by hmac
        message = message.encode('utf-8')
        secret = base64.b64decode(self.secret_key)
        signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(API_KEY,SECRET_KEY,PASSPHRASE)

# Get accounts
r = requests.get(api_url + 'accounts/',  auth=auth)
with open('cb.json', 'w') as outfile:
    json.dump(r.json(), outfile, indent=2, sort_keys=True,)
print(r.status_code)