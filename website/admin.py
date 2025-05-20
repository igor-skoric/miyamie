from django.contrib import admin
from .models import Brand, Category, Dress, DressImage, Appointment, Config


class DressImageInline(admin.TabularInline):
    model = DressImage
    extra = 1


@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    list_display = ('name', 'category__name', 'tag')  # kolone koje se prikazuju u listi
    list_filter = ('category', 'tag')                      # filteri sa desne strane
    search_fields = ('name', 'category__name', 'tag')      # polja po kojima možeš da pretražuješ
    ordering = ('name',)                       # podrazumevano sortiranje
    inlines = [DressImageInline]

    prepopulated_fields = {"slug": ("name",)}              # automatski popunjava slug iz name



admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Appointment)
admin.site.register(Config)
