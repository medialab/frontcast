from django.contrib import admin

from observer.models import DocumentProfile, Layout, Section, LayoutField



class SectionInline(admin.TabularInline):
    model = Section
    extra = 1



# Register your models here.
class LayoutAdmin(admin.ModelAdmin):
  search_fields = ['name']
  inlines = (SectionInline, )



class LayoutFieldAdmin(admin.ModelAdmin):
  search_fields = ['name']






admin.site.register(DocumentProfile)
admin.site.register(Layout, LayoutAdmin)

admin.site.register(LayoutField, LayoutFieldAdmin)