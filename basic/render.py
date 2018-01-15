

import warnings
import re

from django.template import RequestContext, loader
from django.template.context import _current_app_undefined
from django.template.engine import (
    _context_instance_undefined, _dictionary_undefined, _dirs_undefined,
)
from django.utils.deprecation import RemovedInDjango110Warning
from secu.models import Role, Right, RoleRight, User, UserRole
from django.http import HttpResponse
from django.db.models import Prefetch
from pyquery import PyQuery

"""
    rewrite django.shortcuts.render to add right limit
"""


def render(request, template_name, context=None, validator=None,
           context_instance=_context_instance_undefined,
           content_type=None, status=None, current_app=_current_app_undefined,
           dirs=_dirs_undefined, dictionary=_dictionary_undefined,
           using=None):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    Uses a RequestContext by default.
    """
    if validator is not None:
        if context is None:
            context = {
                'validator': merge_dict(*validator)
            }
        else:
            context['validator'] = merge_dict(*validator)
    if (context_instance is _context_instance_undefined
            and current_app is _current_app_undefined
            and dirs is _dirs_undefined
            and dictionary is _dictionary_undefined):
        # No deprecated arguments were passed - use the new code path
        # In Django 1.10, request should become a positional argument.
        content = loader.render_to_string(
            template_name, context, request=request, using=using)

    else:
        # Some deprecated arguments were passed - use the legacy code path
        if context_instance is not _context_instance_undefined:
            if current_app is not _current_app_undefined:
                raise ValueError('If you provide a context_instance you must '
                                 'set its current_app before calling render()')
        else:
            context_instance = RequestContext(request)
            if current_app is not _current_app_undefined:
                warnings.warn(
                    "The current_app argument of render is deprecated. "
                    "Set the current_app attribute of request instead.",
                    RemovedInDjango110Warning, stacklevel=2)
                request.current_app = current_app
                # Directly set the private attribute to avoid triggering the
                # warning in RequestContext.__init__.
                context_instance._current_app = current_app

        content = loader.render_to_string(
            template_name, context, context_instance, dirs, dictionary,
            using=using)
    user_name = request.session.get('user_name', None)
    if user_name != None:
        content = render_with_right_by_pyQuery(user_name, content)
    return HttpResponse(content, content_type, status)

def merge_dict(*args):
    result_dict = {}
    for item in args:
        result_dict.update(item)
    return result_dict    

def render_with_right(user_name, content):
    if user_name == 'root':
        return re.sub(r'#!(\S+)!#', '', content, flags=re.IGNORECASE)
    # 取出该字符串中存在的权限值
    right_list = re.findall(r'#!(?P<RightTag>\S+)!#', content, re.IGNORECASE)
    result_content = content
    if right_list:
        user_roles = UserRole.objects.select_related('role').filter(user=User.objects.get(user_name=user_name))
        # 用户拥有的所有（在right_list的范围内）
        own_right_list = []
        if user_roles:
            for user_role in user_roles:
                role = Role.objects.prefetch_related(Prefetch('rights', queryset=Right.objects.filter(view_name__in=right_list),
                                                              to_attr='own_rights')).get(pk=user_role.role.id)
                if role:
                    for right in role.own_rights:
                        if not own_right_list.__contains__(right.view_name):
                            own_right_list.append(right.view_name)
        if len(own_right_list) > 0:
            # 排除用户拥有的权限，不拥有的权限直接剔除
            right_split = '|'
            right_str = '|' + right_split.join(right_list) + '|'
            for right in own_right_list:
                right_filter = '|{}|'.format(right)
                right_str = right_str.replace(right_filter, '|')
            right_str = re.sub(r'(\|){2,}', '|', right_str)
            right_str = re.sub(r'^\|', '', right_str)
            right_str = re.sub(r'\|$', '', right_str)
            right_str = right_str.replace('.', '\.')
            exp = r'<(?P<HtmlTag>[^>\s]+)\s[^>]*#!({0})!#[^>]*>(?:(?!<\/(?P=HtmlTag)>)[\s\S])*<\/(?P=HtmlTag)>'.format(right_str)
            result_content = re.sub(exp, '', content, flags=re.IGNORECASE)
        else:
            # 没有任何权限，则剔除所有
            exp = r'<(?P<HtmlTag>[^>\s]+)\s[^>]*#!(\S+)!#[^>]*>(?:(?!<\/(?P=HtmlTag)>)[\s\S])*<\/(?P=HtmlTag)>'
            result_content = re.sub(exp, '', content, flags=re.IGNORECASE)
    return re.sub(r'#!(\S+)!#', '', result_content, flags=re.IGNORECASE)


def render_with_right_by_pyQuery(user_name, content):

    PQ = PyQuery(content)
    if user_name != 'root':
        # 取出该字符串中存在的权限值
        right_list = [right.attr('right') for right in PQ('[right]').items()]
        right_list = list(set(right_list))
        if right_list:
            user_roles = UserRole.objects.select_related('role').filter(user=User.objects.get(user_name=user_name))
            # 用户拥有的所有权限（在right_list的范围内）
            own_right_list = []
            if user_roles:
                for user_role in user_roles:
                    role = Role.objects.prefetch_related(Prefetch('rights', queryset=Right.objects.filter(view_name__in=right_list),
                                                                  to_attr='own_rights')).get(pk=user_role.role.id)
                    if role:
                        for right in role.own_rights:
                            if not own_right_list.__contains__(right.view_name):
                                own_right_list.append(right.view_name)
            # 根据用户权限剔除没有权限的标签
            for page_right in right_list:
                if not own_right_list.__contains__(page_right):
                    right_filter = '[right=' + page_right + ']'
                    PQ(right_filter.replace('.', '\.')).remove()
    PQ('[right]').remove_attr('right')
    return '<html>\n' + PQ.html(method='html') + '\n</html>'
