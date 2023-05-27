from django.db import models
from profiles.models import Profile


class Request(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='requests_sent')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name='requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['profile', 'receiver']

    def __str__(self):
        return f"Request from {self.profile} to {self.receiver}"
