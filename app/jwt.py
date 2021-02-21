import jwt
import os
from jwt import PyJWKClient


class JWT:
    @staticmethod
    def get_current_user_info(jwt_assertion: str):
        if os.getenv("TEST_USER", False):
            return {
                "aud": [],
                "email": "testuser@localhost.com",
                "exp": 1548134702,
                "iat": 1548134702,
                "iss": "localhost.com",
                "nbf": 1548134702,
                "sub": "localhost/testuser",
            }
        url = os.environ["JWK_ENDPOINT"]
        jwks_client = PyJWKClient(url)
        signing_key = jwks_client.get_signing_key_from_jwt(jwt_assertion)
        return jwt.decode(
            jwt_assertion,
            signing_key.key,
            algorithms=["ES256"],
            options={
                "verify_aud": False,
            },
        )
