from django.db import models

class BankInterest(models.Model):
    bank_name = models.CharField(max_length=100)
    savings_rate = models.DecimalField(max_digits=5, decimal_places=2)
    fixed_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.bank_name
