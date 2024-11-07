from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        context["activate_url"] = (
            f"http://localhost:4200/email-confirmation?key={context['key']}"
        )
        super().send_mail(template_prefix, email, context)
