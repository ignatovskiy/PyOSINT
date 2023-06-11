from pyosint.core.utils import *


URL = "https://www.spravportal.ru/services/who-calls/num/"


class Spravportal():
    def __init__(self, input_data):
        self.input_data = input_data

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_number_data(self, page_soup):
        number_raw_data = get_all_elements_from_parent(page_soup, "div", {"class": "col-sm-8 col-xs-8"})
        number_data = [data.text.strip() for data in number_raw_data]
        number_raw_comments_times = get_all_elements_from_parent(page_soup,
                                                                 "div", {"class": "col-lg-4 col-md-5 col-sm-5 col-xs-5"})
        number_raw_comments = get_all_elements_from_parent(page_soup, "div", {"class": "panel panel-default"})
        number_times = [data.text.strip() for data in number_raw_comments_times]
        number_comments = [data.p.text for data in number_raw_comments if data.p]
        return number_data, [f"{time_} | {comment}" for time_, comment in zip(number_times, number_comments)]

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        try:
            number_data, number_comments = self.get_number_data(parsed)
            number_rating, number_category = number_data
        except ValueError:
            number_rating, number_category, number_comments = None, None, None
        return {"rating": number_rating,
                "category": number_category,
                "comments": number_comments}


def main():
    pass


if __name__ == "__main__":
    main()
