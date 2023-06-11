from pyosint.core.utils import *


URL = "https://zvonili.com/phone/"


class Zvonili():
    def __init__(self, input_data):
        self.input_data = input_data

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}{input_data}"

    def get_number_data(self, page_soup):
        number_raw_data = get_all_elements_from_parent(page_soup, 'td')
        number_data = [data.text.strip() for data in number_raw_data][::-2][::-1]
        number_comments_raw = get_all_elements_from_parent(page_soup, "blockquote", {"class": "card-blockquote"})
        number_times_raw = get_all_elements_from_parent(page_soup, "span", {"style": "font-size: 14px;"})
        number_times = [data.text.strip() for data in number_times_raw]
        number_comments = [data.text.strip() for data in number_comments_raw]
        return number_data, [f"{time_} | {comment}" for time_, comment in zip(number_times, number_comments)]

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        try:
            number_data, number_comments = self.get_number_data(parsed)

            if len(number_data) == 0:
                number_rating, number_views, number_reviews, number_category = None, None, None, None
            elif len(number_data) == 4:
                number_rating, number_views, number_reviews, number_category = number_data
            elif len(number_data) == 2:
                number_rating, number_views = number_data
                number_reviews, number_category = None, None
            elif len(number_data) == 3:
                number_rating, number_views, number_reviews = number_data
                number_category = None
            else:
                number_rating, number_category, number_reviews, number_views = None, None, None, None

            if not number_comments:
                number_comments = None
        except ValueError:
            number_rating, number_category, number_reviews, number_views, number_comments = None, None, None, None, None
        return {"rating": number_rating,
                "views": number_views,
                "reviews": number_reviews,
                "category": number_category,
                "comments": number_comments}


def main():
    pass


if __name__ == "__main__":
    main()
