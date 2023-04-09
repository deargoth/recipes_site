from unittest import TestCase

from .pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_the_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=2
        )
        self.assertEqual([1, 2, 3, 4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=3
        )
        self.assertEqual([1, 2, 3, 4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=4
        )
        self.assertEqual([2, 3, 4, 5, 6, 7], pagination)

    def test_make_pagination_is_static_when_last_page_is_near(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=10,
            current_page=14,
        )['pagination']
        self.assertEqual([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=10,
            current_page=15,
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15, 16, 17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=10,
            current_page=16,
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15, 16, 17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=10,
            current_page=17,
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15, 16, 17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=10,
            current_page=18,
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15, 16, 17, 18, 19, 20], pagination)
