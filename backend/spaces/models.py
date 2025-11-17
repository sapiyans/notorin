from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class Space(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class SpaceMember(BaseModel):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="memberships"
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["space", "user"],
                name="unique_space_user"
            )
        ]

