from django.contrib import admin
from example.blog.models import Entry, Tag
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django_extensions.admin.widgets import AdminManyToManySearchInput

class EntryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {
       'author': ('first_name', 'email'),
    }
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'tags':
            kwargs['widget'] = AdminManyToManySearchInput(db_field.rel, ('name',))
        return super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Entry, EntryAdmin)

admin.site.register(Tag)