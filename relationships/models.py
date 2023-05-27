from django.db import models


class Relationship(models.Model):
    name = models.CharField(max_length=250)
    archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"
