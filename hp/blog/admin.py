# -*- coding: utf-8 -*-
#
# This file is part of the jabber.at homepage (https://github.com/jabber-at/hp).
#
# This project is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-xmpp-account.
# If not, see <http://www.gnu.org/licenses/.

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    actions = ['make_publish', 'make_unpublish', ]
    readonly_fields = ('author', 'created', 'updated', )
    list_display = ('published', '__str__', 'author', 'created', )
    list_display_links = ('__str__', )
    list_filter = ('author', )

    fieldsets = (
        (None, {
            'fields': ('author', ('created', 'updated', ), ('published', 'sticky', )),
        }),
        (_('Title'), {
            'fields': [('title_de', 'title_en'), ],
        }),
        (_('Text'), {
            'fields': [('text_de', 'text_en'), ],
        }),
    )

    #################
    # Admin actions #
    #################
    def make_publish(self, request, queryset):
        queryset.update(published=True)
    make_publish.short_description = _('Publish selected blog posts')

    def make_unpublish(self, request, queryset):
        queryset.update(published=False)
    make_unpublish.short_description = _('Unpublish selected blog posts')

    def save_model(self, request, obj, form, change):
        if change is False:  # adding a new object
            obj.author = request.user
        obj.save()
