from django.core.exceptions import ValidationError

from .models import Borrowers, Loans
from .models import home_ownership_choices, address_state_choices
from .models import grade_choices, status_choices, term_choices

import numpy as np
import string

import pdb


class Borrowers_Validation:

    @classmethod
    def check_fields(cls, request_body):
        fields = set([f.name for f in Borrowers._meta.get_fields()])
        fields.remove('loans')
        fields.remove('member_id')
    
        keys = set(request_body.keys())

        for f in fields:
            if f not in keys:
                raise ValidationError(f"'{f}' was not found in {keys}.\n")

    @classmethod
    def validate_all_util(cls, value):
        return np.clip(np.float(value), 0.0, 250.0) if value is not np.nan else 0.0

    @classmethod
    def validate_annual_income(cls, value):
        return np.clip(np.float(value), 0.0, 1e7) if value is not np.nan else 0.0

    @classmethod
    def validate_avg_cur_bal(cls, value):
        return np.clip(np.float(value), 0.0, 1e5) if value is not np.nan else 0.0

    @classmethod
    def validate_dti(cls, value):
        return np.clip(np.float(value), 0.0, 100.0) if value is not np.nan else 0.0

    @classmethod
    def validate_home_ownership(cls, value):
        choices = [c[0] for c in home_ownership_choices()]
        if value.upper() not in choices:
            return 'OTHER'
        return value.upper()

    @classmethod
    def validate_address_state(cls, value):
        choices = [c[0] for c in address_state_choices()]
        if value.upper() not in choices:
            raise ValidationError("The choice for 'state address' is not valid.\n")
        return value.upper()

    @classmethod
    def validate_zip_code(cls, value):
        try:
            value = str(value)[:3]
            if (len(value) < 3) or (not value.isdigit()):
                raise ValidationError
            else:
                return value
        except:
            raise ValidationError("Invalid zip code.\n")

    @classmethod
    def validate_emp_title(cls, value):
        value = str(value) if value is not np.nan else ''
        value = value.lower().rstrip().lstrip()
        return ''.join(list(filter(lambda x: x in string.ascii_lowercase, value)))

    @classmethod
    def validate_emp_length(cls, value):
        value = str(value)
        value = ''.join(list(filter(lambda x: x.isdigit(), value)))
        value = 0 if value == '' else value
        return np.clip(np.int(value), 0, 10)


class Loans_Validation:

    @classmethod
    def check_fields(cls, request_body):
        fields = set([f.name for f in Loans._meta.get_fields()])
        fields.remove('id')
    
        keys = set(request_body.keys())

        for f in fields:
            if f not in keys:
                raise ValidationError(f"'{f}' was not found in {keys}.\n")

    @classmethod
    def validate_member_id(cls, value):
        value = int(value)
        if value < 1:
            raise ValidationError("Member PK cannto be negative.\n")
        return value

    @classmethod
    def validate_title(cls, value):
        return str(value).lower()

    @classmethod
    def validate_funded_amount(cls, value):
        return np.clip(np.float(value), 0.0, 5e4)

    @classmethod
    def validate_total_payments(cls, value):
        return np.clip(np.float(value), 0.0, 1e5)

    @classmethod
    def validate_grade(cls, value):
        choices = [c[0] for c in grade_choices()]
        if value.upper() not in choices:
            raise ValidationError(f"The {value} is not supported.\n")
        return value.upper()

    @classmethod
    def validate_interest_rate(cls, value):
        return np.clip(np.float(value), 0.0, 32.0)

    @classmethod
    def validate_amount(cls, value):
        return np.clip(np.float(value), 0.0, 5e4)

    @classmethod
    def validate_status(cls, value):
        choices = [c[0] for c in status_choices()]
        value = value.upper()
        if 'CURRENT' in value:
            value = 'CURRENT'
        elif 'FULLY PAID' in value:
            value = 'PAID'
        elif 'GRACE' in value:
            value = 'GRACE'
        elif '31-120' in value:
            value = 'LATE2'
        elif '16-30' in value:
            value = 'LATE1'
        else:
            value = 'DEFAULT'
        return value

    @classmethod
    def validate_meets_policy(cls, value):
        return bool(value)

    @classmethod
    def validate_term(cls, value):
        choices = [c[0] for c in term_choices()]
        value = ''.join(list(filter(lambda x: x.isdigit(), str(value))))
        if value not in choices:
            raise ValidationError("The term choices supported are only 36 and 60 months.\n")
        return value
