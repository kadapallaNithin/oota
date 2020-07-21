from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, ListView
from django import forms
from .models import PostPaid, WaterPostPaidTransaction
from payments.models import Plan, WaterTransaction
from product.models import Product, ProductIPAddress
from product import views as product_views

class WaterTransactionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = WaterTransaction
    fields = ['request']

    def test_func(self):
        plan = get_object_or_404(Plan,id=self.kwargs.get('plan_id'))
        return plan.user == self.request.user
    def form_valid(self,form):
        plan = get_object_or_404(Plan,id=self.kwargs.get('plan_id'))
        form.instance.plan = plan
        #Invalid = False
        if not plan.is_active :
        #    Invalid = True
            messages.warning(self.request,f'Plan is not activated yet! Please contact the owner.')
        elif plan.remaining < form.instance.request:
        #    Invalid = True
            messages.warning(self.request,f'You can only request for { plan.limit } - { plan.used } = { plan.remaining } but requested for { form.instance.request }.')
        #if Invalid:
        #    return HttpResponseRedirect(reverse('water_transaction',args=(plan.id,)))
        else:
            #self.kwargs['ip_address'] = product_views.get_product_ip(self.request, plan.product_id)
            plan.used += form.instance.request
            plan.save()
            return super().form_valid(form)
        return HttpResponseRedirect(reverse('water_transaction',args=(plan.id,)))

        def get_context_data(self):
            context = super().get_context_data()
            context['object'] = get_object_or_404(Plan,id=self.kwargs.get('plan_id'))
            return context

@login_required
def dispense(request,transaction_id):
    txn = get_object_or_404(WaterTransaction,id=transaction_id)
    product = txn.plan.product
    link_data = ProductIPAddress.objects.filter(product_id=product.id).order_by('id')[0]
    #context = {"link_data":link_data}
    return HttpResponseRedirect(f"http://{ link_data.ip }/turn?key={ link_data.product_key }") #render(request,'payments/dispense.html',context)

class WaterTransactionListView(LoginRequiredMixin, ListView):
    model = WaterTransaction
    ordering = ['-started_on']
    def get_queryset(self):
        return WaterTransaction.objects.filter(plan__user=self.request.user)

class PlanCreateView(LoginRequiredMixin,CreateView):
    model = Plan
    fields = ['limit']

    def get_context_data(self):
        context = super().get_context_data()
        context['product'] = get_object_or_404(Product,id=self.kwargs.get('product_id'))
        return context

    def form_valid(self,form):
        user = self.request.user
        if user.is_authenticated:
            form.instance.user = user
            form.instance.product = get_object_or_404(Product,id=self.kwargs.get('product_id'))
#            if len(Plan.objects.filter(user=self.request.user,product=form.instance.product)) == 0:
            try :
                return super().form_valid(form)
            except OverflowError:
                messages.warning(self.request,f'Too big limit!')
        #     else:
        #         messages.warning(self.request,f'Already registered! for { form.instance.product }')
        return redirect('my_plans')

class PlanActivateUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Plan
    fields = ['limit']
    template_name = 'payments/plan_update.html'
 
    def form_valid(self,form):
        plan = form.instance
        if not plan.is_active :
            plan.is_active = True
            try:
                return super().form_valid(form)
            except OverflowError:
                messages.warning(self.request,f"Too big limit!")
        else:
            messages.warning(self.request,f"You can't activate plan { plan }! as this plan is aleady active.")
        return redirect('my_devices') 

    def test_func(self):
        user = self.request.user
        plan = get_object_or_404(Plan,id=self.kwargs.get('pk'))
        return plan.product.owner == user

class PlanRequestsListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Plan
    template_name = 'payments/plan_requested_list.html'

    def get_queryset(self):
        product = get_object_or_404(Product,id=self.kwargs.get('product_id'))
        return Plan.objects.filter(product=product)

    def test_func(self):
        product = get_object_or_404(Product,id=self.kwargs.get('product_id'))
        return product.owner == self.request.user

class MyPlansListView(LoginRequiredMixin,ListView):
    model = Plan

    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user).order_by('-date')

class PostPaidCreateView(LoginRequiredMixin, CreateView):
    model = PostPaid#, UserPassesTestMixin
    fields = []#['product']
    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.bill = 0
        form.instance.product = get_object_or_404(Product,pk=self.kwargs.get('product_id'))#Product.objects.filter(id=self.kwargs.get('product_id')).first()#request.POST['product']
        if len(PostPaid.objects.filter(user=self.request.user,product=form.instance.product)) != 0:
            messages.warning(self.request,f'Already registered! for { form.instance.product }')
            return redirect('post_paid_list')
        form_is_valid = super().form_valid(form)
        if form_is_valid:
            messages.success(self.request,f'{ form.instance.user } has requested post paid for { form.instance.product }')
        return form_is_valid
        
class PostPaidUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostPaid
    fields = ['limit']
    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.bill = 200
        #form.instance.product = self.request.user.product
        return super().form_valid(form)

class PostPaidListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = PostPaid
    fields = ['product','limit','bill']
    context_object_name = 'object'

    def get_queryset(self):
        return PostPaid.objects.filter(user=self.request.user)

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            #if user.postpaid
            return True
        return False


class WaterPostPaidTransactionCreateView(CreateView):
    model = WaterPostPaidTransaction
    fields = ['num_liters']

def water_dispensed_periodic(request):
    if request.method == "GET":
        g = request.GET
        if 'key' in g  and '' in g and 'trans' in g :
            prod_ips = ProductIPAddress.objects.filter(product_id=g['prod'])
            if len(prod_ips) >= 1:
                prod_ip = prod_ips.last()
                if prod_ip.server_key == g['key']:
                    prod_key = "nithin"
                    serv_key = "nithinPk"
                    new_prod_ip = ProductIPAddress.objects.create(product_id=g['prod'],ip=g['ip'],product_key=prod_key,server_key=serv_key)
                    new_prod_ip.save()
                    return HttpResponse('{"api_key":"'+prod_key+'","ssid":"kadapalla","password":"12345678"}')
    return HttpResponse("I got nothing")














#class PostPaidForm(LoginRequiredMixin, UserPassesTestMixin, forms.ModelForm):
 #   class Meta:
  #      model = PostPaid
   #     fields = ['product','user']
    
    
#@login_required
#def postpaid(request):
#    if request.method == 'POST':
 #       form = PostPaidForm(request.POST)
  #      if form.is_valid():
   #         form.save()
    #        messages.success(request,f'Postpaid established!')
     #       return redirect('home')
    #else:
     #   form = PostPaidForm()
    #return render(request,'payments/postpaid.html',{'form':form})
