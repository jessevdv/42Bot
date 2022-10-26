import requests
import os


class IntraAPI(object):
  def __init__(self):
    self.token = None
    
  def request_token(self):
    uri = "https://api.intra.42.fr/v2/oauth/token"
      
    request_token_payload = {
        "client_id": os.environ['client_id'],
        "client_secret": os.environ['client_secret'],
        "grant_type": "client_credentials",
        "scope": "public",
    }
    print("Attempting to get a token from intranet")
    res = requests.post(uri, params=request_token_payload)
    rj = res.json()
    self.token = rj["access_token"]
    return self.token
    
  def request(self, url):  
    if not url.startswith("http"):
      url = f"https://api.intra.42.fr/v2/{url}"   
    if self.token is None:
      header = {"Authorization": f"Bearer {self.request_token()}"}
    else:
      header = {"Authorization": f"Bearer {self.token}"}
    print(f"Attempting a request to {url}")
    res = requests.get(url, headers=header)
    rc = res.status_code
    print(f"Request to {url} returned with code {rc}")    
    return (res)
