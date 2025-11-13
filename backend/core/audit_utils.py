import decimal
from datetime import datetime, date


MODELOS_AUDITADOS = [
    'Space',
    'SpaceMember',
    'Receipt',
    'ReceiptItem',
    'Category',
]

CAMPOS_IGNORADOS = [
    'created_at',
    'updated_at',
    'password',
    'last_login',
    'extra_data',
]

CAMPOS_SOFT_DELETE = ['is_active', 'ativo', 'status']


def preparar_dados_para_json(dados):
    """
    Converte dados para formatos JSON-friendly.
    Simples e direto.
    """
    if dados is None:
        return {}
    
    resultado = {}
    
    for chave, valor in dados.items():
        if chave in CAMPOS_IGNORADOS:
            continue
            
        if isinstance(valor, decimal.Decimal):
            resultado[chave] = float(valor)
        
        elif isinstance(valor, (datetime, date)):
            resultado[chave] = valor.isoformat()
        
        elif hasattr(valor, 'pk'):
            resultado[chave] = valor.pk
        
        elif not isinstance(valor, (str, int, float, bool, list, dict)):
            resultado[chave] = str(valor)
        
        else:
            resultado[chave] = valor
    
    return resultado


def extrair_dados_do_model(instance):
    """
    Pega todos os campos de uma instância.
    """
    dados = {}
    
    for field in instance._meta.fields:
        nome = field.name
        valor = getattr(instance, nome)
        dados[nome] = valor
    
    return dados


def detectar_soft_delete(instance):
    """
    Verifica se o objeto foi "deletado" (is_active = False)
    """
    for campo in CAMPOS_SOFT_DELETE:
        if hasattr(instance, campo):
            valor = getattr(instance, campo)
            if valor is False:
                return True
    return False


def get_object_repr(instance):
    """
    Gera uma representação legível do objeto.
    """
    if hasattr(instance, 'name') and instance.name:
        return f"{instance.__class__.__name__}: {instance.name}"
    
    if hasattr(instance, 'store_name') and instance.store_name:
        return f"Nota: {instance.store_name}"
    
    return f"{instance.__class__.__name__} #{instance.pk}"