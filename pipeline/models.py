from django.db import models

from itertools import product
import pandas as pd


def load_state_codes():
    df = pd.read('states_lookup.csv').set_index('Abbreviation')
    df = df.to_dict()['State']
    return tuple(zip(df.items()))


class Loans(models.Model):
    _ = tuple(product(list('ABCDEFG'), range(1, 6)))
    GRADE_CHOICES = tuple(map(lambda x: x[0] + str(x[1]), _))

    STATUS_CHOICES = ('PAID', 'CURRENT', 'CHARGED_OFF', 'LATE1', 'LATE2', 'GRACE', 'DEFAULT')
    TERM_CHOICES = ((36, '36 months'), (60, '60 months'))

    id              = models.AutoField(primary_key=True)
    member_id       = models.ForeignKey("Borrowers", on_delete=models.CASCADE)
    title           = models.CharField(max_length=256, blank=True)
    funded_amount   = models.FloatField()
    total_payments  = models.FloatField()
    grade           = models.ChoiceField(choices=GRADE_CHOICES)
    interest_rate   = models.FloatField()
    amount          = models.FloatField()
    status          = models.ChoiceField(choices=STATUS_CHOICES, default='DEFAULT')
    meets_policy    = models.BooleanField(default=True)
    term            = models.ChoiceField(choices=TERM_CHOICES, default=30)

    class Meta:
        db_table = 'Loans'


class Borrowers(models.Model):
    HOME_OWNERSHIP_CHOICES = ('MORTGAGE', 'RENT', 'OWN', 'OTHER')
    STATE_CODE_CHOICES = load_state_codes()

    member_id       = models.AutoField(primary_key=True)
    all_util        = models.FloatField(default=0.0)
    annual_income   = models.FloatField(default=0.0)
    avg_cur_bal     = models.FloatField()
    dti             = models.FloatField()
    home_ownership  = models.ChoiceField(choices=HOME_OWNERSHIP_CHOICES, default='OTHER')
    address_state   = models.ChoiceField(choices=STATE_CODE_CHOICES, default='')
    zip_code        = models.CharField(max_length=3)
    emp_title       = models.CharField(max_length=256)
    emp_length      = models.IntegerField(default=0)

    class Meta:
        db_table = 'Borrowers'

