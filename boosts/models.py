from django.db import models
from profiles.models import Profile
from recommendations.models import Recommendation


class Boost(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='boosts')
    recommendation = models.ForeignKey(Recommendation,
                                       on_delete=models.CASCADE,
                                       related_name='boosts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['profile', 'recommendation']

    def __str__(self):
        return f"{self.profile} Boosted {self.recommendation}"
