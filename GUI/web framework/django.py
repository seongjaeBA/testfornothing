from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response

def readhtml(request):
    return render_to_response(request)

if __name__ == '__main__':
    
    readhtml('mdod850-HbO.html')


