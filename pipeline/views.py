from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # !unsafe, but OK for prototype
from django.core.exceptions import ValidationError

from .models import Borrowers, Loans
from .validations import Borrowers_Validation as BV

import json

import pdb


def index(request):
    return JsonResponse({'status': 'OK'})

@csrf_exempt
def borrower(request, member_id):
    body = json.loads(request.body.decode('utf-8'))
    try:
        BV.check_fields(body)
        borrower = Borrowers.objects.get_or_create(
                pk              = None,
                all_util        = BV.validate_all_util(body['all_util']),
                annual_income   = BV.validate_annual_income(body['annual_income']),
                avg_cur_bal     = BV.validate_avg_cur_bal(body['avg_cur_bal']),
                dti             = BV.validate_dti(body['dti']),
                home_ownership  = BV.validate_home_ownership(body['home_ownership']),
                address_state   = BV.validate_address_state(body['address_state']),
                zip_code        = BV.validate_zip_code(body['zip_code']),
                emp_title       = BV.validate_emp_title(body['emp_title']),
                emp_length      = BV.validate_emp_length(body['emp_length'])
        )


    except ValidationError as e:
        return HttpResponse(e, status=400)

    # do we have all keys?

    # convert any of the keys
    return JsonResponse(body)
