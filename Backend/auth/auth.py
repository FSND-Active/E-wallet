from flask import request
from functools import wraps
from datetime import datetime,timedelta
import jwt
import os

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error=error
        self.status_code= status_code

# encode jwt
'''
@TODO implement encode_jwt(mail,permissions) method
    @INPUTS
        mail: user email address(string)
        permissions: ['string permissions']

    it should create and encode the payload
    return the encoded payload or token
'''

def encode_jwt(mail:str,permissions:list):
    payload= {
        "email":mail,
        "permission":permissions,
        "exp":datetime.utcnow() + timedelta(minutes=60),
        "iat":datetime.utcnow()
    }
    return jwt.encode(payload,os.getenv("KEY"),"HS256")

# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''

def get_token_auth_header():
    header= request.headers.get("Authorization",None)
    if not header:
        raise AuthError("no Authorization header",401)
    token= header.split()
    if token[0].lower() != "bearer":
        raise AuthError("Invalid Header", 400)
    elif len(token)>2:
        raise AuthError("invalid Header",400)
    elif len(token)==1:
        raise AuthError("invalid Header",400)
    return token[1]


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
'''

def check_permissions(permission,payload):
    if "permission" not in payload:
        raise AuthError("Permissions not included",401)
    if permission not in payload["permission"]:
        raise AuthError("You forbidden from using this service",403)
    return True



'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should decode the payload from the token
    return the decoded payload
'''

def verify_decode_jwt(token):
    try:
        payload= jwt.decode(token,os.getenv("KEY",))
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("token_expired",401)
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token",401)
    except Exception:
        raise AuthError("Unable to parse authentication token",400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method to check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''

def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            token= get_token_auth_header()
            payload= verify_decode_jwt(token)
            check_permissions(permission,payload)
            return f(payload,*args,**kwargs)
        return wrapper
    return requires_auth_decorator
