from nose import tools
from assistant.models import Category
from django.test import TestCase


class TestCategory:
    def setUp(self):
        self.cat1 = Category(title='cat1', parent=None, active=True)
        self.cat1.save()

        self.cat2 = Category(title='cat2', parent=self.cat1, active=True)
        self.cat2.save()

    def teardown(self):
        pass

    def test_get_id(self):
        tools.assert_equal(self.cat1.get_id(), '')
        tools.assert_equal(self.cat2.get_id(), self.cat1.id)

    def test_rew(self):
        tools.assert_true(hasattr(Category, 'get_id'))


# class Category2TestCase(TestCase):
#     def setUp(self):
#         self.cat1 = Category(title='cat1', parent=None, active=True)
#         self.cat1.save()
#
#         self.cat2 = Category(title='cat2', parent=self.cat1, active=True)
#         self.cat2.save()
#
#     def test_get_id(self):
#         self.assertEquals(self.cat1.get_id(), '')
#         self.assertEquals(self.cat2.get_id(), self.cat1.id)
