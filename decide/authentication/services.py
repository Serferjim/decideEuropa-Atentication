from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from authentication.models import TwoStepsAuth
from django.core.exceptions import ObjectDoesNotExist
from Crypto import Random
from rest_framework.authtoken.models import Token

def send_mail_2_steps_auth(user):
    u = check_if_user_exists(user)
    code = str(int.from_bytes(Random.new().read(24), 'big'))
    try:	
        old_two_steps_auth = TwoStepsAuth.objects.get(user = u)
        old_two_steps_auth.delete()
        two_steps_auth = TwoStepsAuth.objects.create(code = code, user = u)
    except ObjectDoesNotExist:
        two_steps_auth = TwoStepsAuth.objects.create(code = code, user = u)
    send_mail('Autenticación en Decide mediante email', ''.join(('Use el siguiente código para autenticarse en el sistema\r\n\r\n', str(code))), 'decide@decide.com', [user.email], fail_silently = False)

def login_email_auth(user):
    u = check_if_user_exists(user)
    try:
        token = Token.objects.get(user = u)
        raise ValidationError(_("El usuario ya está autenticado en el sistema"),
            code = 'token_already_created',
            params = {},)
    except ObjectDoesNotExist:
        TwoStepsAuth.objects.get(user = u).delete()
        token = Token.objects.create(user = u)
        
def check_if_user_exists(user):
    u = User.objects.get(pk = user.pk)
    if u == None:
        raise ValidationError(_("No se ha encontrado el usuario en la base de datos"),
            code = '404_usuario',
            params = {},)
    return u

    
