from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import Product,Category
from . import tasks
from django.contrib import messages
from .forms import UploadFileForm
from django.contrib.auth.mixins import UserPassesTestMixin
from utils import IsAdminUserMixin
from orders.forms import CartAddForm
# Create your views here.


class HomeView(View):
    def get(self,request,category_slug=None):
        products = Product.objects.filter(available = True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products=products.filter(category=category)
        return render(request , 'home/index.html',{'products':products,'categories':categories})
    
class ProductDetailView(View):
    def get(self,request,slug):
        product = get_object_or_404(Product,slug=slug)
        form = CartAddForm()
        return render(request , 'home/detail.html',{'product':product,'form':form})
    
class BucketHomeView(IsAdminUserMixin,View):
    template_name = 'home/bucket.html'
    def get(self,request,*args, **kwargs):
        objects = tasks.all_bucket_objects_task()
        return render(request , self.template_name,{'objects':objects})
class DeleteBucketObjects(IsAdminUserMixin,View):
    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request,'your objects will be delete soon','info')
        return redirect('home:bucket')
class DownloadBucketObject(IsAdminUserMixin,View):
    def get(self,request,key):
        messages.success(request,'your download will started soon','info')
        tasks.download_object_task.delay(key)
        return redirect('home:bucket')  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# class UploadBucketObject(IsAdminUserMixin, View):
#     def post(self, request):
#         image = request.FILES.get('image')
#         print(image)
#         image_info = {
#             'filename': image.name,
#             'size': image.size,
#             'content_type': image.content_type,
#             # Add more fields as needed
#         }
#         print(image_info)   
#         tasks.upload_object_task.delay(image_info)
#         return redirect('home:bucket')
        
        