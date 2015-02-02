from django.contrib import admin
from observer.models import Document, Tag, WorkingDocument, Profile



class DocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'reference', 'slug']



class TagAdmin(admin.ModelAdmin):
  search_fields = ['name']
  list_filter = ('type',)



class WorkingDocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'slug']
  fields = ['title', 'type', 'abstract', 'parent', 'dependencies', 'documents', 'owner', ]
  list_filter = ('type',)



admin.site.register(Profile)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(WorkingDocument, WorkingDocumentAdmin)