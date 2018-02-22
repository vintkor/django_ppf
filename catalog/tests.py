# from .models import Category, Product
# from nose import tools
#
#
# class TestCategory:
#     def setUp(self):
#         self.category = Category(title="lion", parent=None)
#         self.category.save()
#
#     def teardown(self):
#         pass
#
#     def test_get_absolute_url(self):
#         tools.assert_equal(self.category.get_absolute_url(), '/catalog/category/2/')
#
#     def test__str__(self):
#         tools.assert_equal(self.category.__str__(), self.category.title)
#
#
# class TestProduct:
#     def setUp(self):
#         cat = Category(title="lion", parent=None)
#         cat.save()
#         self.product = Product(title="product", category=cat)
#         self.product.save()
#
#     def teardown(self):
#         pass
#
#     def test_get_absolute_url(self):
#         tools.assert_equal(self.product.get_absolute_url(), '/catalog/product/1/')
#
#     def test_product_category(self):
#         tools.assert_equal(self.product.category.title, 'lion')
#
#     def test_obj__str__(self):
#         tools.assert_equal(str(self.product), self.product.title)
