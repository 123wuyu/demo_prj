from django.contrib import admin

from contents.models import ContentCategory, Content

admin.site.register(ContentCategory)
admin.site.register(Content)
