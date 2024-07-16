from django.shortcuts import render,redirect
from django.views import View
from accounts.forms import UserRegistertionForm , VerifyCodeForm , UserLoginForm
import random
from utils import send_otp_code
from accounts.models import OtpCode,User
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login , logout ,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin



class UserRegisterView(View):
    form_class = UserRegistertionForm
    def get(self,request):
        form = self.form_class()
        return render (request , 'accounts/register.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone_number'],random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'],code=random_code)
            request.session['user_register_info'] ={
                'phone_number':form.cleaned_data['phone_number'],
                'email':form.cleaned_data['email'],
                'full_name' :form.cleaned_data['full_name'],
                'password':form.cleaned_data['password'],
            }
            messages.success(request , 'we sent you a code','success')
            return redirect('accounts:verify_code')
        messages.error(request,'not ok form','danger')
        return render (request , 'accounts/register.html',{'form':self.form_class})

class UserRegisterVerifyCode(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'
    def get(self,request):
        form = self.form_class
        return render(request , self.template_name,{'form':form})
    
    def post(self,request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            create_code=code_instance.created.time()
            create_code1 = format(create_code.minute)
            datetime1 = datetime.now().time()
            datetime2 = format(datetime1.minute)

            if cd['code'] == code_instance.code :
                User.objects.create_user(user_session['phone_number'],user_session['email'],
                                         user_session['full_name'],user_session['password'],)
                if int(datetime2)-int(create_code1) < 3:
                    messages.error(request , 'expire code please try again','danger')
                    code_instance.delete()
                    return redirect('accounts:user_register')
                code_instance.delete()
                messages.success(request , 'you registered','success')
                return redirect('home:home')
            else:
                messages.error(request,'this code is wrong','danger')
                return redirect('accounts:verify_code')
        return render(request , 'accounts/verify.html',{'form':form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def get(self,request):
        form = self.form_class
        return render(request , self.template_name,{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd= form.cleaned_data
            user = authenticate(request , phone_number=cd['phone_number'],password=cd['password'])
            print(user)
            if user is not None:
                login(request , user)
                messages.success(request , 'login','success')
                return redirect('home:home')
            messages.error(request,'username or password is wrong','danger')
        return render(request , self.template_name , {'form':form})
    
    
class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request, 'Logout','success')
        return redirect('home:home')
    