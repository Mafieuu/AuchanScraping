# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import pymysql

class CrapyAuchanPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='090302M@ty',
            database='auchan'
        )

        self.cur = self.conn.cursor()

        # self.cur.execute("""CREATE DATABASE IF NOT EXISTS auchan;""")
        # self.cur.execute("""USE auchan;""")

        # Table catégorie
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Categorie(
                idCategorie INTEGER PRIMARY KEY ,
                nomCategorie VARCHAR(100)
            );
        """)

        # Table sous-catégorie
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS SubCategorie(
                idSubCategorie INTEGER PRIMARY KEY ,
                idCategorie INTEGER ,
                FOREIGN KEY (idCategorie) REFERENCES Categorie(idCategorie) ,
                nomSubCategorie VARCHAR(100)
            );
        """)

        # Tableau produit
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Produit (
                idProduit INTEGER PRIMARY KEY,
                idSubCategorie INTEGER ,
                FOREIGN KEY (idSubCategorie) REFERENCES SubCategorie(idSubCategorie) ,
                idCategorie INTEGER ,
                FOREIGN KEY (idCategorie) REFERENCES Categorie(idCategorie) ,
                nomProduit VARCHAR(150),
                imageURL VARCHAR(350)
            );
        """)

        # Table suivi
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Suivi(
                idProduit INTEGER NOT NULL,
                FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
                dateCollecte DATE NOT NULL,
                prix VARCHAR(25) NOT NULL,
                prixPromo VARCHAR(25),
                stock BOOL,
                PRIMARY KEY(idProduit, dateCollecte)
            );
        """)


## Insertion et mise à jour des tables
    def process_item(self, item, spider):

        self.cur.execute("""
            SELECT * FROM Categorie WHERE idCategorie = %s
        """, (item["category_id"],))
        res_category = self.cur.fetchone()

        # if res_category:
        #     spider.logger.warn("Category already in database: %s" % item['category_id'])
        if not res_category:
            self.cur.execute("""
                INSERT INTO Categorie VALUES(%s,%s)""",
                (item["category_id"], item["category"]))
            self.conn.commit()


        ## Insertion et mise à jour de la table SubCategorie
        self.cur.execute("""
            SELECT * FROM SubCategorie WHERE idSubCategorie = %s
        """, (item["subcategory_id"],))
        res_subcategory = self.cur.fetchone()

        # if res_subcategory:
        #     spider.logger.warn("Category already in database: %s" % item['category_id'])
        if not res_subcategory:
            self.cur.execute("""
                INSERT INTO SubCategorie VALUES(%s,%s,%s)""",
                (item["subcategory_id"], item["category_id"], item["subcategory"]))
            self.conn.commit()

        ## Insertion et mise à jour de la table Produit
        self.cur.execute("""
                SELECT * FROM Produit WHERE idProduit = %s
            """, (item["product_id"],))
        res_product = self.cur.fetchone()

        # if res_product:
        #     spider.logger.warn("Category already in database: %s" % item['category_id'])
        if not res_product:
            self.cur.execute("""
                    INSERT INTO Produit VALUES(%s,%s,%s,%s,%s)""",
                             (item["product_id"], item["subcategory_id"], item["category_id"], item["title"], item["image_url"]))
            self.conn.commit()


        ## Insertion et mise à jour de la table Suivi
        self.cur.execute("""
                SELECT * FROM Suivi WHERE idProduit = %s and dateCollecte = %s
            """, (item["product_id"],item["scraping_date"]))
        res_suivi = self.cur.fetchone()

        # if res_suivi:
        #     spider.logger.warn("Category already in database: %s" % item['category_id'])
        if not res_suivi:
            self.cur.execute("""
                    INSERT INTO Suivi VALUES(%s,%s,%s,%s,%s)""",
                    (item["product_id"], item["scraping_date"], item["price"], item["old_price"], item["is_out_of_stock"]))
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()