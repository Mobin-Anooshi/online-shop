import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm,CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Order , OrderItem,Coupon
from django.contrib import messages
# Create your views here.

class CartView(View):
    def get(self,request) :
        cart = Cart(request)
        return render(request , 'orders/cart.html',{'cart':cart})
class CartAddView(View):
    def post(self,request,product_id):
        cart=Cart(request)
        products = get_object_or_404(Product , id = product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(products ,form.cleaned_data['quantity'])
        return redirect('orders:cart')
    
class CartRemoveView(View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product , id=product_id)
        cart.remove(product)
        return redirect('orders:cart')
    
class OrderDetailView(LoginRequiredMixin,View):
    form_class = CouponApplyForm
    def get (self,request,order_id):
        order = get_object_or_404(Order , id = order_id)
        return render (request , 'orders/orders.html',{'order':order,'form':self.form_class})
    
class OrderCreateView(LoginRequiredMixin , View):
    def get(self , request):
        cart = Cart(request)
        order = Order.objects.create(user = request.user)
        for item in cart :
            OrderItem.objects.create(order=order , product=item['product'],price=item['price'],quantity=item['quantity'])
        return redirect('orders:order_detail',order.id)
    
    
class CouponApplyView(LoginRequiredMixin,View):
    form_calss = CouponApplyForm
    
    def post(self,request,order_id):
        now = datetime.datetime.now()
        form = self.form_calss(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon =  Coupon.objects.get(code__exact=code, valid_from__lte=now , valid_to__gte=now,active=True)
            except Coupon.DoesNotExist :
                messages.error(request,'this coupon does not exists','danger')
                return redirect('orders:order_detail',order_id)
            order = Order.objects.get(pk = order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail',order_id)
        