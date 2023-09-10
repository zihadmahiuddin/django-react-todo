from django.contrib.auth.models import User
from django.db import models


class TodoItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    content = models.CharField(max_length=200)

    def __str__(self) -> str:
        prefix = "[x]" if self.done else "[ ]"
        return f"{prefix} {self.content}"
