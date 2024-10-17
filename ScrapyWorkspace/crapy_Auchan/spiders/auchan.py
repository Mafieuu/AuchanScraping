import scrapy

class AuchanSpider(scrapy.Spider):
    name = "auchan"
    allowed_domains = ['auchan.sn']
    start_urls = ['https://www.auchan.sn/']  

    def parse(self, response):
        # Récupérer les catégories dans le menu déroulant
        categories = response.css('#top-menu li.category.menu-item')
        for category in categories:
            category_name = category.css('a span.link-label::text').get()
            subcategories = category.css('ul.top-menu.menu-depth1-list li.category')
            
            # Si la catégorie a des sous-catégories, scraper les sous-catégories
            if subcategories:
                for subcategory in subcategories:
                    subcategory_name = subcategory.css('a span::text').get()
                    subcategory_url = subcategory.css('a::attr(href)').get()
                    yield response.follow(subcategory_url, callback=self.parse_category, meta={'category': category_name, 'subcategory': subcategory_name})
            else:
                category_url = category.css('a::attr(href)').get()
                yield response.follow(category_url, callback=self.parse_category, meta={'category': category_name}) # a revoir pourquoi null pour ce sub_categorie

    def parse_category(self, response):
        category = response.meta['category']
        subcategory = response.meta.get('subcategory', None)# si pas de subcategorie alors subcategory=None
        
        # Récupérer les produits sur cette page
        products = response.css('article.product-miniature')
        for product in products:
            product_id = product.css('article::attr(data-id-product)').get()
            title = product.css('h2.product-title a::text').get()
            price = product.css('span.price::text').get()
            old_price = product.css('span.regular-price::text').get() is not None
            image_url = product.css('a.thumbnail img::attr(data-full-size-image-url)').get()
            is_out_of_stock = product.css('span.rupture::text').get() is not None # si la balise n'existe pas return None

            yield {
                'category': category,
                'subcategory': subcategory,
                'product_id': product_id,
                'title': title,
                'price': price,
                'old_price': old_price,
                'image_url': image_url,
                'is_out_of_stock': is_out_of_stock,
            }
        
        # Pagination
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'category': category, 'subcategory': subcategory})

    def parse_promotions(self, response):
        # Scraping de la page "Promotions"
        promotions_url = 'https://www.auchan.sn/promotions'
        yield response.follow(promotions_url, callback=self.parse_category, meta={'category': 'Promotions'})
        # les produits ayant subcategory=promotions seront compte deux fois.
