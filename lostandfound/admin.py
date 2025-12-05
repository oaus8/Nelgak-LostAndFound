from django.contrib import admin
from .models import LostItem, ClaimVerification

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'location_lost', 'date_lost', 'contact_name', 'created_at')
    list_filter = ('category', 'location_lost', 'date_lost')
    search_fields = ('item_name', 'description', 'contact_name', 'contact_email', 'contact_phone')

admin.site.register(ClaimVerification)
