from mock import patch, Mock
from freezegun import freeze_time
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.models import UserInfo
from app.schemas import UserInfo as UserInfoSchema


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_user_info(self, session, user_info: dict = {}):
        data = {"user_id": "Test user ID", "name": "Test name"}  # A
        data.update(user_info)
        db_user_info = UserInfo(**data)
        session.add(db_user_info)
        session.commit()
        return db_user_info

    def test_create_user_info(self, client):
        response = client.post(
            "/new",
            json={
                "user_id": "Some user id",
                "name": "Some name",
                "locale": "en",
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "user_id": "Some user id",
            "name": "Some name",
            "locale": "en",
        }

    def test_create_user_info_invalid(self, client):
        response = client.post("/new", json={"name": "Test"})
        assert response.status_code == 422

    @patch("app.jwt.JWT.get_current_user_info")
    def test_get_current_user_info(
        self, m_get_current_user_info, client, database_test_session
    ):
        self._insert_test_user_info(
            database_test_session, {"user_id": "provider/test_user_id"}
        )
        m_get_current_user_info.return_value = {
            "aud": "some.aud",
            "email": "some@email.com",
            "exp": 1677084692,
            "family_name": "Surname",
            "given_name": "Name",
            "groups": [],
            "iat": 1612383135,
            "iss": "authenticate.endpoint",
            "jti": "218e9c05-e3d4-4132-920d-fda95686f13b",
            "locale": "en",
            "name": "Name Surname",
            "picture": "https://image.url",
            "sid": "990efd79-bdca-4ff4-8b41-270261797161",
            "sub": "1145123213213213123781",
            "user": "112351023941203942302",
        }
        response = client.get(
            "me", headers={"X-Pomerium-Jwt-Assertion": "jwt_assertion"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "aud": "some.aud",
            "email": "some@email.com",
            "exp": 1677084692,
            "family_name": "Surname",
            "given_name": "Name",
            "groups": [],
            "iat": 1612383135,
            "iss": "authenticate.endpoint",
            "jti": "218e9c05-e3d4-4132-920d-fda95686f13b",
            "locale": "en",
            "name": "Name Surname",
            "picture": "https://image.url",
            "sid": "990efd79-bdca-4ff4-8b41-270261797161",
            "sub": "1145123213213213123781",
            "user": "112351023941203942302",
        }
        m_get_current_user_info.assert_called_with("jwt_assertion")

    def test_get__user_info(self, client, database_test_session):
        self._insert_test_user_info(
            database_test_session, {"user_id": "provider/test_user_id"}
        )
        response = client.get("/provider/test_user_id")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "user_id": "provider/test_user_id",
            "name": "Test name",
            "locale": "en",
        }
