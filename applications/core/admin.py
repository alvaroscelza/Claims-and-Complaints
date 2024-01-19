from django.contrib import admin

from applications.core.models import Business, Company, Judgement


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Judgement)
class JudgementAdmin(admin.ModelAdmin):
    pass
