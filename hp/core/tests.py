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

import doctest
from contextlib import contextmanager
from unittest import mock

from celery import task

from django.test import TestCase as DjangoTestCase
from django.test import Client
from django.test import override_settings

from . import utils


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(utils))
    return tests


class HomepageTestCaseMixin(object):
    def assertIsTask(self, t, expected):
        self.assertEqual(t, task(expected))

    def assertTaskCall(self, mocked, task, *args, **kwargs):
        self.assertTrue(mocked.called)
        a, k = mocked.call_args
        self.assertEqual(k, {})  # apply_async receives task args/kwargs as tuple/dict arg

        instance, called_args, called_kwargs = a

        self.assertIsTask(instance, task)
        self.assertEqual(args, called_args)
        self.assertEqual(kwargs, called_kwargs)

    @contextmanager
    def mock_celery(self):
        def run(self, args, kwargs):
            return self.run(*args, **kwargs)

        with mock.patch('celery.app.task.Task.apply_async', side_effect=run, autospec=True) as func:
            yield func


class TestCase(HomepageTestCaseMixin, DjangoTestCase):
    pass


@override_settings(MIDDLEWARE=[
    'django.contrib.sessions.middleware.SessionMiddleware',  # required by AuthenticationMiddleware
    'django.middleware.locale.LocaleMiddleware',  # required by standard view
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # required by HomepageMiddleware
    'core.middleware.HomepageMiddleware',
])
class MiddlewareTestCase(TestCase):
    def test_basic(self):
        c = Client()
        with self.assertTemplateUsed('blog/blogpost_list.html'):
            response = c.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.wsgi_request.os, 'any')
            self.assertTrue(response.wsgi_request.os_mobile)
            # If we execute the test-suite with "manage.py test" instead of "fab test", localsettings will be
            # used and the results are different.
            self.assertEqual(response.wsgi_request.site['NAME'], 'example.com', 'Tested with fab test?')


#@override_settings(ROOT_URLCONF=__name__)
class I18nURLTests(TestCase):
    def test_basic(self):
        self.fail()
