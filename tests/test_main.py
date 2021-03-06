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
        data = {
            "user_id": "Test user ID",
            "name": "Test name",
        }
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
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "user_id": "Some user id",
            "name": "Some name",
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
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "provider/test_user_id",
        }
        response = client.get(
            "me", headers={"X-Pomerium-Jwt-Assertion": "jwt_assertion"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "user_id": "provider/test_user_id",
            "name": "Test name",
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "provider/test_user_id",
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
        }
