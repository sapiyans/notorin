from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from core.models import AuditLog
from .audit_utils import *
from .context import get_current_user, get_current_ip

def registrar_auditoria(instance, acao, old_data=None, new_data=None):
    if instance.__class__.__name__ not in MODELOS_AUDITADOS:
        return
    
    user = get_current_user()
    
    space = None
    if hasattr(instance, 'space'):
        space = instance.space
    elif hasattr(instance, 'spaces') and instance.spaces.exists():
        space = instance.spaces.first()
    
    old_data_json = preparar_dados_para_json(old_data or {})
    new_data_json = preparar_dados_para_json(new_data or {})
    
    if acao == 'UPDATE' and old_data_json == new_data_json:
        return
    
    AuditLog.objects.create(
        user=user,
        action=acao,
        model_name=instance.__class__.__name__,
        object_id=instance.pk,
        object_repr=get_object_repr(instance),
        old_data=old_data_json,
        new_data=new_data_json,
        space=space,
        ip=get_current_ip(),
    )


@receiver(pre_save)
def capturar_estado_anterior(sender, instance, **kwargs):
    nome_modelo = instance.__class__.__name__
    
    if nome_modelo not in MODELOS_AUDITADOS:
        return
    
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._old_data = extrair_dados_do_model(old)
        except sender.DoesNotExist:
            instance._old_data = None


@receiver(post_save)
def registrar_pos_save(sender, instance, created, **kwargs):
    nome_modelo = instance.__class__.__name__
    
    if nome_modelo not in MODELOS_AUDITADOS:
        return
    
    if created:
        novos_dados = extrair_dados_do_model(instance)
        registrar_auditoria(
            instance=instance,
            acao='CREATE',
            new_data=novos_dados
        )
    else:
        novos_dados = extrair_dados_do_model(instance)
        old_data = getattr(instance, '_old_data', {})
        
        if detectar_soft_delete(instance):
            registrar_auditoria(
                instance=instance,
                acao='SOFT_DELETE',
                old_data=old_data,
                new_data=novos_dados
            )
        else:
            registrar_auditoria(
                instance=instance,
                acao='UPDATE',
                old_data=old_data,
                new_data=novos_dados
            )


@receiver(post_delete)
def registrar_delete(sender, instance, **kwargs):
    nome_modelo = instance.__class__.__name__
    
    if nome_modelo not in MODELOS_AUDITADOS:
        return
    
    dados = extrair_dados_do_model(instance)
    
    registrar_auditoria(
        instance=instance,
        acao='DELETE',
        old_data=dados
    )