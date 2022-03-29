import scrapy


class KolesaspiderSpider(scrapy.Spider):
    name = 'kolesaspider'
    allowed_domains = ['kolesa.kz']
    start_urls = ['https://kolesa.kz/cars/']
    urls = [
        ['https://kolesa.kz/cars/region-aktubinskaya-oblast/?auto-custom=2', 4491],
        ['https://kolesa.kz/cars/region-almatinskaya-oblast/?auto-custom=2&auto-car-transm=1', 15595],
        ['https://kolesa.kz/cars/region-almatinskaya-oblast/?auto-custom=2&auto-car-transm=2',  29291],
        ['https://kolesa.kz/cars/region-akmolinskaya-oblast/?auto-custom=2', 17729],
        ['https://kolesa.kz/cars/region-atyrauskaya-oblast/?auto-custom=2', 3603],
        ['https://kolesa.kz/cars/region-yuzhnokazahstanskaya-oblast/?auto-custom=2', 18045],
        ['https://kolesa.kz/cars/region-vostochnokazakhstanskaya-oblast/?auto-custom=2', 7215],
        ['https://kolesa.kz/cars/region-zhambilskaya-oblast/?auto-custom=2', 6609],
        ['https://kolesa.kz/cars/region-zapadnokazakshstabskaya-oblast/?auto-custom=2', 2997],
        ['https://kolesa.kz/cars/region-karagandinskaya-oblast/?auto-custom=2', 8645],
        ['https://kolesa.kz/cars/region-kostanayskaya-oblast/?auto-custom=2', 3609],
        ['https://kolesa.kz/cars/region-kyzylordinskaya-oblast/?auto-custom=2', 3978],
        ['https://kolesa.kz/cars/region-mangistauskaya-oblast/?auto-custom=2', 5209],
        ['https://kolesa.kz/cars/region-pavlodarskaya-oblast/?auto-custom=2', 4120],
        ['https://kolesa.kz/cars/region-severokazakhstanskaya-oblast/?auto-custom=2', 1816]
    ]

    def parse(self, response, **kwargs):
        for url in self.urls:
            for i in range(1, url[1]//20):
                yield scrapy.Request(
                    f'{url[0]}&page={i}',
                    callback=self.parse_page
                )

    def parse_page(self, response):
        titles = response.xpath(
             "//div[contains(@class, 'a-info-side') and contains(@class, 'col-right-list')]/div[1]/span[1]/a/text()"
        ).extract()
        prices = response.xpath(
             "//div[contains(@class, 'a-info-side') and contains(@class, 'col-right-list')]/div[1]/span[3]/text()"
        ).extract()
        descriptions = response.xpath(
            "//div[contains(@class, 'a-info-side') and contains(@class, 'col-right-list')]/div[3]/div[1]/div[2]/text()"
        ).extract()
        cities = response.xpath(
            "//div[contains(@class, 'a-info-side') and contains(@class, 'col-right-list')]/div[4]/div[1]/div[1]/text()"
        ).extract()
        dates = response.xpath(
            "//div[contains(@class, 'a-info-side') and contains(@class, 'col-right-list')]/div[4]/div[1]/span[1]/text()"
        ).extract()
        row_data = zip(titles, prices, descriptions, cities, dates)
        for item in row_data:
            car_dict = {}
            try:
                title = item[0].strip()
                man_word_count = 1
                for man_two_word in [
                    'Alfa Romeo', 'Aston Martin', 'Great Wall', 'Iran Khodro', 'Land Rover', 'ВАЗ (Lada)'
                ]:
                    if man_two_word in title:
                        man_word_count = 2

                car_dict['manufacturer'] = ' '.join(title.split()[0:man_word_count]).strip()
                car_dict['model'] = ' '.join(title.split()[man_word_count:]).strip()
                car_dict['price'] = item[1].replace(u'\xa0', u' ').strip()
            except Exception as e:
                pass
            try:
                description = item[2].strip()
                description_tokens = description.split(',')
                car_dict['year'] = description_tokens[0].split()[0].strip()
                car_dict['body'] = description_tokens[1].split()[-1].strip()
                car_dict['engine_volume'] = description_tokens[2].split()[0].strip()
                car_dict['fuel_type'] = description_tokens[3].strip()
                car_dict['transmission'] = ' '.join(description_tokens[4].split()[1:]).strip()
            except Exception as e:
                pass
            try:
                car_dict['city'] = item[3].strip()
                car_dict['date'] = item[4].strip()
            except Exception as e:
                pass
            yield car_dict
