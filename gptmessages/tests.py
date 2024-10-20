from rest_framework.test import APITestCase
from . import models
from users.models import User
from gptconversations.models import Conversation


class TestMessagesLists(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "123"

    TITLE = "test_title"

    USER_MESSAGE = "test user message"
    AI_MESSAGE = "test ai message"

    URL = "/api/v1/messages/"

    LOGIN_URL = "/api/v1/users/login/"

    def setUp(self):
        # user 생성
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

        # conversation 생성
        conversation = Conversation.objects.create(
            owner=self.user,
            title=self.TITLE,
        )
        conversation.save()
        self.conversation = conversation

        # message 생성
        message = models.Message.objects.create(
            conversation=self.conversation,
            user_message=self.USER_MESSAGE,
            ai_message=self.AI_MESSAGE,
        )
        message.save()
        self.message = message

        # token 얻기
        response = self.client.post(
            self.LOGIN_URL,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        token = response.json()["token"]
        self.token = token

    def test_get_messages(self):

        # 로그인하지 않고 get 해보기
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 get 해보기
        response = self.client.get(
            self.URL,
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        # print(data)
        # [{'id': 1, 'conversation': 'test_title', 'user_message': 'test user message', 'ai_message': 'test ai message'}]

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["id"],
            1,
        )
        self.assertEqual(
            data[0]["conversation"],
            self.TITLE,
        )
        self.assertEqual(
            data[0]["user_message"],
            self.USER_MESSAGE,
        )
        self.assertEqual(
            data[0]["ai_message"],
            self.AI_MESSAGE,
        )


class TestConversationMessages(APITestCase):

    USERNAME = "test_user"
    PASSWORD = "123"

    DIFF_USERNAME = "diff_test_user"
    DIFF_PASSWORD = "diff_123"

    TITLE = "test_title"

    USER_MESSAGE = "test user message"
    AI_MESSAGE = "test ai message"

    URL = "/api/v1/messages/"

    LOGIN_URL = "/api/v1/users/login/"

    def setUp(self):
        # user 생성
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

        # diff user 생성
        diff_user = User.objects.create(
            username=self.DIFF_USERNAME,
        )
        diff_user.set_password(self.DIFF_PASSWORD)
        diff_user.save()
        self.diff_user = diff_user

        # conversation 생성
        conversation = Conversation.objects.create(
            owner=self.user,
            title=self.TITLE,
        )
        conversation.save()
        self.conversation = conversation

        # message 생성
        message = models.Message.objects.create(
            conversation=self.conversation,
            user_message=self.USER_MESSAGE,
            ai_message=self.AI_MESSAGE,
        )
        message.save()
        self.message = message

        # token 얻기
        response = self.client.post(
            self.LOGIN_URL,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        token = response.json()["token"]
        self.token = token

    def test_conversation_not_found(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get(self.URL + "2/")
        self.assertEqual(response.status_code, 404)

    def test_get_messages_in_conversation(self):

        # 로그인하지 않은 상태에서 get
        response = self.client.get(self.URL + "1/")
        self.assertEqual(
            response.status_code,
            403,
        )

        # 대화를 다른 유저가 접근하는 경우 에러 띄우기
        self.client.force_login(
            self.diff_user,
        )
        response = self.client.get(self.URL + "1/")
        self.assertEqual(
            response.status_code,
            403,
        )
        self.client.logout()

        # 여기서부터 로그인하고 테스트 진행
        # 로그인 후 get
        response = self.client.get(
            self.URL + "1/",
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        # print(data)
        # [{'user_message': 'test user message', 'ai_message': 'test ai message'}]

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["user_message"],
            self.USER_MESSAGE,
        )
        self.assertEqual(
            data[0]["ai_message"],
            self.AI_MESSAGE,
        )

    def test_post_messages_in_conversation(self):
        # 로그인하지 않은 상태에서 post
        response = self.client.post(self.URL + "1/")
        self.assertEqual(
            response.status_code,
            403,
        )

        # 대화를 다른 유저가 접근하는 경우 에러 띄우기
        self.client.force_login(
            self.diff_user,
        )
        response = self.client.post(self.URL + "1/")
        self.assertEqual(
            response.status_code,
            403,
        )
        self.client.logout()

        # 여기서부터 로그인하고 테스트 진행
        # 로그인 후 아무 데이터 없이 post
        response = self.client.post(
            self.URL + "1/",
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # user_message만 주는 경우
        test_user_message = "test user message post"
        response = self.client.post(
            self.URL + "1/",
            headers={
                "jwt": self.token,
            },
            data={
                "user_message": test_user_message,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # ai_message만 주는 경우
        test_ai_message = "test ai message post"
        response = self.client.post(
            self.URL + "1/",
            headers={
                "jwt": self.token,
            },
            data={
                "ai_message": test_ai_message,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        #  user_message, ai_message 다 주는 경우
        response = self.client.post(
            self.URL + "1/",
            headers={
                "jwt": self.token,
            },
            data={
                "user_message": test_user_message,
                "ai_message": test_ai_message,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        # print(data)
        # {'id': 2, 'conversation': 'test_title', 'user_message': 'test user message post', 'ai_message': 'test ai message post'}

        self.assertEqual(
            data["id"],
            2,
        )
        self.assertEqual(
            data["conversation"],
            self.TITLE,
        )
        self.assertEqual(
            data["user_message"],
            test_user_message,
        )
        self.assertEqual(
            data["ai_message"],
            test_ai_message,
        )
