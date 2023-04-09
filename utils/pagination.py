import math


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)

    page_range = list(page_range.page_range)

    # print(page_range
    current_page = current_page.number

    total_pages = len(page_range)
    start_range = current_page - middle_page
    stop_range = current_page + middle_page

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        pages = stop_range - total_pages
        stop_range -= pages
        start_range -= pages

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_is_out_of_range': current_page > middle_page,
        'last_page_is_out_of_range': stop_range < total_pages,
    }
