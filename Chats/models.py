# from django.contrib.auth.models import User
from users.models import User
from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=True, related_name="sender_message_set")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_delete = models.BooleanField(default=False)
    receiver_delete = models.BooleanField(default=False)


class BlockedUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blocking_users')
    blocked_users = models.ManyToManyField(User, related_name='blocked_by')



    def block_user(self, user_to_block):
        if user_to_block != self.user:  # Ensure user is not blocking themselves
            self.blocked_users.add(user_to_block)
            return True
        return False

    def unblock_user(self, user_to_unblock):
        self.blocked_users.remove(user_to_unblock)

    def get_blocked_users(self):
        return self.blocked_users.all()

    def __str__(self):
        return f"{self.user.username} - Blocked Users: {', '.join([user.username for user in self.blocked_users.all()])}"
