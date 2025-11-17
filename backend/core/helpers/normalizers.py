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

def normalize_quantity(valor: Union[str, float, int]) -> Optional[float]:
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

def normalize_date(data_str: str, output_format: str = '%Y-%m-%d') -> Optional[str]:
    if not data_str:
        return None
    
    patterns = [
        (r'(\d{2})/(\d{2})/(\d{4})\s+(\d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),
        (r'(\d{2})/(\d{2})/(\d{4})', '%Y-%m-%d'),
        (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
    ]
    
    for pattern, _ in patterns:
        match = re.search(pattern, data_str)
        if match:
            if len(match.groups()) == 4:
                dia, mes, ano, hora = match.groups()
                try:
                    data_obj = datetime(int(ano), int(mes), int(dia))
                    return f"{data_obj.strftime(output_format)} {hora}"
                except:
                    return data_str
            elif len(match.groups()) == 3:
                dia, mes, ano = match.groups()
                try:
                    data_obj = datetime(int(ano), int(mes), int(dia))
                    return data_obj.strftime(output_format)
                except:
                    return data_str
    
    return data_str

def normalize_email(email: str) -> Optional[str]:
    if not email:
        return None
    email = email.lower().strip()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return email
    return None

def normalize_uf(uf: str) -> Optional[str]:
    if not uf:
        return None
    uf = uf.upper().strip()
    ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                   'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                   'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    if uf in ufs_validas:
        return uf
    return None

def safe_convert(value: Any, convert_func, default: Any = None) -> Any:
    try:
        result = convert_func(value)
        if result is None:
            return default
        return result
    except:
        return default