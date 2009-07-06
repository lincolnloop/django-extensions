from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
from django.template.loader import render_to_string
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django_extensions.forms.widgets import ForeignKeySearchInput

class AdminForeignKeySearchInput(ForeignKeySearchInput, ForeignKeyRawIdWidget):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input
    instead in a <select> box.
    """
    # if this is set, the if None test below doesn't trigger to use reverse()
    #search_path = '../foreignkey_autocomplete/'

    def __init__(self, rel, search_fields, attrs=None):
        ForeignKeyRawIdWidget.__init__(self, rel, attrs)
        self.search_fields = search_fields
        if self.search_path is None:
            try:
                self.search_path = reverse('foreignkey_autocomplete')
            except NoReverseMatch:
                raise ImproperlyConfigured(
                    "The foreignkey autocomplete URL couldn't be "
                    "auto-detected. Make sure you include "
                    "'django_extensions.urls.autocomplete' in your URLconf.")

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        return truncate_words(obj, 14)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        opts = self.rel.to._meta
        app_label = opts.app_label
        model_name = opts.object_name.lower()
        related_url = '../../../%s/%s/' % (app_label, model_name)
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        if value:
            value = force_unicode(value)
            label = self.label_for_value(value)
        else:
            value = u''
            label = u''
        context = {
            'url': url,
            'related_url': related_url,
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'search_path': self.search_path,
            'search_fields': ','.join(self.search_fields),
            'model_name': model_name,
            'app_label': app_label,
            'label': label,
            'value': value,
            'name': name,
            'safe_name': name.replace('-', '_'),
        }
        output = render_to_string(self.widget_template or (
            'django_extensions/admin/widgets/%s/%s/foreignkey_searchinput.html' % (app_label, model_name),
            'django_extensions/admin/widgets/%s/foreignkey_searchinput.html' % app_label,
            'django_extensions/admin/widgets/foreignkey_searchinput.html',
        ), context)
        return mark_safe(u''.join(output))
