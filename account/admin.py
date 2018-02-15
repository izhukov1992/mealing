from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from account.models import Account


class AccountInline(admin.StackedInline):
    """Stacked account details in user model.
    """

    model = Account


class UserAdmin(BaseUserAdmin):
    """User admin section with account details.
    """

    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
