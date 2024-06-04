import csv
import os
from myApp1.models import BankInterest
from django.conf import settings

def run():
    csv_path = os.path.join(settings.BASE_DIR, 'csv', 'bank_interest.csv')
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            BankInterest.objects.create(
                bank_name=row['Bank Name'],
                savings_rate=float(row['Savings Rate'].strip('%')),
                fixed_rate=float(row['Fixed Rate'].strip('%'))
            )
