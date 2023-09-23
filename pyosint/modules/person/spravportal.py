from pyosint.core.templates.person import Person

URL = "https://www.spravportal.ru/services/who-calls/num/"


class Spravportal(Person):
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_number_data(self, page_soup):
        number_raw_data = self.get_all_elements_from_parent(page_soup, "div", {"class": "col-sm-8 col-xs-8"})
        number_data = [data.text.strip() for data in number_raw_data]
        number_raw_comments_times = self.get_all_elements_from_parent(page_soup,
                                                                 "div", {"class": "col-lg-4 col-md-5 col-sm-5 col-xs-5"})
        number_raw_comments = self.get_all_elements_from_parent(page_soup, "div", {"class": "panel panel-default"})
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
