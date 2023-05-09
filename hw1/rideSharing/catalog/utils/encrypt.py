from django.conf import settings
import hashlib

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8')) ## added salt
    obj.update(data_string.encode('utf-8')) ## hashed the password with salt
    return obj.hexdigest()