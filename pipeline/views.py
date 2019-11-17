from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # !unsafe, but OK for prototype

from .models import Borrowers, Loans

import json

import pdb

def index(request):
    return JsonResponse({'status': 'OK'})

@csrf_exempt
def borrower(request, member_id):
    body = json.loads(request.body.decode('utf-8'))
    return JsonResponse(body)
