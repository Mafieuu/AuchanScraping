import scrapy
from datetime import datetime


class AuchanSpider(scrapy.Spider):
    name = "auchan"
    allowed_domains = ['auchan.sn']
    start_urls = ['https://www.auchan.sn']

    def parse(self, response):
        # Dans le menu deroulant, recup les infos des categories
        categories = response.css('#top-menu li')
        for category in categories:
            category_name = category.css('a span.link-label::text').get()
            category_id = category.attrib.get('id').strip("abcdefghijklmnopqrstuvwxyw- ")  # on recup que les numero
            subcategories = category.css('ul.top-menu.menu-depth1-list li')

            # Si la catégorie a des sous-catégories, scraper les sous-catégories
            if subcategories:
                for subcategory in subcategories:
                    subcategory_name = subcategory.css('a span::text').get()
                    subcategory_url = subcategory.css('a::attr(href)').get()
                    subcategory_id = subcategory.attrib.get('id').strip("abcdefghijklmnopqrstuvwxyw- ")
                    yield response.follow(subcategory_url, callback=self.parse_category,
                                          meta={'category': category_name, 'subcategory': subcategory_name,
                                                'category_id': category_id, 'subcategory_id': subcategory_id})

            else:
                category_url = category.css('a::attr(href)').get()
                yield response.follow(category_url, callback=self.parse_category,
                                      meta={'category': category_name, 'category_id': category_id})

    def parse_category(self, response):
        _id_subcategorie_forcing = int(
            response.meta.get('category_id')) + 1000  # pour les categorie n'ayant pas de sub categor
        _id_subcategorie_forcing = str(_id_subcategorie_forcing)
        category = response.meta['category']
        subcategory = response.meta.get('subcategory', response.meta[
            'category'])  # si pas de subcategorie alors subcategory=nom categorie
        subcategory_id = response.meta.get('subcategory_id', _id_subcategorie_forcing)
        category_id = response.meta.get('category_id')

        # Récupérer les produits sur cette page
        products = response.css('article.product-miniature')
        for product in products:
            product_id = product.css('article::attr(data-id-product)').get()
            title = product.css('h2.product-title a::text').get()
            price = product.css('span.price::text').get()
            price = price.strip()

            # Les problemes

            is_old_price = product.css('span.regular-price::text').get() is not None
            #
            # Une etude munitieuse du site de Auchan nous a permis de comprendre que pour qu'un produit soit en rupture de stock
            # elle doit etre en promotion mais aussi ne pas avoir un <div class="miniature-notif.notif-discount.discount-amount.discount-product.prio2"
            #
            #
            #
            #
            #
            # On a la confirmations que Auchan met a jour sa base de donne, certains produits en rupture de stocke
            # sont supprimme oubien omis de la categorie rupture de stocke
            # parfois (22/10/2024 15h) on a 6 produits en rupture de stocke et parfois zero
            # Le code marche
            #
            #
            if is_old_price:
                old_price = product.css('span.regular-price::text').get()
                is_out_of_stock = not product.css(
                    'div.miniature-notif.notif-discount.discount-amount.discount-product.prio2').get() is not None
                # si un produit est en reduction et qu'il n'a pas le fameux div alors il est en rupture de stock
            else:
                old_price = "Not concerned"  # a revoir si necessaire
                is_out_of_stock = False

            image_url = product.css('a.thumbnail img::attr(data-full-size-image-url)').get()
            # old_reduct_promo=product.css('div.miniature-notif notif-discount discount-amount discount-product prio2::text').get
            # if old_reduct_promo is None:
            #     is_out_of_stock = True#product.css('span.rupture::text').get() is not None
            # else:
            #     is_out_of_stock=False
            #          # si la balise n'existe pas return None

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
                "scraping_date": datetime.now().strftime('%Y-%m-%d')
            }
        # checker tous les links de la page
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category,
                                  meta={'category': category, 'subcategory': subcategory,
                                        'subcategory_id': subcategory_id, 'category_id': category_id})
# pour reconnaitre les produits qui sont en promotion suffit de regarder old_price