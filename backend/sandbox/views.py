from ninja import Router
from django.http import JsonResponse
from receipts.scraper import NFCeScraper
from receipts.parsers import SimpleParser
import logging

logger = logging.getLogger(__name__)

router = Router()
scraper = NFCeScraper()
parser = SimpleParser()


@router.get("/teste")
def teste_scraper(request, url: str):
    try:
        html = scraper.get_html(url)
        dados = parser.parse(html)
        
        return JsonResponse({
            'status': 'ok',
            'dados': dados
        })
        
    except Exception as e:
        logger.error(f"Erro no teste_scraper: {str(e)}")
        return JsonResponse({
            'status': 'erro',
            'erro': str(e)
        })