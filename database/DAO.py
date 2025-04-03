from database.DB_connect import DBConnect
from datetime import datetime
from model.retailer import Retailer

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAnni():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """SELECT DISTINCT YEAR(Date)
                    FROM go_daily_sales
                    ORDER BY YEAR(Date);"""
        cursor.execute(query)
        intAnni = []
        for tupla in cursor: #tupla è già un objData
            intAnni.append(tupla[0])
        cursor.close()
        cnx.close()
        return intAnni

    @staticmethod
    def getAllBrands():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """SELECT DISTINCT Product_brand
                   FROM go_products;"""
        cursor.execute(query)
        strBrand = []
        for str in cursor:
            strBrand.append(str[0])
        cursor.close()
        cnx.close()
        return strBrand

    @staticmethod
    def getAllRetailers():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT *
                    FROM go_retailers;"""
        cursor.execute(query)
        objRetailer = []
        for obj in cursor:
            objRetailer.append(Retailer(**obj))
        cursor.close()
        cnx.close()
        return objRetailer

    @staticmethod
    def getTopVendite(intAnno, strBrand, intRetailer):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT gds.Date AS data, 
                           gp.Product_number AS prodotto, 
                           gr.Retailer_code AS retailer, 
                           SUM(gds.Quantity * gds.Unit_sale_price) AS ricavo 
                    FROM go_daily_sales gds
                    JOIN go_products gp ON gds.Product_number = gp.Product_number
                    JOIN go_retailers gr ON gds.Retailer_code = gr.Retailer_code
                    WHERE 
                        YEAR(gds.Date) = COALESCE(%s, YEAR(gds.Date)) AND
                        gp.Product_brand = COALESCE(%s, gp.Product_brand) AND
                        gr.Retailer_code = COALESCE(%s, gr.Retailer_code)
                    GROUP BY gds.Date, gp.Product_number, gr.Retailer_code
                    ORDER BY ricavo DESC
                    LIMIT 5;"""
        cursor.execute(query, (intAnno, strBrand, intRetailer))
        dizionarioDBRS = []
        for dizionario in cursor:
            dizionarioDBRS.append(dizionario)
        cnx.close()
        cursor.close()
        return dizionarioDBRS

    @staticmethod
    def getStatisticheVendite(intAnno, strBrand, intRetailer):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT 
                    COALESCE(SUM(gds.Quantity * gds.Unit_sale_price), 0) AS Giro_d_affari,
                    COUNT(gds.Retailer_code) AS Numero_vendite,
                    COUNT(DISTINCT gds.Retailer_code) AS Numero_retailers_coinvolti,
                    COUNT(DISTINCT gds.Product_number) AS Numero_prodotti_coinvolti
                FROM go_daily_sales gds
                JOIN go_retailers gr ON gds.Retailer_code = gr.Retailer_code
                JOIN go_products gp ON gds.Product_number = gp.Product_number
                WHERE 
                    YEAR(gds.Date) = COALESCE(%s, YEAR(gds.Date)) AND
                    gp.Product_brand = (COALESCE(%s, gp.Product_brand)) AND
                    gr.Retailer_code = (COALESCE(%s, gr.Retailer_code)) ;"""
        cursor.execute(query, (intAnno, strBrand, intRetailer))
        dizionarioAVRP = cursor.fetchone()
        cnx.close()
        cursor.close()
        return dizionarioAVRP

if __name__ == '__main__':
    print(DAO.getTopVendite(2018, None, None))
    print(DAO.getStatisticheVendite(None, None, 1205))
#in caso di passaggio di strAnno/strRetailer SQL cercherà di fare un cast della stringa a un intero.









