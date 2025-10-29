from django.db import models

CATEGORY_CHOICES = [
        ('I rent', 'I rent'),
        ('I am looking for', 'I am looking for'),
    ]

class Announcement(models.Model):

    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500, blank=True, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
