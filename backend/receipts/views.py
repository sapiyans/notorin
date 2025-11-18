from ninja import Router
from ninja_extra.security import django_auth
from .scraper import NFCeScraper
from .parsers import SimpleParser
from django.http import JsonResponse
from .models import Receipt, ReceiptItem, Store
from spaces.models import Space, SpaceMember
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = Router()
scraper = NFCeScraper()
parser = SimpleParser()

@router.get("/salvar", auth=django_auth)
def salvar_nota(request, url: str):
    try:
        # Primeiro, verifica se a nota já existe pela URL
        existing_receipt = Receipt.objects.filter(url=url).first()
        
        if existing_receipt:
            return JsonResponse({
                'status': 'aviso',
                'mensagem': 'Esta nota fiscal já foi salva anteriormente',
                'receipt_id': existing_receipt.id,
                'data_criacao': existing_receipt.created_at,
                'ja_existente': True
            })
        
        html = scraper.get_html(url)
        dados = parser.parse(html)
        
        # Busca o SpaceMember ativo do usuário
        space_member = SpaceMember.objects.filter(
            user=request.user,
            is_active=True
        ).select_related('space').first()
        
        if space_member:
            space = space_member.space
        else:
            # Cria novo espaço se não existir
            space = Space.objects.create(
                name=f"Espaço do {request.user.username}",
                is_active=True
            )
            SpaceMember.objects.create(
                space=space,
                user=request.user,
                role='admin',
                is_active=True
            )
        
        emitente = dados.get('emitente', {})
        destinatario = dados.get('destinatario', {})
        totais = dados.get('totais', {})
        pagamento = dados.get('pagamento', {})
        itens = dados.get('itens', [])  # Agora é uma lista, não dicionário
        
        store, store_created = Store.find_or_create_from_emitente(space, emitente)
        
        data_emissao = None
        if dados.get('data_emissao'):
            try:
                data_emissao = datetime.strptime(dados['data_emissao'], '%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        emitente_end = emitente.get('endereco', {})
        emitente_endereco_completo = emitente_end.get('endereco', '')
        emitente_municipio = emitente_end.get('municipio', '')
        if emitente_municipio and ' - ' in emitente_municipio:
            emitente_municipio = emitente_municipio.split(' - ')[1]
        
        # Usando get_or_create com a URL como identificador único
        receipt, created = Receipt.objects.get_or_create(
            url=url,  # Campo único para identificar a nota
            defaults={
                'space': space,
                'user': request.user,
                'store': store,
                'serie': dados.get('serie', ''),
                'numero': dados.get('numero', ''),
                'data_emissao': data_emissao,
                'valor_total': dados.get('valor_total'),
                'emitente_nome': emitente.get('nome', ''),
                'emitente_cnpj': emitente.get('cnpj', ''),
                'emitente_endereco': emitente_endereco_completo,
                'emitente_municipio': emitente_municipio,
                'emitente_uf': emitente_end.get('uf', ''),
                'destinatario_nome': destinatario.get('nome', ''),
                'destinatario_cnpj': destinatario.get('cnpj', ''),
                'destinatario_cpf': destinatario.get('cpf', ''),
                'valor_total_produtos': totais.get('valor_total_produtos'),
                'valor_total_descontos': totais.get('valor_total_descontos'),
                'valor_pis': totais.get('valor_pis'),
                'valor_cofins': totais.get('valor_cofins'),
                'valor_aproximado_tributos': totais.get('valor_aproximado_tributos'),
                'meio_pagamento': pagamento.get('meio_pagamento', ''),
                'valor_pagamento': pagamento.get('valor_pagamento')
            }
        )
        
        # Se a nota já existia (não foi criada agora)
        if not created:
            return JsonResponse({
                'status': 'aviso',
                'mensagem': 'Esta nota fiscal já foi salva anteriormente',
                'receipt_id': receipt.id,
                'data_criacao': receipt.created_at,
                'ja_existente': True
            })
        
        # Só cria os itens se a nota foi criada agora
        if itens and isinstance(itens, list):
            for item in itens:
                ReceiptItem.objects.create(
                    receipt=receipt,
                    numero=item.get('numero', ''),
                    descricao=item.get('descricao', ''),
                    quantidade=item.get('quantidade'),
                    unidade_comercial=item.get('unidade_comercial', ''),
                    valor=item.get('valor'),
                    cfop=item.get('cfop', ''),
                    valor_aproximado_tributos=item.get('valor_aproximado_tributos')
                )
        elif itens and isinstance(itens, dict):
            # Fallback para compatibilidade com versão antiga (dicionário único)
            ReceiptItem.objects.create(
                receipt=receipt,
                numero=itens.get('numero', ''),
                descricao=itens.get('descricao', ''),
                quantidade=itens.get('quantidade'),
                unidade_comercial=itens.get('unidade_comercial', ''),
                valor=itens.get('valor'),
                cfop=itens.get('cfop', ''),
                valor_aproximado_tributos=itens.get('valor_aproximado_tributos')
            )
        
        return JsonResponse({
            'status': 'ok',
            'mensagem': 'Nota salva com sucesso',
            'receipt_id': receipt.id,
            'store_criada': store_created,
            'itens_criados': len(itens) if isinstance(itens, list) else 1
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar nota: {str(e)}")
        return JsonResponse({
            'status': 'erro',
            'erro': str(e)
        })