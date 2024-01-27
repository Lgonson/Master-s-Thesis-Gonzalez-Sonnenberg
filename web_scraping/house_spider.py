# import the scrapy module
import scrapy

# define the spider class
class ImmoscoutSpider(scrapy.Spider):
    # name of the spider, used to call it from the command line
    name = "immowelt"

    # the domain(s) that the spider is allowed to crawl
    allowed_domains = ["www.immowelt.de"]

    # the method that will be called when the spider starts to run
    def start_requests(self):
        print(f'self is: {self}')
        # the base URL that will be used to crawl the pages
        #base_url = "https://www.immowelt.de/liste/berlin/immobilien/mk?d=true&pmi=50000&sd\
        #=DESC&sf=TIMESTAMP&sp={}"
        #base_url = "https://www.immowelt.de/liste/berlin/wohnungen/kaufen?d=true&pmi=50000&rmi=1&sd=DESC&sf=TIMESTAMP&sp={}"
        base_url = "https://www.immowelt.de/liste/berlin/haeuser/kaufen?d=true&pmi=50000&rmi=1&sd=DESC&sf=TIMESTAMP&sp={}"


        # loop over the range of pages to be crawled (1 to 490)
        for number_page in range(0, 311):
            # create the URL for the current page
            url = base_url.format(number_page)
            # make a request to the current page and call the 'parse' method to handle the response
            yield scrapy.Request(url=url, callback=self.parse)

    # the method that will be called to handle the response from each page
    def parse(self, response):
        # select all the 'houses' on the page
        houses = response.css("div.EstateItem-1c115")

        # loop over the 'houses' on the page
        for house in houses:
            # get the URL for the current house
            house_url = response.urljoin(house.css("div.EstateItem-1c115 a").attrib["href"])
            print(f"house_url is: {house_url}")

            # make a request to the URL of the current house and call the 'parse_house' method to handle the response
            yield scrapy.Request(house_url, callback=self.parse_house, meta={"item":
                {
                # extract the data for the current house and add it to the 'meta' dictionary
                "title": house.css("div.EstateItem-1c115 a div.FactsMain-bb891 h2::text").get(),
                "location": house.css("div.EstateItem-1c115 a div.FactsMain-bb891 div div div span::text").get(),
                "price": house.css(
                    "div.EstateItem-1c115 a div.FactsMain-bb891 div.KeyFacts-efbce div[data-test='price']::text").get(),
                "area": house.css(
                    "div.EstateItem-1c115 a div.FactsMain-bb891 div.KeyFacts-efbce div[data-test='area']::text").get(),
                "rooms": house.css(
                    "div.EstateItem-1c115 a div.FactsMain-bb891 div.KeyFacts-efbce div[data-test='rooms']::text").get(),
                "url": house_url
            }})

    # the method that will be called to handle the response from each house
    def parse_house(self, response):
        # get the 'item' dictionary from the 'meta' dictionary
        item = response.meta["item"]
        # extract the description for the current house and add it to the 'item' dictionary
        item["description"] = response.css("sd-card app-texts sd-read-more div p::text").getall(),

        item["lage"] = response.css("sd-card div sd-read-more div p::text").get(),
        item['baujahr'] = response.css('sd-card div sd-cell sd-cell-row sd-cell-col p::text').getall(),
        item['baujahr_1'] = response.css('sd-card li::text').getall(),
        item['baujahr_2'] = response.css("app-estate-object-informations sd-card div ul li").getall(),
        item['baujahr_3'] = response.css("app-energy div div sd-cell.cell.ng-star-inserted sd-cell-row sd-cell-col p::text").getall(),
        item['baujahr_4'] = response.css('sd-card div sd-cell sd-cell-col p::text').getall(),

        # yield the 'item' dictionary
        yield item




