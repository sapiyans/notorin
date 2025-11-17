from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from spaces.models import Space


class Store(BaseModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='stores')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    cnpj = models.CharField(max_length=18, db_index=True, blank=True , null=True)
    nome = models.CharField(max_length=255, blank=True , null=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True , null=True)
    telefone = models.CharField(max_length=20, blank=True , null=True)
    
    endereco = models.CharField(max_length=255, blank=True , null=True)
    bairro = models.CharField(max_length=100, blank=True , null=True)
    cep = models.CharField(max_length=10, blank=True , null=True)
    municipio = models.CharField(max_length=100, blank=True , null=True)
    uf = models.CharField(max_length=2, blank=True , null=True)
    pais = models.CharField(max_length=100, blank=True , null=True)
    
    class Meta:
        ordering = ['nome', 'municipio']
    
    def __str__(self):
        if self.municipio:
            return f"{self.nome} - {self.municipio}/{self.uf}"
        return self.nome or "Loja sem nome"
    
    @classmethod
    def find_or_create_from_emitente(cls, space, emitente):
        cnpj = emitente.get('cnpj', '').strip()
        
        if cnpj:
            store = cls.objects.filter(space=space, cnpj=cnpj).first()
            if store:
                return store, False
        
        nome = emitente.get('nome', '').strip()
        ie = emitente.get('inscricao_estadual', '').strip()
        telefone = emitente.get('telefone', '').strip()
        
        end = emitente.get('endereco', {})
        endereco = end.get('endereco', '').strip()
        bairro = end.get('bairro', '').strip()
        cep = end.get('cep', '').strip()
        municipio = end.get('municipio', '').strip()
        uf = end.get('uf', '').strip()
        pais = end.get('pais', '').strip()
        
        store = cls.objects.create(
            space=space,
            cnpj=cnpj,
            nome=nome,
            inscricao_estadual=ie,
            telefone=telefone,
            endereco=endereco,
            bairro=bairro,
            cep=cep,
            municipio=municipio,
            uf=uf,
            pais=pais
        )
        return store, True


class Receipt(BaseModel):
    url= models.URLField(max_length=500, unique=True, blank=True, null=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='receipts')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    
    serie = models.CharField(max_length=10, blank=True , null=True)
    numero = models.CharField(max_length=20, blank=True , null=True)
    data_emissao = models.DateTimeField(blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    emitente_nome = models.CharField(max_length=255, blank=True , null=True)
    emitente_cnpj = models.CharField(max_length=18, blank=True , null=True)
    emitente_endereco = models.CharField(max_length=255, blank=True , null=True)
    emitente_municipio = models.CharField(max_length=100, blank=True , null=True)
    emitente_uf = models.CharField(max_length=2, blank=True , null=True)
    
    destinatario_nome = models.CharField(max_length=255, blank=True , null=True)
    destinatario_cnpj = models.CharField(max_length=18, blank=True , null=True)
    destinatario_cpf = models.CharField(max_length=14, blank=True , null=True)
    
    valor_total_produtos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_total_descontos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_pis = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_cofins = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_aproximado_tributos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    meio_pagamento = models.CharField(max_length=50, blank=True , null=True)
    valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ['-data_emissao']
    
    def __str__(self):
        return f"{self.serie} {self.numero} - R$ {self.valor_total}" if self.valor_total else f"{self.serie} {self.numero}"


class ReceiptItem(BaseModel):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='itens')
    
    numero = models.CharField(max_length=10, blank=True , null=True)
    descricao = models.CharField(max_length=255, blank=True , null=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    unidade_comercial = models.CharField(max_length=10, blank=True , null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cfop = models.CharField(max_length=4, blank=True , null=True)
    valor_aproximado_tributos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ['numero']
    
    def __str__(self):
        return self.descricao or f"Item {self.numero}"