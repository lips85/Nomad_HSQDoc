from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.constant.constant import AI_MODEL, AI_PRICING_PER_MILLION_TOKENS


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        default="",
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        default="",
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default="",
    )
    openai_api_key = models.CharField(
        max_length=200,
        blank=True,
    )
    claude_api_key = models.CharField(
        max_length=200,
        blank=True,
    )

    def total_conversations(self):
        total_conversations = []

        conversations = self.conversations.all()
        for conversation in conversations:
            title = conversation.title
            messages = conversation.messages.all()
            total_messages = messages.count()
            file_name = conversation.file_name
            openai_total_tokens = 0
            openai_total_cost = 0
            claude_total_tokens = 0
            claude_total_cost = 0
            for message in messages:
                if message.model == AI_MODEL[1]:
                    openai_total_tokens += message.token
                    openai_total_cost += (
                        AI_PRICING_PER_MILLION_TOKENS[AI_MODEL[1]] * openai_total_tokens
                    )
                else:
                    claude_total_tokens += message.token
                    claude_total_cost += (
                        AI_PRICING_PER_MILLION_TOKENS[AI_MODEL[2]] * claude_total_tokens
                    )
            total_tokens = openai_total_tokens + claude_total_tokens
            total_cost = openai_total_cost + claude_total_cost
            total_conversations.append(
                {
                    "title": title,
                    "total_messages": total_messages,
                    "total_tokens": total_tokens,
                    "total_cost_per_1M_tokens": total_cost,
                    "file_name": file_name,
                    "models": {
                        "openai": {
                            "tokens": openai_total_tokens,
                            "cost_per_1M_tokens": openai_total_cost,
                        },
                        "claude": {
                            "tokens": claude_total_tokens,
                            "cost_per_1M_tokens": claude_total_cost,
                        },
                    },
                }
            )

        return total_conversations

    def total_messages(self):
        total_messages = 0

        conversations = self.conversations.all()
        for conversation in conversations:
            total_messages += conversation.messages.all().count()

        return total_messages

    def total_tokens(self):
        total_tokens = 0
        total_tokens_openai = 0
        total_tokens_claude = 0

        total_conversations = self.total_conversations()
        for conversation in total_conversations:
            total_tokens += conversation["total_tokens"]
            total_tokens_openai += conversation["models"]["openai"]["tokens"]
            total_tokens_claude += conversation["models"]["claude"]["tokens"]

        user_total_tokens = {
            "total_tokens": total_tokens,
            "total_tokens_openai": total_tokens_openai,
            "total_tokens_claude": total_tokens_claude,
        }
        return user_total_tokens

    def total_cost(self):
        total_cost = 0
        total_cost_openai = 0
        total_cost_claude = 0

        total_conversations = self.total_conversations()
        for conversation in total_conversations:
            total_cost += conversation["total_cost_per_1M_tokens"]
            total_cost_openai += conversation["models"]["openai"]["cost_per_1M_tokens"]
            total_cost_claude += conversation["models"]["claude"]["cost_per_1M_tokens"]

        user_total_cost = {
            "total_cost_per_1M_tokens": total_cost,
            "total_cost_openai_per_1M_tokens": total_cost_openai,
            "total_cost_claude_per_1M_tokens": total_cost_claude,
        }
        return user_total_cost

    def total_files(self):
        total_files = []

        conversations = self.conversations.all()
        for conversation in conversations:
            file_name = conversation.file_name
            if (file_name != "") and (file_name not in total_files):
                total_files.append(file_name)

        return total_files
