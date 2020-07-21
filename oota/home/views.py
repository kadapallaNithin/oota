from django.shortcuts import render, redirect
from django.contrib import messages
from payments.models import PostPaid, WaterPostPaidTransaction
def index(request):
#    if request.method == 'POST':
 #       if request.POST.product:
  #          return redirect(request,'home/pay.html')
  context = dict()
  if request.user.is_authenticated :
    context['status'] = 'logged in'
    post_paid = PostPaid.objects.filter(user=request.user).first()
    context['last_transaction'] = WaterPostPaidTransaction.objects.filter(post_paid=post_paid).first()
  else:
    context['status'] = 'not logged in'
  return render(request,'home/index.html',context)

def error(request,**kwargs):
  if 'message' in kwargs  and kwargs['message'] != None:
    messages.warning(request,kwargs["message"])
  if 'redirect' in kwargs and kwargs['redirect'] != None:
    return redirect(kwargs['redirect'])
  return render(request,'home/base.html')
#class HomeView(ListView):
#    model = 
def about(request):
    return render(request,'home/about.html')