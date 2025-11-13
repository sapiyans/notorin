import re
import unicodedata
from datetime import datetime
from typing import Optional, Union, Any

def normalize_text(texto: str) -> Optional[str]:
    if not texto:
        return texto
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def clean_text(texto: str) -> Optional[str]:
    if not texto:
        return texto
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def only_numbers(valor: Union[str, int, float]) -> Optional[str]:
    if not valor:
        return None
    return re.sub(r'\D', '', str(valor))

def normalize_currency(valor: Union[str, float, int]) -> Optional[float]:
    if not valor:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    valor = str(valor).replace('.', '').replace(',', '.')
    numeros = re.findall(r'[\d,\.]+', valor)
    if numeros:
        valor_limpo = numeros[0].replace(',', '')
        if '.' in valor_limpo and valor_limpo.count('.') > 1:
            partes = valor_limpo.split('.')
            valor_limpo = ''.join(partes[:-1]) + '.' + partes[-1]
        try:
            return float(valor_limpo)
        except:
            return None
    return None

