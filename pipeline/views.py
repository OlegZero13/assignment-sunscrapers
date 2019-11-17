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
    except ValidationError as e:
        return HttpResponse(e, status=400)

    # do we have all keys?

    # convert any of the keys
    return JsonResponse(body)
