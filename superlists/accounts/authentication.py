import sys
from accounts.models import ListUser, Token


class PasswordLessAuthenticationBackend(object):

    def authenticate(self, uid):
        print('uid', uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print('no token found', file=sys.stderr)
            return None

        token = Token.objects.get(uid=uid)
        print('Got Token', file=sys.stderr)

        try:
            user = ListUser.objects.get(email=token.email)
            print('Got Email', file=sys.stderr)
            return user
        
        except ListUser.DoesNotExist:
            print('New User', file=sys.stderr)
            return ListUser.objects.create(email=token.email)
    
    def get_user(self, email):
        return ListUser.objects.get(email=email)
