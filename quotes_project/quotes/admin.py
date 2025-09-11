from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("short_text", "source", "weight", "likes", "dislikes", "views", "created_at")
    list_filter = ("source",)
    search_fields = ("text", "source")
    readonly_fields = ("views", "likes", "dislikes", "created_at")

    def short_text(self, obj):
        return obj.text[:80]
    short_text.short_description = "Цитата"