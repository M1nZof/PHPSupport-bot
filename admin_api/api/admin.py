from django.contrib import admin

from .models import Contractor, Client, Task, Question


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class ContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class ContractorAdmin(admin.ModelAdmin):
    pass
