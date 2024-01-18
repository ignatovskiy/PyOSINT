from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://prod-alt.screenshot.api.visualping.io"


class Screenshot(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        data = {"renderer": "6.1.0", "target_device": "4", "url": self.input_data, "wait_time": "2",
                "alert_error": True, "getAllText": False, "getHTMLTree": True,
                "preactions": {"active": False, "actions": []}}

        return self.get_request_content(self.make_request('post', url, data_=data))

    def get_search_url(self):
        return f"{URL}/screenshot/fastshot"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url())
        return {"Screenshot": ''}


def main():
    handle_cmd_args_module(Screenshot)


if __name__ == "__main__":
    main()
