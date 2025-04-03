import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab06"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.ddAnno = None
        self.ddBrand = None
        self.ddRetailer = None
        self.btnTopVendite = None
        self.btnAnalizzaVendite = None

    def change_theme(self, e):
        if self._page.theme_mode == ft.ThemeMode.DARK:
            self._page.theme_mode = ft.ThemeMode.LIGHT
            self.theme.label = "Light Theme"
        else:
            self._page.theme_mode = ft.ThemeMode.DARK
            self.theme.label = "Dark Theme"
        self._page.update()

    def load_interface(self):
        self.theme = ft.Switch(label = "Dark Theme", on_change = self.change_theme)
        self._title = ft.Text("Analizza Vendite", color="grey", size=24)
        self._page.controls.append(ft.Row([self._title], ft.MainAxisAlignment.CENTER))
        self._page.controls.append(ft.Row([self.theme], ft.MainAxisAlignment.START))
        self.ddAnno = ft.Dropdown(label = "anno",
                                  width = 300,
                                  on_change = self._controller.handleAnno
                                )
        self._controller.fillddAnno()
        self.ddBrand = ft.Dropdown(label = "brand",
                                   width = 300,
                                   on_change = self._controller.handleBrand)
        self._controller.fillddBrand()
        self.ddRetailer = ft.Dropdown(label = "retailer",
                                      width = 500,
                                      on_change = self._controller.handleRetailer)
        self._controller.fillddRetailer()
        self.btnTopVendite = ft.ElevatedButton(text = "Top vendite",
                                               width = 200,
                                               on_click = self._controller.handleTopVendite)
        self.btnStatisticheVendite = ft.ElevatedButton(text = "Analizza Vendite",
                                                    width = 200,
                                                    on_click = self._controller.handleStatisticheVendite)
        self.lvTxtOut = ft.ListView(expand=True)
        self._page.add(ft.Row([self.ddAnno, self.ddBrand, self.ddRetailer], alignment = ft.MainAxisAlignment.CENTER))
        self._page.add(ft.Row([self.btnTopVendite, self.btnStatisticheVendite], alignment = ft.MainAxisAlignment.CENTER))
        self._page.add( self.lvTxtOut)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def alert(self, message):
        dlg = ft.AlertDialog(title = ft.Row([ft.Icon(ft.icons.ERROR, color = "red"), ft.Text("Errore:", color = "red")]),
                             content = ft.Text(message, color = "red"),
                             actions = [ft.TextButton("OK", on_click=lambda e: self.closealert(dlg))])
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def closealert(self, dlg):
        dlg.open = False
        self._page.update()

    def update_page(self):
        self._page.update()
