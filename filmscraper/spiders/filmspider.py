import scrapy
from filmscraper.items import FilmItem


class FilmspiderSpider(scrapy.Spider):
    name = "filmspider"
    allowed_domains = ["filmweb.pl"]
    start_urls = ["https://filmweb.pl/films/search?page=" + str(i) for i in range(1, 1001)]

    def parse(self, response):
        films = response.css('.previewCard')
        for film in films:
            relative_url = film.css('.preview__link ::attr(href)').get()
            film_url = "https://filmweb.pl" + relative_url
            yield response.follow(film_url, callback=self.parse_film)

    def parse_film(self, response):
        film_item = FilmItem()

        film_item['url'] = response.url

        self.parse_film_basic_info(film_item, response)
        self.parse_film_media(film_item, response)
        self.parse_film_cast(film_item, response)
        self.parse_film_additional_info(film_item, response)
        self.parse_film_trivia(film_item, response)
        self.parse_film_reviews(film_item, response)

        yield film_item

    def parse_film_basic_info(self, film_item, response):
        title = response.css(".filmCoverSection__title ::text").get()
        film_item['title'] = title

        org_title = response.css(".filmCoverSection__originalTitle ::text").get()
        film_item['org_title'] = org_title if org_title else title

        film_item['length'] = response.css(".filmCoverSection__duration span ::text").get()
        film_item['year'] = response.css(".filmCoverSection__year ::text").get()
        film_item['avg_viewer_rating'] = response.css(".filmRating--hasPanel .filmRating__rateValue ::text").get()
        film_item['avg_critic_rating'] = response.css(".filmRating--filmCritic .filmRating__rateValue ::text").get()
        film_item['plot'] = response.css(".filmPosterSection__plot span ::text").get()

        poster = response.css(".filmPosterSection__poster a img")
        film_item['poster_url'] = poster.attrib['src'] if poster else ""

        film_item['genre'] = response.xpath("//div[@itemprop='genre']/span/a/span/text()").get()
        film_item['country'] = response.xpath(
            "//div[@itemprop='genre']/following-sibling::div[1]/span/a/span/text()").get()
        film_item['universum'] = response.xpath("//span[contains(@data-i18n,'entity@world')]/text()").get()

        world_premiere = response.xpath("//span[@itemprop='datePublished' and @class='block']/text()")
        film_item['world_premiere'] = world_premiere[0].get() if world_premiere else ""
        pl_premiere = response.xpath("//span[@itemprop='datePublished' and @class='block premiereCountry']/text()")
        film_item['pl_premiere'] = pl_premiere[0].get() if pl_premiere else world_premiere[0].get()

    def parse_film_media(self, film_item, response):
        # photos
        imgs = response.xpath("//img[@class='gallery__photo']")
        imgs_src_array = [img.attrib['src'] for img in imgs]
        film_item['photos_url'] = imgs_src_array

        # videos
        video = response.css(".thumbnail__video source")
        film_item['video_url'] = video[0].attrib['src'] if video else ""

    def parse_film_cast(self, film_item, response):
        # cast
        cast_xpath = response.xpath("//div[@itemprop='actor']/div/a/img")
        cast = []
        for actor in cast_xpath:
            actor_name = actor.attrib['alt'].split(" / ")[0]
            actor_role = actor.attrib['alt'].split(" / ")[1]
            actor_photo = actor.attrib['content']
            cast.append(dict(
                actor_name=actor_name,
                actor_role=actor_role,
                actor_phot_url=actor_photo
            ))
        film_item['cast'] = cast

    def parse_film_additional_info(self, film_item, response):
        direction = response.xpath("//div[@data-type='directing-info']/a")
        film_item['direction'] = direction.attrib['title'] if direction else ""

        script = response.xpath("//div[@data-type='screenwriting-info']/a")
        film_item['script'] = script.attrib['title'] if script else ""
        film_item['description'] = response.css('.descriptionSection__moreText ::text').get()
        film_item['boxoffice'] = response.xpath(
            "//div[contains(@class, 'filmInfo__group--filmBoxOffice')]/div[@class='filmInfo__info'][1]/div[1]/text()").get()
        film_item['budget'] = response.xpath(
            "//div[contains(@class, 'filmInfo__group--filmBoxOffice')]/div[@class='filmInfo__info'][2]/text()").get()
        film_item['studio'] = response.xpath(
            "//div[contains(@class, 'filmInfo__group--studios')]/div[@class='filmInfo__info']/text()").get()

    def parse_film_trivia(self, film_item, response):
        trivia = response.css('.curiositiesSection__item')
        trivia_arr = []
        for el in trivia:
            arr = el.css("::text")
            trivia_el = ""
            for part in arr:
                trivia_el += part.get()
            trivia_arr.append(trivia_el)
        film_item['trivia'] = trivia_arr

    def parse_film_reviews(self, film_item, response):
        reviews = response.css(".flatReview")
        num_reviews = len(reviews)
        review_arr = []
        for i in range(num_reviews):
            title = response.xpath(
                "//div[@class='flatReview'][" + str(i + 1) + "]/div[1]/div[@class='flatReview__title']/a/text()").get()
            author = response.xpath(
                "//div[@class='flatReview'][" + str(i + 1) + "]/div[1]/div[@class='flatReview__author']/a/text()").get()
            text = response.xpath("//div[@class='flatReview'][" + str(i + 1) + "]/div[2]/text()").get()
            review_arr.append(dict(
                title=title,
                author=author.strip() if author is not None else "anonymous",
                text=text
            ))
        film_item['viewer_ratings'] = review_arr