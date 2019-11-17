from django.db import models

from itertools import product
import pandas as pd


def address_state_choices():
    df = pd.read_csv('./pipeline/states_lookup.csv').set_index('Abbreviation')
    df = df.to_dict()['State']
    return tuple(df.items())

def home_ownership_choices():
    a = ('MORTGAGE', 'RENT', 'OWN', 'OTHER')
    return tuple(zip(a, a))

def grade_choices():
    a = tuple(product(list('ABCDEFG'), range(1, 6)))
    b = tuple(map(lambda x: x[0] + str(x[1]), a))
    return tuple(zip(b, b))

def status_choices():
    return (('PAID', 'paid'),
            ('CURRENT', 'current'),
            ('CHARGED_OFF', 'charged off'),
            ('LATE1', 'late up to 60 weeks'),
            ('LATE2', 'late beyond 60 weeks'),
            ('GRACE', 'in grace period'),
            ('DEFAULT', 'default'))

def term_choices():
    return (('36', '36 months'), ('60', '60 months'))



class Loans(models.Model):
    id              = models.AutoField(primary_key=True)
    member_id       = models.ForeignKey("Borrowers", on_delete=models.CASCADE)
    title           = models.CharField(max_length=256, blank=True)
    funded_amount   = models.FloatField()
    total_payments  = models.FloatField()
    grade           = models.CharField(choices=grade_choices(), max_length=2)
    interest_rate   = models.FloatField()
    amount          = models.FloatField()
    status          = models.CharField(choices=status_choices(), default='DEFAULT', max_length=12)
    meets_policy    = models.BooleanField(default=True)
    term            = models.CharField(choices=term_choices(), default='30', max_length=2)

    class Meta:
        db_table = 'Loans'


class Borrowers(models.Model):
    member_id       = models.AutoField(primary_key=True)
    all_util        = models.FloatField(default=0.0)
    annual_income   = models.FloatField(default=0.0)
    avg_cur_bal     = models.FloatField()
    dti             = models.FloatField()
    home_ownership  = models.CharField(
                    choices=home_ownership_choices(),
                    default='OTHER', 
                    max_length=8)
    address_state   = models.CharField(
                    choices=address_state_choices(), 
                    default='', 
                    max_length=2)
    zip_code        = models.CharField(max_length=3)
    emp_title       = models.CharField(max_length=256)
    emp_length      = models.IntegerField(default=0)

    class Meta:
        db_table = 'Borrowers'

