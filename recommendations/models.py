from django.db import models
from profiles.models import Profile
from experiences.models import Experience
from relationships.models import Relationship


class Recommendation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='recommendations_sent')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name='recommendations_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    related_experience = models.ForeignKey(Experience,
                                           on_delete=models.CASCADE,
                                           related_name='recommendations')
    relation = models.ForeignKey(Relationship, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile}: recommends {self.receiver}"
