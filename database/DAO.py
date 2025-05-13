from database.DB_connect import DBConnect
from model.product import Product


class DAO():


    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select distinct(year(`Date`)) as year
                    from go_daily_sales"""

        cursor.execute(query,)

        for row in cursor:
            res.append(row["year"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select distinct(Product_color) as color
                    from go_products"""

        cursor.execute(query, )

        for row in cursor:
            res.append(row["color"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodesColor(color):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select *
                    from go_products
                    where Product_color = %s"""

        cursor.execute(query, (color,))

        for row in cursor:
            res.append(Product(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def verificaNodi(year, u, v):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []

        query = """select count(distinct(gds.Date)) as tot
                    from go_daily_sales gds, go_daily_sales gds2 
                    where year(gds.Date) = 2015
                    and gds.Product_number = 1110 and gds2.Product_number = 24110
                    and gds.Retailer_code = gds2.Retailer_code and gds.Order_method_code = gds2.Order_method_code """

        cursor.execute(query, (year, u, v))

        for row in cursor:
            res.append((row["tot"]))

        cursor.close()
        conn.close()
        return res



