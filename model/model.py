from database.DAO import DAO

class Model:
    def __init__(self):
        pass

    def getAllAnni(self):
        return DAO.getAllAnni()

    def getAllBrands(self):
        return DAO.getAllBrands()

    def getAllRetailers(self):
        return DAO.getAllRetailers()

    def getTopVendite(self, strAnno, strBrand, intRetailer):
        return DAO.getTopVendite(strAnno, strBrand, intRetailer)

    def getStatisticheVendite(self, strAnno, strBrand, intRetailer):
        return DAO.getStatisticheVendite(strAnno, strBrand, intRetailer)
