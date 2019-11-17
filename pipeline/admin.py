from django.contrib import admin
from .models import Borrowers, Loans


class Borrowers_AdminPanelDisplay(admin.ModelAdmin):
    items = set([f.name for f in Borrowers._meta.get_fields()])
    items.remove('loans')
    list_display = tuple(items)

class Loans_AdminPanelDisplay(admin.ModelAdmin):
    list_display = tuple([f.name for f in Loans._meta.get_fields()])


admin.site.register(Borrowers, Borrowers_AdminPanelDisplay)
admin.site.register(Loans, Loans_AdminPanelDisplay)
