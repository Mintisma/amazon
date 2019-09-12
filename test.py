import requests


class SearchTerms:
    n = 0
    d = dict()
    searched = set()
    base_url = 'https://completion.amazon.com/search/complete?mkt=1&search-alias=aps&q='

    def drop_down(self, search):
        url = self.base_url + search
        wb_data = requests.get(url)
        self.d[self.n] = [ele.replace('"', '') for ele in wb_data.text.split(',[')[1].split(',')]
        self.d[self.n] = [ele.replace(']', '') for ele in self.d[self.n]]
        self.searched.add(search.replace('%20', ' '))
        for kw in [ele for ele in self.d[0]]:  # base case 1: if search term == response
            if (kw not in self.searched) and (len(kw.split()) < 4):
                self.n += 1
                self.drop_down(kw)