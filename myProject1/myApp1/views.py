from django.shortcuts import render
import csv
import os
from django.conf import settings
from .models import BankInterest

def home(request):
    # Read bank names from the CSV file
    csv_path = os.path.join(settings.BASE_DIR, 'csv', 'bank_interest.csv')
    bank_names = []
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            bank_names.append(row['Bank Name'])  
    
    if request.method == "POST":
        bank_name = request.POST['bank_name']
        amount = float(request.POST['amount'])
        account_type = request.POST['account_type']
        
        bank_interest = BankInterest.objects.filter(bank_name=bank_name).first()
        if bank_interest:
            rate = bank_interest.savings_rate if account_type == 'savings' else bank_interest.fixed_rate
            interest_amount = amount * rate / 100
        else:
            interest_amount = None
        
        context = {
            'bank_name': bank_name,
            'amount': amount,
            'account_type': account_type,
            'interest_amount': interest_amount,
            'bank_names': bank_names,
        }
        return render(request, 'dashboard.html', context)
    
    return render(request, 'home.html', {'bank_names': bank_names})
def show(request):
    csv_path = os.path.join(settings.BASE_DIR, 'csv', 'bank_interest.csv')

    if request.method == 'POST':
        bank_name = request.POST['bank_name']
        amount = float(request.POST['amount'])
        account_type = request.POST['account_type']

        with open(csv_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['Bank Name'] == bank_name:  
                    savings_rate_str = row['Savings Rate'].strip('%')
                    fixed_rate_str = row['Fixed Rate'].strip('%')
                    
                    try:
                        savings_rate = float(savings_rate_str) if savings_rate_str != '--' else 0.0
                        fixed_rate = float(fixed_rate_str) if fixed_rate_str != '--' else 0.0
                    except ValueError:
                        savings_rate = 0.0
                        fixed_rate = 0.0
                    
                    if account_type == 'savings':
                        interest = amount * savings_rate / 100
                        result = f'Savings Interest for {amount} रु in {bank_name} is रु {interest:,.2f}'
                    else:
                        interest = amount * fixed_rate / 100
                        result = f'Fixed Interest for {amount} रु in {bank_name} is रु {interest:,.2f}'

    return render(request, 'dashboard.html', {'result': result})
