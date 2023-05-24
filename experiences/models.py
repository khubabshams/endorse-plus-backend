from django.db import models
from profiles.models import Profile


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #  TODO: make company model add to __str__
    location = models.CharField(max_length=100, blank=True)
    date_from = models.DateField()
    date_to = models.DateField(default=None, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        date_to = not self.is_current and f'{self.date_to}' or 'now'
        return f"{self.owner}: {self.title} at company from {self.date_from} until {date_to}"
