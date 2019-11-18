from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt # !unsafe, but OK for prototype
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from .models import Borrowers, Loans
from .validations import Borrowers_Validation as BV
from .validations import Loans_Validation as LV

import json

import pdb


def index(request):
    return JsonResponse({'status': 'OK'})

@csrf_exempt
def borrower(request, member_id):
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        if body_str == '':
            return HttpResponse('No data attached.\n', status=404)
        body = json.loads(body_str)
        try:
            BV.check_fields(body)
            borrower = Borrowers.objects.update_or_create(pk= int(member_id), defaults={
                'all_util'        : BV.validate_all_util(body['all_util']),
                'annual_income'   : BV.validate_annual_income(body['annual_income']),
                'avg_cur_bal'     : BV.validate_avg_cur_bal(body['avg_cur_bal']),
                'dti'             : BV.validate_dti(body['dti']),
                'home_ownership'  : BV.validate_home_ownership(body['home_ownership']),
                'address_state'   : BV.validate_address_state(body['address_state']),
                'zip_code'        : BV.validate_zip_code(body['zip_code']),
                'emp_title'       : BV.validate_emp_title(body['emp_title']),
                'emp_length'      : BV.validate_emp_length(body['emp_length'])
            })
        except ValidationError as e:
            return HttpResponse(e, status=400)
        return HttpResponse(f'Borrower entry updated (pk={member_id}).\n', status=201)

    else:
        try:
            borrower = Borrowers.objects.get(pk=member_id)
        except Borrowers.DoesNotExist:
            return HttpResponse(f"Borrower of pk={member_id} does not exist.\n", status=404)
    return JsonResponse(model_to_dict(borrower))

@csrf_exempt
def loan(request, loan_id):
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        if body_str == '':
            return HttpResponse('No data attached.\n', status=404)
        body = json.loads(body_str)
        try:
            LV.check_fields(body)
            member_id = LV.validate_member_id(body['member_id'])
            borrower = Borrowers.objects.get(pk=member_id)
            loan = Loans.objects.update_or_create(pk=int(loan_id), defaults={
                'member_id'       : borrower,
                'title'           : LV.validate_title(body['title']),
                'funded_amount'   : LV.validate_funded_amount(body['funded_amount']),
                'total_payments'  : LV.validate_total_payments(body['total_payments']),
                'grade'           : LV.validate_grade(body['grade']),
                'interest_rate'   : LV.validate_interest_rate(body['interest_rate']),
                'amount'          : LV.validate_amount(body['amount']),
                'status'          : LV.validate_status(body['status']),
                'meets_policy'    : LV.validate_meets_policy(body['meets_policy']),
                'term'            : LV.validate_term(body['term'])
            })
        except Borrowers.DoesNotExist:
            return HttpResponse(f"Borrower of pk={member_id} does not exist.\n", status=404)
        except ValidationError as e:
            return HttpResponse(e, status=400)
        return HttpResponse(f'Loan entry updated (pk={loan_id}).\n', status=201)
    else:
        try:
            loan = Loans.objects.get(pk=loan_id)
        except Loans.DoesNotExist:
            return HttpResponse(f"Loan of pk={loan_id} does not exist.\n", status=404)
    return JsonResponse(model_to_dict(loan))
