from django.db import models

class Invitation(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    email = models.EmailField(blank=True, default='')
    description = models.TextField(max_length=500)
    createdate = models.DateTimeField(auto_now_add=True)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    def __str__(self):
        return f'Invitation from {self.author.username} to {self.email}'
