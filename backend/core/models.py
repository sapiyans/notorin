from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        abstract = True



class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Criação'),
        ('UPDATE', 'Edição'),
        ('DELETE', 'Exclusão'),
        ('SOFT_DELETE', 'Exclusão Lógica'),
        ('VIEW', 'Visualização'),
        ('LOGIN', 'Login'),
        ('INVITE', 'Convite'),
        ('JOIN', 'Entrada'),
        ('LEAVE', 'Saída'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200, blank=True)
    
    old_data = models.JSONField(default=dict, blank=True)
    new_data = models.JSONField(default=dict, blank=True)
    
    space = models.ForeignKey(
        'spaces.Space',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    ip = models.GenericIPAddressField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['space', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.created_at} - {self.user} - {self.action} - {self.model_name}"
  