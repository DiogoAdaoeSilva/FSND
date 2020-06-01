import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsdn.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drink'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
[DONE]
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    '''All errors in this method raise a 401 'Unauthorized' error code '''
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization_header_is_expected.' 
            }, 401)
    
    header_parts = auth.split()
    print('>>> header_parts:', header_parts ) #debugging
    print('>>> len(header_parts):', len(header_parts)) # debugging

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'authorization_header_invalid',
            'description': "Header must start with 'Bearer'. "
            }, 401)

    elif len(header_parts) == 1:
        raise AuthError({
            'code': 'authorization_header_invalid',
            'description': 'Missing token.'
            }, 401)

    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'authorization_header_invalid',
            'description': 'Authorization header must be bearer token.'
            }, 401)

    token = header_parts[1]
    return token
    

        

   

'''
[DONE]
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid claims',
            'description': 'Permissions not included in JWT'
            }, 400) # Bad request error code

    print(">>> payload['permissions']:", payload['permissions'] )

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Permission not found',
            'description': 'User does not have permission to do requested change'
            }, 403) # Forbidden error code
    return True

'''
[DONE]
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid) [DONE]
    it should verify the token using Auth0 /.well-known/jwks.json [DONE]
    it should decode the payload from the token [DONE]
    it should validate the claims [DONE]
    return the decoded payload [DONE]

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    '''Credit to Udacity's classes where it is shown how to verify and decode tokens
    Used the same structure as shown in the Udacity's classes'''
    jsonurl =urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json') #open url where keys are found
    print('>>> jsonurl:',jsonurl) # debugging
    jwks = json.loads(jsonurl.read()) # load keys found in above url
    print('>>> jwks:', jwks) #debugging
    
    unverified_header = jwt.get_unverified_header(token) # returns the JWT's header without doing any kind of validation
    print('>>> unverified_header', unverified_header)

    rsa_key = {}
    if 'kid' not in unverified_header: # The "kid" (key ID) Header Parameter is a hint indicating which key was used to secure the JWS.
        raise AuthError({
            'code': 'invalid error',
            'description': 'Authorization malformed'
            }, 401)
    # verify the token using Auth0 /.well-known/jwks.json    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
            'kty': key['kty'],
            'kid': key['kid'],
            'use': key['use'],
            'n': key['n'],
            'e': key['e']
            }
    print('>>> rsa_key:', rsa_key)
    if rsa_key:
        print('>>> passed if rsa_key')
        # decode the payload
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience = API_AUDIENCE,
                issuer = 'https://' + AUTH0_DOMAIN + '/')

            print('>>> payload:', payload)

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims, check audience and issuer.'
                }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
        }, 400)







'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token [DONE]
    it should use the verify_decode_jwt method to decode the jwt [DONE]
    it should use the check_permissions method validate claims and check the requested permission []
    return the decorator which passes the decoded payload to the decorated method []
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print('>>> running requires_auth') #debugging
            token = get_token_auth_header()
            try:
                print('>>> running_verify_jwt')
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            
            print('>>> running check_permissions')
            print('>>> permission:', permission)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs) # return the payload to the decorated function

        return wrapper
    return requires_auth_decorator