from ninja import Router
from django.http import JsonResponse
from receipts.scraper import NFCeScraper
from receipts.parsers import SimpleParser
import logging

logger = logging.getLogger(__name__)

router = Router()
scraper = NFCeScraper()
parser = SimpleParser()


@router.get("/teste", response={200: dict, 400: dict})
def teste_scraper(request, success: bool = True):
    if success:
        return 200, {'success': True}
    return 400, {'error': True, 'message': 'Erro ao acessar a page de teste'}