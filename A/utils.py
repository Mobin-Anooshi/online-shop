from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin



def send_otp_code(phone_number , code):
    try:
        api = KavenegarAPI('#')
        params ={
            'sender':'',
            'receptors':phone_number,
            'messages': f'کد تایید شما :{code}'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e :
        print(e)
    except HTTPException as e :
        print(e)
        
class IsAdminUserMixin(UserPassesTestMixin):    
    def test_func(self) :
        return self.request.user.is_authenticated and self.request.user.is_admin
    
