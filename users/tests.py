from rest_framework.test import APITestCase
from .models import User


class TestUserRegister(APITestCase):

    USERNAME = "Test User"
    GENDER = "male"
    EMAIL = "testEmail@gmail.com"

    URL = "/api/v1/users/"

    def test_create_user(self):
        test_username = "test_username"
        test_password = "test_password"

        # username이나 password를 안 넘겼을 때 에러 띄우기
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.post(
            self.URL,
            data={"username": test_username},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.post(
            self.URL,
            data={"password": test_password},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # username과 password만으로도 계정 만들기
        response = self.client.post(
            self.URL,
            data={
                "username": test_username,
                "password": test_password,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        data = response.json()
        # print(data)
        # {'username': 'test_username', 'email': '', 'first_name': '', 'last_name': '', 'gender': ''}

        self.assertIn("email", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("gender", data)

        self.assertEqual(
            data["username"],
            test_username,
        )

        # 이미 있는 username으로 계정 만들기 시도
        response = self.client.post(
            self.URL,
            data={
                "username": test_username,
                "password": "123",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # 비어있는 정보 가지고 계정 생성 시도
        response = self.client.post(
            self.URL,
            data={
                "username": "test_blank",
                "password": "test_blank_password",
                "email": "",
                "first_name": "",
                "last_name": "",
                "gender": "",
            },
        )

        # 모든 정보를 가지고 계정 생성 시도
        test_username_2 = "test_username_2"
        test_password_2 = "test_password_2"
        test_email = "testEmail@gmail.com"
        test_first_name = "first_name"
        test_last_name = "last_name"
        test_gender = "male"

        response = self.client.post(
            self.URL,
            data={
                "username": test_username_2,
                "password": test_password_2,
                "email": test_email,
                "first_name": test_first_name,
                "last_name": test_last_name,
                "gender": test_gender,
            },
        )

        data = response.json()

        self.assertEqual(
            data["email"],
            test_email,
        )
        self.assertEqual(
            data["first_name"],
            test_first_name,
        )
        self.assertEqual(
            data["last_name"],
            test_last_name,
        )
        self.assertEqual(
            data["gender"],
            test_gender,
        )
        self.assertEqual(
            data["username"],
            test_username_2,
        )


class TestUserProfile(APITestCase):

    USERNAME = "test_user"
    PASSWORD = "123"

    URL = "/api/v1/users/profile/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_get_profile(self):
        # 로그인하지 않고 profile 얻기 시도
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 profile 얻기 시도
        self.client.force_login(
            self.user,
        )

        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        # print(data)
        # {'username': 'test_user', 'email': '', 'first_name': '', 'last_name': '', 'gender': ''}

        self.assertIn("email", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("gender", data)

        self.assertEqual(
            data["username"],
            self.USERNAME,
        )

    def test_put_profile(self):
        # 로그인하지 않고 profile put 시도
        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 profile put 시도
        self.client.force_login(
            self.user,
        )

        # 아무 데이터 없이 Put 시도
        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            200,
        )

        # 일부 데이터만 Put 시도
        test_new_username = "new_username"

        response = self.client.put(
            self.URL,
            data={"username": test_new_username},
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertIn("email", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("gender", data)

        self.assertEqual(
            data["username"],
            test_new_username,
        )

        # 모든 데이터 Put 시도
        test_latest_username = "latest_username"
        test_email = "testEmail@gmail.com"
        test_first_name = "first_name"
        test_last_name = "last_name"
        test_gender = "male"

        response = self.client.put(
            self.URL,
            data={
                "username": test_latest_username,
                "email": test_email,
                "first_name": test_first_name,
                "last_name": test_last_name,
                "gender": test_gender,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        # print(data)
        # {'username': 'test_user', 'email': 'testEmail@gmail.com', 'first_name': 'first_name', 'last_name': 'last_name', 'gender': 'male'}

        self.assertEqual(
            data["username"],
            test_latest_username,
        )
        self.assertEqual(
            data["email"],
            test_email,
        )
        self.assertEqual(
            data["first_name"],
            test_first_name,
        )
        self.assertEqual(
            data["last_name"],
            test_last_name,
        )
        self.assertEqual(
            data["gender"],
            test_gender,
        )


class TestChangePassword(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "123"

    URL = "/api/v1/users/profile/password/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_change_password(self):
        # 로그인하지 않고 put 시도
        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 테스트 진행
        self.client.force_login(
            self.user,
        )

        # old_password나 new_password가 없으면 에러 띄우기
        test_new_password = "new_password_123"

        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.put(
            self.URL,
            data={"old_password": self.PASSWORD},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.put(
            self.URL,
            data={"new_password": test_new_password},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # old_password가 틀렸으면 에러 띄우기
        response = self.client.put(
            self.URL,
            data={
                "old_password": "wrong_old_password",
                "new_password": test_new_password,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # old_password와 new_password가 같을 때 에러 띄우기
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.PASSWORD,
                "new_password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.put(
            self.URL,
            data={
                "old_password": test_new_password,
                "new_password": test_new_password,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # 실제로 비밀번호 바꾸기
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.PASSWORD,
                "new_password": test_new_password,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        # 새로운 비밀번호 로그인해보기
        self.client.logout()
        self.client.login(
            username=self.USERNAME,
            password=test_new_password,
        )


class TestJWTLogin(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "123"

    URL = "/api/v1/users/login/"
    URL_PROFILE = "/api/v1/users/profile/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_login(self):
        # username이나 password 없으면 에러 띄우기
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.post(
            self.URL,
            data={"username": self.USERNAME},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.post(
            self.URL,
            data={"username": self.PASSWORD},
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # 입력한 username이 존재하지 않을 때
        response = self.client.post(
            self.URL,
            data={
                "username": "wrong_username",
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertEqual(
            response.json()["error"],
            "wrong username",
        )

        # 비밀번호 틀렸을 때
        response = self.client.post(
            self.URL,
            data={
                "username": self.USERNAME,
                "password": "wrong_password",
            },
        )
        self.assertEqual(
            response.json()["error"],
            "wrong password",
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # 로그인 테스트
        response = self.client.post(
            self.URL,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        # 로그인 후 profile 볼 수 있는지 테스트
        # headers로 jwt token 전달
        response = self.client.get(
            self.URL_PROFILE,
            headers={"jwt": response.json()["token"]},
        )
        self.assertEqual(
            response.status_code,
            200,
        )


class TestLogOut(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "123"

    URL_LOGOUT = "/api/v1/users/logout/"
    URL_LOGIN = "/api/v1/users/login/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_get_profile(self):
        # 로그인하지 않고 로그아웃 시도
        response = self.client.post(self.URL_LOGOUT)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 로그아웃 시도
        response = self.client.post(
            self.URL_LOGIN,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.client.post(
            self.URL_LOGOUT,
            headers={"jwt": response.json()["token"]},
        )
        self.assertEqual(
            response.status_code,
            200,
        )
