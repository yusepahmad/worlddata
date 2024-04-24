import json
import time

from datetime import datetime
from ..utils.request_response import PageFocus

sekarang = datetime.now()
format_ymd_hms = sekarang.strftime("%Y-%m-%d %H:%M:%S")

class HardCode(PageFocus):
    def __init__(self):
        super().__init__()
        self.url = None
        self.result = {
            'link': self.url,
            'tag': [
                'worlddata',
                'info'
            ],
            'domain':'www.worlddata.info',
        }
        self.up = {
            'file_name': '',
            'path_data_raw': '',
            'path_data_clear': '',
            "crawling_time": format_ymd_hms,
            "crawling_time_epoch": int(time.time())

        }


    def container(self, soup):
        container = soup.find(id="main")
        card = self.__card_intro(container)

        self.__intro(card)



        benua = self.url.split('/')[3]
        country = self.url.split('/')[4]

        url_page = f'https://www.worlddata.info/{benua}/{country}/'

        # self.__description(self.__boxwhite(container, 'boxwhite'))
        # self.__other(self.__boxwhite(container, 'boxwhite cgrey'))
        # self.__current_time(self.__boxwhite(container, 'boxwhite greybg center timelinks'))
        # self.__population(self.__boxwhite_id(container, 'population'))
        # self.__currnecy(self.__boxwhite(container, 'boxwhite center greybg'))
        # self.__climate(self.__boxwhite(container, 'boxwhite'))
        # self.__important(self.__boxwhite_id(container, 'country_b2'))
        # self.__important2(self.__boxwhite(container, 'boxwhite floater'))

        # methods = [
        #     ('__description', 'boxwhite', ['container', 'boxwhite']),
        #     ('__other', 'boxwhite', ['container', 'boxwhite cgrey']),
        #     ('__current_time', 'boxwhite', ['container', 'boxwhite greybg center timelinks']),
        #     ('__population', 'boxwhite_id', ['container', 'population']),
        #     ('__currnecy', 'boxwhite', ['container', 'boxwhite center greybg']),
        #     ('__climate', 'boxwhite', ['container', 'boxwhite']),
        #     ('__important', 'boxwhite_id', ['container', 'country_b2']),
        #     ('__important2', 'boxwhite', ['container', 'boxwhite floater'])
        # ]
        #
        # for method_name, box_type, args in methods:
        #     method = getattr(self, method_name, None)
        #     if method:
        #         try:
        #             if box_type == 'boxwhite':
        #                 method(self.__boxwhite(*args))
        #             elif box_type == 'boxwhite_id':
        #                 method(self.__boxwhite_id(*args))
        #         except Exception as e:
        #             print("Error in {}: {}".format(method_name, e))
        #     else:
        #         print("Method {} not found, skipping.".format(method_name))

        try:
            self.__description(self.__boxwhite(container, 'boxwhite'))
        except Exception as e:
            print("Error in description:", e)

        try:
            self.__other(self.__boxwhite(container, 'boxwhite cgrey'))
        except Exception as e:
            print("Error in other:", e)

        try:
            self.__current_time(self.__boxwhite(container, 'boxwhite greybg center timelinks'))
        except Exception as e:
            print("Error in current time:", e)

        try:
            self.__population(self.__boxwhite_id(container, 'population'))
        except Exception as e:
            print("Error in population:", e)

        try:
            self.__currnecy(self.__boxwhite(container, 'boxwhite center greybg'))
        except Exception as e:
            print("Error in currency:", e)

        try:
            self.__climate(self.__boxwhite(container, 'boxwhite'))
        except Exception as e:
            print("Error in climate:", e)

        try:
            self.__important(self.__boxwhite_id(container, 'country_b2'))
        except Exception as e:
            print("Error in important:", e)

        try:
            self.__important2(self.__boxwhite(container, 'boxwhite floater'))
        except Exception as e:
            print("Error in important2:", e)

        self.result.update(self.up)
        self.result.update({
            'link': self.url
        })
        print(json.dumps(self.result, indent=4))


    def __important2(self, box):
        title = [title.text.strip() for title in box.find_all('h2')]

        desk = [footnote.text.strip() for footnote in box.find_all(class_='footnote')]

        tables = [table for table in box.find_all('table')]

        for ii, table in enumerate(tables, start=0):
            datas = [tr for tr in table.find_all('tr')]
            ths = []
            tds = []
            for data in datas:
                for th in data.find_all('th'):
                    ths.append(th.text.strip())

                for td in data.find_all('td'):
                    if td.find(class_='indidot'):
                        tds.append(td.find(class_='indidot').get('style').split(':')[-1])
                    else:
                        tds.append(td.text)

            if ths:
                result = []

                for i in range(0, len(tds), len(ths)):
                    obj = {
                        'title': title[ii],
                        'description': desk[ii]
                    }
                    for j in range(len(ths)):
                        obj[ths[j]] = tds[i + j]
                    result.append(obj)
            else:
                result = {}
                for i in range(0, len(tds), 2):
                    result.update(
                        {
                            'title': title[ii],
                            'description': desk[ii],
                            tds[i]: tds[i + 1]
                        }
                    )

            items = {
                title[ii]: result
            }


            self.result.update(items)


    def __important(self, box):
        title = [title.text.strip() for title in box.find_all('h2')]


        important_table = box.find_all('table')

        for ii, table in enumerate(important_table, start=0):
            datas = [tr for tr in table.find_all('tr')]
            ths = []
            tds = []
            for data in datas:
                for th in data.find_all('th'):
                    ths.append(th.text.strip())

                for td in data.find_all('td'):
                    tds.append(td.text)


            if ths:
                result = []
                for i in range(0, len(tds), 2):
                    obj = {}
                    obj[ths[0]] = tds[i]
                    obj[ths[1]] = tds[i + 1]
                    result.append(obj)
            else:
                result = {}
                for i in range(0, len(tds), 2):
                    result.update(
                        {
                            tds[i]:tds[i+1]
                        }
                    )

            items = {
                title[ii]: result
            }

            self.result.update(items)


    def __intro(self, card):
        title = card.find('h1').text.strip()
        img = [f"https://cdn.worlddata.info{img.get('src')}" for img in card.find_all('img')]
        parlement = str(card.find(class_='i1')).split("</h1>")[-1].split("<br/>")[0].strip()
        others = [{key : value} for key, value in zip([key.text.strip() for key in card.find(class_='i2').find_all(class_='indent')], [value.text.strip() for value in card.find(class_='i2').find_all(class_='floater')])]

        self.result.update(
            {
                'country':title,
                'continent': self.url.split('/')[3],
                'government': parlement,
            }
        )
        for item in others:
            self.result.update(item)

    def __description(self, box):
        georaphy = box
        desk = self.soup(str(georaphy).split('</h2>')[-1]).text.strip()

        self.result.update(
            {
                'geography': desk
            }
        )

    def __other(self, box):
        further = box
        further = [{'title' : atext, 'link' : alink} for atext, alink in zip([a.text.strip() for a in further.find_all('a')], [a.get('href') for a in further.find_all('a')])]

        self.result.update(
            {
                'further': further
            }
        )

    def __current_time(self, box):
        current_time = box
        hour = current_time.find(id='localtime_hour').text.strip()
        day = current_time.find(id='localtime_day').text.strip()
        desc_loc = self.soup(''.join(str(current_time.find(id='localtime_box')).split('<br/>')[1:])).text.strip()

        self.result.update(
            {
                'hour':hour,
                'day':day,
                'description_location': desc_loc
            }
        )

    def __population(self, box):
        population = box
        title_population = [pops.text.strip().replace(' ','_').lower() for pops in population.find_all('h2')]
        populations = [ pop_raw.text.strip() for pop_raw in population.find(class_='tabs-lr').find_all('div')]
        img = ['https:'+img.get('src') for img in population.find_all('img')]


        for pops in populations:
            if '/' in pops:
                pops_split = pops.split('/')

                male = pops_split[0]
                if len(pops_split[1].split(':')) > 2:
                    item = {
                        male : pops_split[1].split(':')[1],
                        pops_split[1].split(':')[0] : pops_split[1].split(':')[2]
                    }
                    self.result.update(item)
            else:
                pops_split = pops.split(':')
                if '' not in pops_split:

                    item = {
                        pops_split[0] : pops_split[1]
                    }

                    if item.values():
                        self.result.update(item)

    def __currnecy(self, box):
        currency = box
        currency_items = {'currency':'','currency_description': self.soup(str(currency).split('<div class="currency">')[0]).text.strip()}
        currency_items.update({'currency':self.soup(str(currency).split('<div class="currency">')[1]).text.strip()})

        self.result.update(currency_items)

    def __climate(self, box):
        climate = box
        climate_item = {'climate_title': climate.find('h2').text.strip(), 'climate_description': self.soup(str(climate).split('</h2>')[-1]).text.strip()}

        self.result.update(climate_item)


    def __card_intro(self, container):
            card = container.find(id="intro3")
            return card

    def __boxwhite(self, container, class_data):
        box = container.find(class_=class_data)
        return box

    def __boxwhite_index(self, container, class_data):
        box = container.find_all(class_=class_data)[5]
        return box

    def __boxwhite_id(self, container, id_param):
        box = container.find(id=id_param)
        return box