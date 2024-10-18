import scrapy
from datetime import datetime


class AuchanSpider(scrapy.Spider):
    name = "auchan"
    allowed_domains = ['auchan.sn']
    start_urls = ['https://www.auchan.sn']  

    def parse(self, response):
        # Dans le menu deroulant, recup les infos des categories
        categories =response.css('#top-menu li')
        for category in categories:
            category_name =category.css('a span.link-label::text').get()
            category_id =category.attrib.get('id').strip("abcdefghijklmnopqrstuvwxyw- ") # on recup que les numero
            subcategories =category.css('ul.top-menu.menu-depth1-list li')
            
            # Si la catégorie a des sous-catégories, scraper les sous-catégories
            if subcategories:
                for subcategory in subcategories:
                    subcategory_name =subcategory.css('a span::text').get()
                    subcategory_url =subcategory.css('a::attr(href)').get()
                    subcategory_id=subcategory.attrib.get('id').strip("abcdefghijklmnopqrstuvwxyw- ")
                    yield response.follow(subcategory_url, callback=self.parse_category,meta={'category': category_name, 'subcategory': subcategory_name, 'category_id': category_id, 'subcategory_id':subcategory_id})

            else:
                category_url = category.css('a::attr(href)').get()
                yield response.follow(category_url, callback=self.parse_category, meta={'category': category_name, 'category_id': category_id}) 

    def parse_category(self, response):
        category =response.meta['category']
        subcategory =response.meta.get('subcategory', None)# si pas de subcategorie alors subcategory=None
        subcategory_id =response.meta.get('subcategory_id', None)
        category_id= response.meta.get('category_id', None)

        
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
                'category_id': category_id,
                'category': category,
                'subcategory': subcategory,
                'subcategory_id': subcategory_id,
                'product_id': product_id,
                'title': title,
                'price': price,
                'old_price': old_price,
                'image_url': image_url,
                'is_out_of_stock': is_out_of_stock,
                "scraping_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            }
        # checker tous les links de la page
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'category': category, 'subcategory': subcategory,'subcategory_id': subcategory_id,'category_id': category_id})
# pour reconnaitre les produits qui sont en promotion suffit de regarder old_price