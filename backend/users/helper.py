import re
from django.contrib.auth.models import User

def create_username(email):
    try:
        username = re.split(r'[@\s]', email)[0] 
    except:
        username = email
    number = 1
    original_user = username
    while User.objects.filter(username=username).exists():
        username = f"{original_user}{number}"
        number += 1

    return username
