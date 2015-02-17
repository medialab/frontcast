from django.contrib import admin
from observer.models import Document, Tag, WorkingDocument, Profile



class DocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'reference', 'slug']
  fields = ['title', 'type', 'abstract', 'owner', 'tags', 'reference']


class TagAdmin(admin.ModelAdmin):
  search_fields = ['name']
  list_filter = ('type',)



class WorkingDocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'slug']
  fields = ['title', 'type', 'abstract', 'parent', 'dependencies', 'owner', ]
  list_filter = ('type',)



admin.site.register(Profile)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(WorkingDocument, WorkingDocumentAdmin)