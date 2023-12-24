from django.contrib import admin

from applications.core.models import Business, Company, UserScoreModifierType, UserScoreModifierInstance, Judgement, \
    ClientUser


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(UserScoreModifierType)
class UserScoreModifierTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(UserScoreModifierInstance)
class UserScoreModifierInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Judgement)
class JudgementAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    pass
