from django.contrib import admin
from walt.models import Assignment, Document, Profile, Tag, Task, Unit


class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']

class TaskAdmin(admin.ModelAdmin):
  search_fields = ['name']

class DocumentAdmin(admin.ModelAdmin):
	search_fields = ['title', 'reference', 'slug']

class ProfileAdmin(admin.ModelAdmin):
  search_fields = ['language']

class UnitAdmin(admin.ModelAdmin):
  search_fields = ['name']

admin.site.register(Assignment)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Unit, UnitAdmin)
