from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import TemplateView


CANONICAL_ROLES = (
    'Authenticated',
    'Administrator',
    # 'Contributor',
    # 'Viewer',
    # 'Reviewer',
)
CONFIG_PERMISSION = 'aoaforms.config'


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(CONFIG_PERMISSION):
            raise PermissionDenied()
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class RolesOverview(AdminRequiredMixin, TemplateView):
    template_name = 'cpanel/roles.html'

    def get_context_data(self, **kwargs):
        context = {}
        roles = []

        def has_perm(group, perm):
            return perm in ['%s.%s' % (p.content_type.app_label, p.codename)
                            for p in group.permissions.all()]

        for role in CANONICAL_ROLES:
            group, new = Group.objects.get_or_create(name=role)
            roles.append(dict(name=role,
                              config=has_perm(group, CONFIG_PERMISSION),
                              view=True))
        context['roles'] = roles
        return context


def index_view(request):
    return redirect('cpanel:roles')
