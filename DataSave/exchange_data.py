import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finence_service.settings')
django.setup()

def dollar_rate():
    print("환율정보를 저장합니다")

def dollar_index():
    print("달러인덱스를 저장합니다")