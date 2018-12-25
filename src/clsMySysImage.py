class mysysImages(object):

    def __init__(self):
        self.next_page = 1
        self.results = []

    def get_next_page(self):
        self.next_page += 10
        return self.next_page

    def add_result(self, record):
        self.results.append(record)

    def get_result(self):
        return self.results


class mysysImage(object):

    def __init__(self, image_url):
        self.url = image_url

    def get_url(self):
        return self.url

