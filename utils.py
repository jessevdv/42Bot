
import logging
logging.basicConfig(filename='bot.log',
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',)

import requests
import requests_cache
import os
import time
import pymongo

requests_cache.install_cache(expire_after=360, allowable_methods=('GET', 'POST'))

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
    logging.info("Attempting to get a token from intranet")
    res = requests.post(uri, params=request_token_payload)
    if res.status_code != 200:
      logging.warning(res.reason)
    else:
      rj = res.json()
      self.token = rj["access_token"]
      logging.info("Token received from intra")
    return self.token
    
  def request(self, url):  
    if not url.startswith("http"):
      url = f"https://api.intra.42.fr/v2/{url}"   
    if self.token is None:
      header = {"Authorization": f"Bearer {self.request_token()}"}
    else:
      header = {"Authorization": f"Bearer {self.token}"}
    logging.debug(f"Attempting a request to {url}")
    res = requests.get(url, headers=header)
    rc = res.status_code
    if rc != 200:
      logging.warning(f"{res.reason}")
      if rc == 429:
        logging.info(f"Rate limit exceeded - Waiting {res.headers['Retry-After']}s before requesting again")
        time.sleep(float(res.headers['Retry-After']))
        self.request(url)
      if rc == 401:
        self.request_token()
        self.request(url)
    logging.info(f"Request to {url} returned with code {rc}")    
    return (res)


def connectMongo(collection_name: str):
  mongo_secret = os.environ['mongo_secret']
  client = pymongo.MongoClient(f"mongodb+srv://Neutron:{mongo_secret}@codambot.dbbyafe.mongodb.net/?retryWrites=true&w=majority")
  db = client.CodamBot
  collection = db[collection_name]
  
  return collection