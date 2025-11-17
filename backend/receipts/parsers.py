from bs4 import BeautifulSoup
from core.helpers.normalizers import (
    normalize_text, clean_text, normalize_currency,
    normalize_quantity, normalize_date, only_numbers,
    normalize_email, normalize_uf, safe_convert
)

class SimpleParser:
    TAB_CONFIGS = {
        'Conteudo_pnlNFe': {
            'tipo': 'principal',
            'campos': {
                'serie': {'label': 'serie', 'normalize': None},
                'numero': {'label': 'numero', 'normalize': None},
                'data_emissao': {'label': 'data', 'normalize': 'date'},
                'valor_total': {'label': 'valor total', 'normalize': 'currency'},
                'inscricao_estadual': {'label': 'inscricao estadual', 'normalize': 'only_numbers'},
                'cnpj': {'label': 'cnpj', 'normalize': 'only_numbers'},
            }
        },
        'Conteudo_pnlNFe_tabEmitente': {
            'tipo': 'emitente',
            'campos': {
                'nome': {'label': 'nome', 'normalize': None},
                'cnpj': {'label': 'cnpj', 'normalize': 'only_numbers'},
                'inscricao_estadual': {'label': 'inscricao estadual', 'normalize': 'only_numbers'},
                'telefone': {'label': 'telefone', 'normalize': 'only_numbers'},
            },
            'endereco': {
                'endereco': {'label': 'endereco', 'normalize': None},
                'bairro': {'label': 'bairro', 'normalize': None},
                'cep': {'label': 'cep', 'normalize': 'only_numbers'},
                'municipio': {'label': 'municipio', 'normalize': None},
                'uf': {'label': 'uf', 'normalize': 'uf'},
                'pais': {'label': 'pais', 'normalize': None},
            }
        },
        'Conteudo_pnlNFe_tabNFe': {
            'tipo': 'destinatario',
            'campos': {
                'nome': {'label': 'nome', 'normalize': None},
                'cnpj': {'label': 'cnpj', 'normalize': 'only_numbers'},
                'cpf': {'label': 'cpf', 'normalize': 'only_numbers'},
                'telefone': {'label': 'telefone', 'normalize': 'only_numbers'},
                'email': {'label': 'e-mail', 'normalize': 'email'},
            },
            'endereco': {
                'endereco': {'label': 'endereco', 'normalize': None},
                'bairro': {'label': 'bairro', 'normalize': None},
                'cep': {'label': 'cep', 'normalize': 'only_numbers'},
                'municipio': {'label': 'municipio', 'normalize': None},
                'uf': {'label': 'uf', 'normalize': 'uf'},
                'pais': {'label': 'pais', 'normalize': None},
            }
        },
        'Conteudo_pnlNFe_tabTotais': {
            'tipo': 'totais',
            'campos': {
                'base_calculo_icms': {'label': 'base de calculo icms', 'normalize': 'currency'},
                'valor_icms': {'label': 'valor do icms', 'normalize': 'currency'},
                'valor_total_produtos': {'label': 'valor total dos produtos', 'normalize': 'currency'},
                'valor_total_descontos': {'label': 'valor total dos descontos', 'normalize': 'currency'},
                'valor_pis': {'label': 'valor do pis', 'normalize': 'currency'},
                'valor_cofins': {'label': 'valor da cofins', 'normalize': 'currency'},
                'valor_total_nfe': {'label': 'valor total da nfe', 'normalize': 'currency'},
                'valor_aproximado_tributos': {'label': 'valor aproximado dos tributos', 'normalize': 'currency'},
                'base_calculo_ibs_cbs': {'label': 'base de calculo do ibs e cbs', 'normalize': 'currency'},
                'valor_ibs': {'label': 'valor do ibs', 'normalize': 'currency'},
                'valor_cbs': {'label': 'valor da cbs', 'normalize': 'currency'},
            }
        },
        'Conteudo_pnlNFe_tabCobranca': {
            'tipo': 'pagamento',
            'estrutura': 'complexa'
        }
    }

    @staticmethod
    def _apply_normalization(value, normalize_type):
        if value is None or normalize_type is None:
            return value
        
        normalizers = {
            'currency': normalize_currency,
            'quantity': normalize_quantity,
            'date': normalize_date,
            'only_numbers': only_numbers,
            'email': normalize_email,
            'uf': normalize_uf,
        }
        
        normalizer_func = normalizers.get(normalize_type)
        if normalizer_func:
            return safe_convert(value, normalizer_func)
        return value

    @staticmethod
    def get_span_in_td_by_tab(soup, tab_id, campos_config, silent=False):
        data = {}
        tab = soup.find('div', id=tab_id)
        
        if tab is None:
            if not silent:
                print(f'Aba não encontrada: {tab_id}')
            return data
        
        for key, config in campos_config.items():
            if isinstance(config, dict):
                label = config.get('label', '')
                normalize_type = config.get('normalize')
            else:
                label = config
                normalize_type = None
            
            label_soup = tab.find('label', string=lambda t: t and label in normalize_text(t))
            
            if label_soup is None:
                label_soup = tab.find(
                    lambda tag: tag.name in ['label', 'span', 'div', 'td', 'th']
                    and label in normalize_text(tag.get_text())
                )
            
            if label_soup is None:
                if not silent:
                    print(f'Label não encontrado: {label}')
                data[key] = None
                continue

            td_label = label_soup.find_parent('td')
            if td_label is None:
                valor_elem = label_soup.find_next_sibling()
                if valor_elem is None:
                    valor_elem = label_soup.parent.find_next_sibling()
                
                if valor_elem:
                    valor = valor_elem.get_text(strip=True)
                else:
                    valor = label_soup.get_text(strip=True)
            else:
                valor_span = td_label.find('span')
                if valor_span is None:
                    valor = td_label.get_text(strip=True)
                else:
                    valor = valor_span.get_text(strip=True)
            
            if not valor or valor == '':
                data[key] = None
            else:
                valor_clean = clean_text(valor)
                data[key] = SimpleParser._apply_normalization(valor_clean, normalize_type)
        
        return data

    @staticmethod
    def extract_section_data(soup, tab_id, campos_dict, endereco_dict=None, silent=False):
        data = SimpleParser.get_span_in_td_by_tab(soup, tab_id, campos_dict, silent)
        
        if endereco_dict:
            endereco_data = SimpleParser.get_span_in_td_by_tab(soup, tab_id, endereco_dict, silent)
            if endereco_data and any(endereco_data.values()):
                data['endereco'] = endereco_data
        
        return data

    @staticmethod
    def extract_pagamento(soup, tab_id, silent=False):
        pagamento = {}
        
        tab = soup.find('div', id=tab_id)
        if tab is None:
            if not silent:
                print(f'Aba não encontrada: {tab_id}')
            return pagamento
        
        # Pega a forma de pagamento da tabela toggle
        tabela_pagamento = tab.find('table', class_='toggle')
        if tabela_pagamento:
            linhas = tabela_pagamento.find_all('tr')
            for linha in linhas:
                tds = linha.find_all('td')
                if len(tds) >= 3:
                    indicador = clean_text(tds[0].get_text(strip=True))
                    meio_pagamento = clean_text(tds[1].get_text(strip=True))
                    descricao = clean_text(tds[2].get_text(strip=True))
                    
                    pagamento['indicador_forma_pagamento'] = indicador
                    pagamento['meio_pagamento'] = meio_pagamento
                    pagamento['descricao_meio_pagamento'] = descricao if descricao else None
        
        # Pega todos os detalhes da tabela toggable
        tabela_detalhes = tab.find('table', class_='toggable')
        if tabela_detalhes:
            # Procura por todas as linhas com labels
            todas_linhas = tabela_detalhes.find_all('tr')
            
            for linha in todas_linhas:
                labels = linha.find_all('label')
                spans = linha.find_all('span')
                
                for i, label in enumerate(labels):
                    label_text = normalize_text(label.get_text(strip=True))
                    
                    # Pega o span correspondente
                    if i < len(spans):
                        valor = clean_text(spans[i].get_text(strip=True))
                    else:
                        # Se não tem span na mesma linha, procura o próximo span
                        span_proximo = label.find_next_sibling('span')
                        if span_proximo:
                            valor = clean_text(span_proximo.get_text(strip=True))
                        else:
                            valor = None
                    
                    if valor:
                        # Mapeia os labels para as chaves
                        if 'valor do pagamento' in label_text:
                            pagamento['valor_pagamento'] = normalize_currency(valor)
                        elif 'uf onde o pagamento foi processado' in label_text:
                            pagamento['uf_processamento'] = normalize_uf(valor)
                        elif 'tipo de integração pagamento' in label_text:
                            pagamento['tipo_integracao'] = valor
                        elif 'cnpj da credenciadora' in label_text:
                            pagamento['cnpj_credenciadora'] = only_numbers(valor)
                        elif 'bandeira da operadora' in label_text:
                            pagamento['bandeira_operadora'] = valor
                        elif 'número de autorização' in label_text:
                            pagamento['numero_autorizacao'] = valor
                        elif 'cnpj do beneficiário de pagamento' in label_text:
                            pagamento['cnpj_beneficiario'] = only_numbers(valor)
                        elif 'identificador do terminal de pagamento' in label_text:
                            pagamento['identificador_terminal'] = valor
                        elif 'data do pagamento' in label_text:
                            pagamento['data_pagamento'] = valor
                        elif 'cnpj transacional do pagamento' in label_text:
                            pagamento['cnpj_transacional'] = only_numbers(valor)
                        elif 'troco' in label_text:
                            pagamento['troco'] = normalize_currency(valor) if valor else None
        
        return pagamento

    @staticmethod
    def extract_itens(html, silent=False):
        soup = BeautifulSoup(html, 'html.parser')
        itens = []
        
        container = soup.find('div', id='Prod')
        if container is None:
            if not silent:
                print("Container 'Prod' não encontrado")
            return itens
        
        tabelas = container.find_all('table', class_='toggle')
        
        for i, tabela in enumerate(tabelas):
            try:
                produto = {}
                
                linhas = tabela.find_all('tr')
                for linha in linhas:
                    num_cell = linha.find('td', class_='fixo-prod-serv-numero')
                    if num_cell:
                        span = num_cell.find('span')
                        if span:
                            produto['numero'] = clean_text(span.get_text())
                    
                    desc_cell = linha.find('td', class_='fixo-prod-serv-descricao')
                    if desc_cell:
                        span = desc_cell.find('span')
                        if span:
                            produto['descricao'] = clean_text(span.get_text())
                    
                    qtd_cell = linha.find('td', class_='fixo-prod-serv-qtd')
                    if qtd_cell:
                        span = qtd_cell.find('span')
                        if span:
                            produto['quantidade'] = normalize_quantity(clean_text(span.get_text()))
                    
                    uc_cell = linha.find('td', class_='fixo-prod-serv-uc')
                    if uc_cell:
                        span = uc_cell.find('span')
                        if span:
                            produto['unidade_comercial'] = clean_text(span.get_text())
                    
                    vb_cell = linha.find('td', class_='fixo-prod-serv-vb')
                    if vb_cell:
                        span = vb_cell.find('span')
                        if span:
                            produto['valor'] = normalize_currency(clean_text(span.get_text()))
                
                detalhes_tabela = tabela.find_next_sibling('table', class_='toggable')
                if detalhes_tabela:
                    detalhes = SimpleParser._extract_produto_detalhes(detalhes_tabela, silent)
                    produto.update(detalhes)
                
                if produto:
                    if 'quantidade_comercial' in produto and not isinstance(produto['quantidade_comercial'], (int, float)):
                        produto['quantidade_comercial'] = normalize_quantity(produto['quantidade_comercial'])
                    if 'quantidade_tributavel' in produto and not isinstance(produto['quantidade_tributavel'], (int, float)):
                        produto['quantidade_tributavel'] = normalize_quantity(produto['quantidade_tributavel'])
                    
                    itens.append(produto)
                    
            except Exception as e:
                if not silent:
                    print(f"Erro ao processar produto {i}: {e}")
        
        return itens

    @staticmethod
    def _extract_produto_detalhes(tabela_detalhes, silent=False):
        detalhes = {}
        
        labels = tabela_detalhes.find_all('label')
        
        for label in labels:
            try:
                label_text = normalize_text(label.get_text(strip=True))
                
                valor_elem = label.find_next_sibling('span')
                if valor_elem is None:
                    parent = label.find_parent('td')
                    if parent:
                        valor_elem = parent.find('span')
                
                if valor_elem:
                    valor = clean_text(valor_elem.get_text(strip=True))
                else:
                    next_elem = label.find_next_sibling()
                    if next_elem:
                        valor = clean_text(next_elem.get_text(strip=True))
                    else:
                        continue
                
                chave, normalize_type = SimpleParser._mapear_label_produto(label_text)
                if chave and valor:
                    if normalize_type:
                        valor = SimpleParser._apply_normalization(valor, normalize_type)
                    detalhes[chave] = valor
                    
            except Exception as e:
                if not silent:
                    print(f"Erro ao extrair detalhe do produto: {e}")
        
        detalhes.update(SimpleParser._extract_tributacao(tabela_detalhes, silent))
        
        return detalhes

    @staticmethod
    def _mapear_label_produto(label_text):
        mapeamento = {
            'código do produto': ('codigo_produto', None),
            'código ncm': ('ncm', None),
            'código cest': ('cest', None),
            'cfop': ('cfop', None),
            'código ean comercial': ('ean_comercial', None),
            'código ean tributável': ('ean_tributavel', None),
            'unidade comercial': ('unidade_comercial_detalhe', None),
            'unidade tributável': ('unidade_tributavel', None),
            'quantidade comercial': ('quantidade_comercial', 'quantity'),
            'quantidade tributável': ('quantidade_tributavel', 'quantity'),
            'valor unitário de comercialização': ('valor_unitario_comercial', 'currency'),
            'valor unitário de tributação': ('valor_unitario_tributacao', 'currency'),
            'valor do desconto': ('valor_desconto', 'currency'),
            'valor total do frete': ('valor_frete', 'currency'),
            'valor do seguro': ('valor_seguro', 'currency'),
            'outras despesas acessórias': ('outras_despesas', 'currency'),
            'valor aproximado dos tributos': ('valor_aproximado_tributos', 'currency'),
            'número do pedido de compra': ('pedido_compra_numero', None),
            'item do pedido de compra': ('pedido_compra_item', None),
            'número da fci': ('numero_fci', None),
            'indicador de escala relevante': ('indicador_escala', None),
            'cnpj do fabricante da mercadoria': ('cnpj_fabricante', 'only_numbers'),
            'código de benefício fiscal na uf': ('codigo_beneficio_fiscal', None),
            'código ex da tipi': ('codigo_ex_tipi', None),
        }
        
        for label_key, (chave, normalize_type) in mapeamento.items():
            if label_key in label_text:
                return chave, normalize_type
        
        return None, None

    @staticmethod
    def _extract_tributacao(tabela_detalhes, silent=False):
        tributacao = {}
        
        icms_fieldset = tabela_detalhes.find('fieldset', class_='fieldset-internal')
        while icms_fieldset:
            legend = icms_fieldset.find('legend')
            if legend:
                legend_text = normalize_text(legend.get_text(strip=True))
                
                if 'icms' in legend_text:
                    if 'icms' not in tributacao:
                        tributacao['icms'] = {}
                    labels = icms_fieldset.find_all('label')
                    for label in labels:
                        label_text = normalize_text(label.get_text(strip=True))
                        valor_elem = label.find_next_sibling('span')
                        if valor_elem:
                            valor = clean_text(valor_elem.get_text(strip=True))
                            
                            if 'origem' in label_text:
                                tributacao['icms']['origem'] = valor
                            elif 'tributação' in label_text:
                                tributacao['icms']['tributacao'] = valor
                            elif 'base de cálculo' in label_text:
                                tributacao['icms']['base_calculo'] = normalize_currency(valor)
                            elif 'alíquota' in label_text:
                                tributacao['icms']['aliquota'] = normalize_currency(valor)
                            elif 'valor' in label_text:
                                tributacao['icms']['valor'] = normalize_currency(valor)
                
                elif 'ibscbs' in legend_text:
                    if 'ibs_cbs' not in tributacao:
                        tributacao['ibs_cbs'] = {}
                    labels = icms_fieldset.find_all('label')
                    for label in labels:
                        label_text = normalize_text(label.get_text(strip=True))
                        valor_elem = label.find_next_sibling('span')
                        if valor_elem:
                            valor = clean_text(valor_elem.get_text(strip=True))
                            
                            if 'cst' in label_text:
                                tributacao['ibs_cbs']['cst'] = valor
                            elif 'cclasstrib' in label_text:
                                tributacao['ibs_cbs']['classe_trib'] = valor
                            elif 'valor da bc' in label_text:
                                tributacao['ibs_cbs']['base_calculo'] = normalize_currency(valor)
                            elif 'valor do ibs' in label_text:
                                tributacao['ibs_cbs']['ibs_valor'] = normalize_currency(valor)
                            elif 'valor da cbs' in label_text:
                                tributacao['ibs_cbs']['cbs_valor'] = normalize_currency(valor)
                
                elif 'pis' in legend_text:
                    if 'pis' not in tributacao:
                        tributacao['pis'] = {}
                    labels = icms_fieldset.find_all('label')
                    for label in labels:
                        label_text = normalize_text(label.get_text(strip=True))
                        valor_elem = label.find_next_sibling('span')
                        if valor_elem:
                            valor = clean_text(valor_elem.get_text(strip=True))
                            
                            if 'cst' in label_text:
                                tributacao['pis']['cst'] = valor
                            elif 'base de cálculo' in label_text:
                                tributacao['pis']['base_calculo'] = normalize_currency(valor)
                            elif 'alíquota' in label_text:
                                tributacao['pis']['aliquota'] = normalize_currency(valor)
                            elif 'valor' in label_text:
                                tributacao['pis']['valor'] = normalize_currency(valor)
                
                elif 'cofins' in legend_text:
                    if 'cofins' not in tributacao:
                        tributacao['cofins'] = {}
                    labels = icms_fieldset.find_all('label')
                    for label in labels:
                        label_text = normalize_text(label.get_text(strip=True))
                        valor_elem = label.find_next_sibling('span')
                        if valor_elem:
                            valor = clean_text(valor_elem.get_text(strip=True))
                            
                            if 'cst' in label_text:
                                tributacao['cofins']['cst'] = valor
                            elif 'base de cálculo' in label_text:
                                tributacao['cofins']['base_calculo'] = normalize_currency(valor)
                            elif 'alíquota' in label_text:
                                tributacao['cofins']['aliquota'] = normalize_currency(valor)
                            elif 'valor' in label_text:
                                tributacao['cofins']['valor'] = normalize_currency(valor)
            
            icms_fieldset = icms_fieldset.find_next_sibling('fieldset', class_='fieldset-internal')
        
        return tributacao

    @staticmethod
    def parse(html, silent=False):
        soup = BeautifulSoup(html, 'html.parser')
        result = {}
        
        for tab_id, config in SimpleParser.TAB_CONFIGS.items():
            if config.get('estrutura') == 'complexa':
                tab_data = SimpleParser.extract_pagamento(soup, tab_id, silent)
            else:
                tab_data = SimpleParser.extract_section_data(
                    soup, 
                    tab_id, 
                    config['campos'],
                    config.get('endereco'),
                    silent
                )
            
            tipo = config.get('tipo', 'desconhecido')
            
            if tipo == 'principal':
                result.update(tab_data)
            else:
                result[tipo] = tab_data
        
        itens = SimpleParser.extract_itens(html, silent)
        if itens:
            result['itens'] = itens
        
        return result

    @staticmethod
    def parse_with_custom_configs(html, custom_configs, silent=False):
        original_configs = SimpleParser.TAB_CONFIGS.copy()
        SimpleParser.TAB_CONFIGS.update(custom_configs)
        result = SimpleParser.parse(html, silent)
        SimpleParser.TAB_CONFIGS = original_configs
        return result