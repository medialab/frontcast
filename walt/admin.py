from django.contrib import admin
from walt.models import Document, Tag, WorkingDocument



class DocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'reference', 'slug']



class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']



class WorkingDocumentAdmin(admin.ModelAdmin):
  search_fields = ['title', 'slug']
  fields = ['title', 'type', 'abstract', 'parent', 'dependencies', 'documents', 'owner', ]



admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(WorkingDocument, WorkingDocumentAdmin)