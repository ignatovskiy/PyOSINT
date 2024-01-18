from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://getyarn.io"


class GetYarn(Web):
    types = ["text"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/yarn-find?text={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        divs = self.get_all_elements_from_parent(parsed, 'div', {"class": "card tight bg-w"})
        clips = {}
        for div in divs:
            div_title = self.get_all_elements_from_parent(div,
                                                          'div',
                                                          {"class": "title ab fw5 p025 px05 tal"})[0]
            div_title_text = self.parse_strings_list([div_title])
            pre_link = self.get_all_elements_from_parent(div, "a", {"class": "p"})[0].get('href')
            pre_link = pre_link.replace("/yarn-clip/", "")
            link = f"https://y.yarn.co/{pre_link}.mp4"
            if not clips.get(div_title_text):
                clips[div_title_text] = [link]
            else:
                clips[div_title_text].append(link)
        return clips


def main():
    handle_cmd_args_module(GetYarn)


if __name__ == "__main__":
    main()
