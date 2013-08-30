from django.contrib import admin
from walt.models import Tag, Document, Profile


class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']

class DocumentAdmin(admin.ModelAdmin):
	search_fields = ['title']

class ProfileAdmin(admin.ModelAdmin):
  search_fields = ['language']

admin.site.register( Tag, TagAdmin )
admin.site.register( Document, DocumentAdmin )
admin.site.register( Profile, ProfileAdmin )
