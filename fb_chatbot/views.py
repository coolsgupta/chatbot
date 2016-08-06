from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import generic

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
            try:
                if self.request.GET['hub.verify_token'] == '9582648830':
                    return HttpResponse(self.request.GET['hub.challenge'])
                else:
                    return HttpResponse('Error, invalid token')
            except:
                return HttpResponse('Error , no token found')


def index(request):
    return HttpResponse("Hello World")

def hello(request):
    return HttpResponse('By Bye World')