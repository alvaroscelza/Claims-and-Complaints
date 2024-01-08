from django.contrib import admin
from users.models import User, UserScoreModifierInstance, UserScoreModifierType
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(UserScoreModifierType)
class UserScoreModifierTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(UserScoreModifierInstance)
class UserScoreModifierInstanceAdmin(admin.ModelAdmin):
    pass


class UserAdmin(UserAdmin):
    model = User
    list_display = [
        "email",
        "username",
        "email_validated",
        "is_active",
        "email_invalid",
        "last_login",
        "date_joined",
        "is_superuser",
        "updated_at",
    ]
    list_editable = ["is_active"]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Custom Fields",
            {
                "fields": (
                    "profile_picture",
                    "email_validated",
                    "email_invalid",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
