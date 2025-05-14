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
                    where year(gds.Date) = %s
                    and gds.Product_number = %s and gds2.Product_number = %s
                    and gds.Retailer_code = gds2.Retailer_code
                    and gds.`Date` = gds2.`Date` """

        cursor.execute(query, (year, u, v))


        for row in cursor:
            res.append((row["tot"]))

        cursor.close()
        conn.close()
        if res is None or res[0] == 0:
            return False
        return res



