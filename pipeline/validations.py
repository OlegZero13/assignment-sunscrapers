from django.core.exceptions import ValidationError

from .models import Borrowers, Loans
from .models import home_ownership_choices, address_state_choices

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
    def validate_all_util(value):
        return np.clip(np.float(value), 0.0, 250.0) if value is not np.nan else 0.0

    @classmethod
    def validate_annual_income(value):
        return np.clip(np.float(value), 0.0, 1e7) if value is not np.nan else 0.0

    @classmethod
    def validate_avg_cur_bal(value):
        return np.clip(np.float(value), 0.0, 1e5) if value is not np.nan else 0.0

    @classmethod
    def validate_dti(value):
        return np.clip(np.float(value), 0.0, 100.0) if value is not np.nan else 0.0

    @classmethod
    def validate_home_ownership(value):
        choices = [c[0] for c in home_ownership_choices]
        if value.upper not in choices:
            return 'OTHER'
        return value.upper()

    @classmethod
    def validate_address_state(value):
        choices = [c[0] for c in address_state_choices()]
        if value.upper() not in choices:
            raise ValidationError("The choice for 'state address' is not valid.")
        return value.upper()

    @classmethod
    def validate_zip_code(value):
        try:
            value = str(value)[:3]
            if (len(value) < 3) or (not value.isdigit()):
                raise ValidationError
        except:
            raise ValidationError("Invalid zip code.")

    @classmethod
    def validate_emp_title(value):
        value = str(value) if value is not np.nan else ''
        value = value.lower().rstrip().lstrip()
        return ''.join(list(filter(lambda x: x in string.ascii_lowercase, value)))

    @classmethod
    def validate_emp_length(value):
        return np.clip(np.int(value), 0, 10)

