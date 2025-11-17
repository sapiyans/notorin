# receipts/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class NFCeScraper:
    BASE_URL = "https://www.nfce.fazenda.sp.gov.br"
    BASE_PATH = "/NFCeConsultaPublica/Paginas"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_html(self, qrcode_url):
        response = self.session.get(qrcode_url)
        
        if response.status_code != 200:
            return f"Erro {response.status_code}: {response.text}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        btn_abas = soup.find('input', {'value': 'Visualizar em Abas'}) or \
                   soup.find('input', {'value': 'Visualizar&#32;em&#32;Abas'})
        
        if btn_abas:
            html = self._get_full_page_html(soup)
        else:
            html = response.text
        
        return html
    
    def _get_full_page_html(self, soup):
        form = soup.find('form', {'method': 'post'})
        action = form.get('action', '')
        
        if action.startswith('/'):
            full_url = self.BASE_URL + action
        else:
            full_url = f"{self.BASE_URL}{self.BASE_PATH}/{action}"
        
        form_data = {}
        for input_tag in form.find_all('input', type='hidden'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            form_data[name] = value
        
        form_data['__EVENTTARGET'] = 'btnVisualizarAbas'
        form_data['__EVENTARGUMENT'] = ''
        response = self.session.post(full_url, data=form_data)

        if response.status_code == 200:
            return response.text
        else:
            return f"Erro no POST: {response.status_code}\n{response.text}"