
import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }
    
def signJWT(user_id: str) ->  str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }
  
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM) 
    return (token)
def decodeJWT(token: str) -> dict:
    token_without_bearer = token.split(' ')[1]
    try:
        decoded_token = jwt.decode( token_without_bearer, JWT_SECRET, JWT_ALGORITHM)
       
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}