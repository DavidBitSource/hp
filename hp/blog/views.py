# -*- coding: utf-8 -*-
#
# This file is part of the jabber.at homepage (https://github.com/jabber-at/hp).
#
# This project is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with this project. If not, see
# <http://www.gnu.org/licenses/>.

import logging

from django.conf import settings
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from core.views import HomepageViewMixin
from core.views import TranslateSlugViewMixin

from .models import BlogPost
from .models import Page

log = logging.getLogger(__name__)
_BLACKLIST = getattr(settings, 'SPAM_BLACKLIST', set())
_RATELIMIT_WHITELIST = getattr(settings, 'RATELIMIT_WHITELIST', set())
_RATELIMIT_CONFIG = getattr(settings, 'RATELIMIT_CONFIG', {})


class BasePageMixin(HomepageViewMixin):
    def get_menuitem(self):
        meta = self.object._meta
        return '%s_%s:%s' % (meta.app_label, meta.model_name, self.object.pk)

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_desc'] = object.get_meta_summary(self.request)
        context['updated'] = object.updated
        context['created'] = object.created
        context['og_title'] = object.title.current % self.request.site
        context['og_desc'] = object.get_opengraph_summary(self.request)
        context['canonical_url'] = object.get_canonical_url()
        context['twitter_title'] = object.title.current % self.request.site
        context['twitter_desc'] = object.get_twitter_summary(self.request)
        context['title'] = 'foo'
        return context


class PageView(TranslateSlugViewMixin, BasePageMixin, DetailView):
    queryset = Page.objects.filter(published=True)


class BlogPostMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()

        # If a user has permissions to publish blogposts, just return all blogposts.
        if self.request.user.has_perm('blog.blogpost_change'):
            return qs
        return qs.published()


class BlogPostListView(HomepageViewMixin, BlogPostMixin, ListView):
    queryset = BlogPost.objects.select_related('author').blog_order()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object_list']:
            newest = max(context['object_list'], key=lambda o: o.updated)
            context['updated'] = newest.updated
        else:
            context['updated'] = timezone.now()
        return context


class BlogPostView(TranslateSlugViewMixin, BasePageMixin, BlogPostMixin, DetailView):
    queryset = BlogPost.objects.all()
    context_object_name = 'post'
    static_context = {
        'og_type': 'article',
    }
