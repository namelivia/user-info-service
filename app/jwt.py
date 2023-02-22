import jwt
import requests
import json
import os
from jwcrypto import jwk, jwt


class JWT:
    @staticmethod
    def get_current_user_info(jwt_assertion: str):
        url = os.environ["JWK_ENDPOINT"]
        # Get key sets from the JWK endpoint
        jwks = jwk.JWKSet().from_json(requests.get(url).text)
        # Decode token
        token = jwt.JWT(jwt=jwt_assertion, key=jwks)
        return json.loads(token.claims)
