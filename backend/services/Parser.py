import bs4


class ParserService:
    def format_html(self, exchange_stock, long_name, txt):
        UNWANTED_ELEMENTS = [
            "\n",
            "  More",
            "  ",
            "About Google",
            "Get the iOS app",
            "For you",
            "(" + exchange_stock + ")",
            long_name,
            "Get the Android app",
            "FollowingSingaporeWorldLocalBusinessTechnologyEntertainmentSportsScienceHealth",
        ]

        soup = bs4.BeautifulSoup(txt, features="html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        aria_labels = [
            element
            for element in soup.find_all("div")
            if element.find("div") is not None
        ]
        aria_labels_set = set(
            [element.find("div").text.strip() for element in aria_labels]
        )

        aria_labels_string = " ".join(aria_labels_set)

        # remove unwanted elements
        for r in UNWANTED_ELEMENTS:
            aria_labels_string = aria_labels_string.replace(r, "")
        return aria_labels_string
