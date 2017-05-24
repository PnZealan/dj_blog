from django.shortcuts import render,render_to_response
from django.http.response import HttpResponse
from blog.models import article_list

# Create your views here.
def index(request):    
    content = article_list.objects.all().order_by('id')
    Context = {'content':content}
    return render_to_response('index.html', Context)




def first(request):
    return render_to_response('index0.html')



def article(request, id):
    content = article_list.objects.filter( id = id )
    Context = {'content':content}
    return render_to_response('article_base.html',Context)
