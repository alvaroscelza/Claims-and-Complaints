from django.contrib import admin

from applications.core.models import Industry, Company, Judgement


@admin.register(Industry)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Judgement)
class JudgementAdmin(admin.ModelAdmin):
    pass
