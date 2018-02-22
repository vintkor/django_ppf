from django.test import TestCase


class SomeTestCase(TestCase):
    def setUp(self):
        pass

    def test_some_method(self):
        self.assertEquals(1, 1)
