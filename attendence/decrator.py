from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.core.urlresolvers import reverse

from attendence.models.Employee import Employee
from secu.models import User, UserRole, Right
import functools

def valid_user(fn):
    fn.need_valid = 1
    @functools.wraps(fn)
    def _valid(request, **kwargs):
        if request.session.get('user_name', None) == None:
            if request.is_ajax():
                response = HttpResponse(reverse('login', args=None))
                response['redirect'] = 1
                return response
            return HttpResponseRedirect(reverse('login', args=None))
        else: 
            if is_authorized(request, fn.__module__ + '.' + fn.__name__):
                return fn(request, **kwargs)
            else:
                if request.is_ajax():
                    response = HttpResponse(reverse('login', args=None))
                    response['redirect'] = 1
                    return response
                return HttpResponseRedirect(reverse('login', args=None))
    return _valid  

def is_authorized(request, view_name):
    from basic.config import ROOTUSER   
    if ROOTUSER['name'] == request.session.get('user_name'):
        return True
    else:    
        user = User.objects.get(user_name=request.session.get('user_name'))
        user_roles = UserRole.objects.filter(user=user)
        right = Right.objects.get(view_name=view_name)
        for user_role in user_roles:
            for role_right in user_role.role.roleright_set.all():
                if right == role_right.right:
                    return True
        return False        