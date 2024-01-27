import scrapy

class ImmoscoutSpider(scrapy.Spider):
    name = "wohnungsboerse_B"
    allowed_domains = ["www.wohnungsboerse.net"]

    def start_requests(self):
        #base_url = "https://www.wohnungsboerse.net/searches/index?marketing_type=kauf&estate_types%5B0%5D=1&estate_types%5B1%5D=3&is_rendite=0&provisionsfrei=0&private_offer=0&cities%5B0%5D=Berlin&page={}"
        base_url = "https://www.wohnungsboerse.net/searches/index?estate_marketing_types=kauf%2C1&marketing_type=kauf&estate_types%5B0%5D=1&is_rendite=0&cities%5B0%5D=Berlin&term=Berlin&umkreiskm=20&pricetext=ab%2050000%20%E2%82%AC&minprice=50000&page={}"
        for page in range(0, 662):  # Update the range to scrape all pages
            url = base_url.format(page)
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        houses = response.css('main div div section a')
        for index, house in enumerate(houses, start=1):
            house_classes = house.attrib.get('class', '').split()
            if 'h-auto' in house_classes and 'pb-6' in house_classes and 'mb-4' in house_classes and 'overflow-hidden' in house_classes and 'rounded-lg' in house_classes and 'sm:grid' in house_classes and 'sm:grid-cols-12' in house_classes and 'bg-bg' in house_classes and 'shadow-20' in house_classes and 'sm:gap-4' in house_classes and 'lg:h-72' in house_classes and 'sm:pb-0' in house_classes:
                continue  # Skip unwanted houses
            house_url = response.urljoin(house.attrib['href'])
            yield scrapy.Request(house_url, callback=self.parse_house)

    def parse_house(self, response):
        item = {
            "title": response.css("div div div h2::text").get(),
            "location": response.css('div.p-4.mt-4.bg-bg.md\\:px-8.md\\:py-10 div div div div:nth-child(2)::text').get(),
            "price": response.css('div div dl dd::text').get(),
            "area": response.css('div dl:nth-child(3) dd::text').get(),
            "rooms": response.css('div dl:nth-child(2) dd::text').get(),
            "url": response.url,
            "description": response.css("div.p-4.mt-4.md\\:grid.md\\:grid-cols-12.bg-bg.md\\:py-10.md\\:px-8 div.overflow-hidden::text").get(),
            "lage": response.css("div.p-4.mt-4.md\\:grid.md\\:grid-cols-12.bg-bg.md\\:py-10.md\\:px-8 div span::text").getall(),
            "baujahr": response.css("div.p-4.mt-4.md\\:grid.md\\:grid-cols-12.bg-bg.md\\:py-10.md\\:px-8 div table tr td::text").getall()
        }
        yield item