from decimal import Decimal
import flet as ft
from UI.view import View
from model import retailer
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._anno = None
        self._brand = None
        self._retailer = None

    def fillddAnno(self):
        self._view.ddAnno.options.append(
            ft.dropdown.Option(text="Nessun filtro", key=None, data=None, on_click=self.selectedAnno))
        intAnno = self._model.getAllAnni()
        for year in intAnno:
            self._view.ddAnno.options.append(ft.dropdown.Option(key = year,
                                                                text = year,
                                                                data = year,
                                                                on_click = self.selectedAnno))
    def selectedAnno(self, e):
        self._anno = e.control.data

    def fillddBrand(self):
        self._view.ddBrand.options.append(
            ft.dropdown.Option(text="Nessun filtro", key=None, data=None, on_click=self.selectedBrand))
        strBrand = self._model.getAllBrands()
        for str in strBrand:
            self._view.ddBrand.options.append(ft.dropdown.Option(key = str,
                                                                 text = str,
                                                                data = str,
                                                                 on_click = self.selectedBrand))
    def selectedBrand(self, e):
        self._brand = e.control.data

    def fillddRetailer(self):
        self._view.ddRetailer.options.append(
            ft.dropdown.Option(text="Nessun filtro", key=None, data=None, on_click=self.selectedRetailer))
        objRetailer = self._model.getAllRetailers()
        for obj in objRetailer:
            self._view.ddRetailer.options.append(ft.dropdown.Option(key = obj,
                                                                text = obj.Retailer_name,
                                                                 data = obj,
                                                                on_click = self.selectedRetailer))
    def selectedRetailer(self, e):
        self._retailer = e.control.data

    def handleAnno(self, e):
        pass

    def handleBrand(self, e):
        pass

    def handleRetailer(self, e):
        pass

    def handleTopVendite(self, e):
        self._view.lvTxtOut.controls.clear()
        dizionarioDBRS =  self._model.getTopVendite(self._anno, self._brand, self._retailer.Retailer_code if self._retailer else None)
        if len(dizionarioDBRS) == 0:
            self._view.alert("Vendite non esistenti per i dati selezionati")
            return
        for dizionario in dizionarioDBRS:
            self._view.lvTxtOut.controls.append(ft.Text(f"Data: {dizionario['data']}; Ricavo: {dizionario['ricavo']}; Retailer: {dizionario['retailer']}; Product: {dizionario['prodotto']}"))
        self._view.update_page()

    def handleStatisticheVendite(self, e):
        self._view.lvTxtOut.controls.clear()
        dizionarioAVRP = self._model.getStatisticheVendite(self._anno, self._brand,
                                                   self._retailer.Retailer_code if self._retailer else None)
        if (dizionarioAVRP['Giro_d_affari']==Decimal('0.00') and dizionarioAVRP['Numero_vendite'] == 0 and dizionarioAVRP['Numero_retailers_coinvolti'] == 0 and dizionarioAVRP['Numero_prodotti_coinvolti'] == 0) :
            self._view.alert("Vendite non esistenti per i dati selezionati")
        self._view.lvTxtOut.controls.append(ft.Text("Statistiche vendite:"))
        self._view.lvTxtOut.controls.append(ft.Text(f"Giro d'affari: {float(dizionarioAVRP['Giro_d_affari'])}\n Numero vendite: {dizionarioAVRP['Numero_vendite']}\n Numero retailers coinvolti: {dizionarioAVRP['Numero_retailers_coinvolti']}\n Numero prodotti coinvolti: {dizionarioAVRP['Numero_prodotti_coinvolti']}"))
        self._view.update_page()
