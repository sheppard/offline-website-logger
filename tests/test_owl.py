from __future__ import unicode_literals

from rest_framework.test import APITestCase
from rest_framework import status
import json
from time import gmtime
from calendar import timegm
import swapper

User = swapper.load_model('auth', 'User')
from owl.models import Event
from tests.test_app.models import Item


class OwlTestCase(APITestCase):
    def setUp(self):
        Item.objects.create(name="Test Item", id=1)

    def log(self, events):
        data = json.dumps(events)
        response = self.client.post(
            "/owl.json",
            content_type="application/json",
            data=data,
            HTTP_USER_AGENT="Test Client 1.0",
        )
        self.assertTrue(
            status.is_success(response.status_code),
            response.status_code,
        )
        self.assertEqual(Event.objects.count(), len(events))
        return response


class AnonymousTestCase(OwlTestCase):
    def test_no_get(self):
        response = self.client.get("/owl.json")
        self.assertFalse(status.is_success(response.status_code))

    def test_log_model(self):
        self.log([{"path": "/items/1/"}])
        event = Event.objects.all()[0]

        self.assertEqual(event.session.client.ip_address, "127.0.0.1")
        self.assertEqual(event.session.client.user_agent, "Test Client 1.0")
        self.assertEqual(event.session.client.browser, "Other")
        self.assertEqual(event.path, "/items/1/")
        self.assertEqual(event.action, "view")

    def test_log_notexist(self):
        self.log([{"path": "/items/2/"}])
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]

        self.assertEqual(event.session.client.ip_address, "127.0.0.1")
        self.assertEqual(event.path, "/items/2/")

    def test_log_invalid_url(self):
        self.log([{"path": "/invalid/"}])
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]
        self.assertEqual(event.path, "/invalid/")

    def test_custom_action(self):
        self.log([{"path": "/items/1/", "action": "edit"}])
        event = Event.objects.all()[0]
        self.assertEqual(event.action, "edit")

    def test_referer(self):
        self.log([{"path": "/items/1/", "referer": "http://example.com/"}])
        event = Event.objects.all()[0]
        self.assertEqual(event.referer, "http://example.com/")

    def test_lag(self):
        ts0 = timegm(gmtime())
        ts1 = ts0 - 10 * 60
        ts2 = ts1 - 10 * 60
        self.log([
            {"path": "/",         "client_date": ts2},
            {"path": "/items/",   "client_date": ts1},
            {"path": "/items/1/", "client_date": ts0},
        ])

        events = Event.objects.order_by('client_date')
        self.assertEqual(int(events[0].lag.seconds / 60), 20)
        self.assertEqual(int(events[1].lag.seconds / 60), 10)
        self.assertEqual(int(events[2].lag.seconds / 60),  0)

    def test_server_view(self):
        # Server-rendered HTML should cause log events
        self.client.get("/items/1/", HTTP_ACCEPT="text/html")
        self.assertGreater(Event.objects.count(), 0)
        event = Event.objects.all()[0]
        self.assertEqual(event.path, "/items/1/")
        self.assertEqual(event.action, "server:view")

    def test_api_fetch(self):
        # JSON fetches should not cause log events
        self.client.get("/items/1/", HTTP_ACCEPT="application/json")
        self.assertEqual(Event.objects.count(), 0)


class LoggedInTestCase(OwlTestCase):
    def setUp(self):
        super(LoggedInTestCase, self).setUp()
        self.user = User.objects.create(
            username="testuser",
        )
        self.user.set_password('1234')
        self.user.save()

    def do_auth(self):
        self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': '1234',
        })
        self.assertTrue(self.client.session)
        Event.objects.all().delete()

    def test_log(self):
        self.do_auth()
        self.log([{"path": "/items/1/"}])
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]
        self.assertEqual(event.session.user, self.user)

    def test_session(self):
        self.do_auth()
        self.log([{"path": "/items/1/", "client_key": 1234}])
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]
        self.assertEqual(event.session.client_key, "1234")
        self.assertIsNotNone(event.session.server_key)
