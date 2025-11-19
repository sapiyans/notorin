from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class SocialAccount(BaseModel):
    class Provider(models.TextChoices):
        FACEBOOK = 'fb', 'Facebook'
        GOOGLE = 'go', 'Google'
        APPLE = 'ap', 'Apple'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='social_accounts'
    )

    provider = models.CharField(max_length=2, choices=Provider.choices)
    provider_id = models.CharField(max_length=255, db_index=True)

    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    extra_data = models.JSONField(default=dict, blank=True)


    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def __str__(self):
        return f"{self.user} ({self.get_provider_display()})"

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['provider', 'provider_id'],
                name='unique_provider_account'
            ),
            models.UniqueConstraint(
                fields=['user', 'provider'],
                name='unique_user_provider'
            )
        ]