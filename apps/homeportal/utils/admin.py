"""Generic admin utilities and config."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)


class BaseAppAdminMixin(SimpleHistoryAdmin, ModelAdmin, ImportExportModelAdmin):
    """Base application admin mixin."""

    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseAppAdminMixin):
    """Unfold user admin config."""

    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, BaseAppAdminMixin):
    """Unfold group admin config."""

    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm
