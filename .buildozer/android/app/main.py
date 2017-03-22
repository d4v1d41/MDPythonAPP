# -*- coding: iso-8859-1 -*-
import mechanize
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.theming import ThemeManager
from kivymd.textfields import MDTextField
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.window import Window
from plyer import vibrator

Window.softinput_mode = 'below_target'

name1= str()
sr= str()
def datascrape(exp, anioexp, dia, mes, anio):
    # creating br and setting up
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open("http://www.migraciones.gov.ar/accesible/consulta_tramite/form_inicial.php")
    browser.select_form(nr=0)
    # filling forms
    browser.form['exp'] = exp
    browser.form['anioEXP'] = [anioexp]
    browser.form['dia'] = dia
    browser.form['mes'] = mes
    browser.form['anio'] = anio
    browser.submit()
    data = browser.response()
    sr = str(data.read())
    # analyze for getting name of user
    nam0 = ''.join(sr)
    nam0 = nam0[nam0.index('nombre"'):nam0.index('tipo_tramite')]
    nam0 = nam0[nam0.index('value="'):nam0.index('">')]
    nam0= nam0[7::]
    # analyze for getting last name of user
    nam = ''.join(sr)
    nam = nam[nam.index('name="apellido"'):nam.index('tipo_tramite'):]
    nam = nam[nam.index('value="'):nam.index('">'):]
    nam= nam[7::]
    # getting status and depuring
    sr = sr[sr.index('estado" value="'):sr.index('<input type="hidden" name="delegacion"'):]
    k=[sr]
    k= [i.replace('estado" value="', '') for i in k]
    k= [i.replace('">','') for i in k]
    k=map(lambda s: s.strip(), k)
    global sr
    sr= (k[0]).decode('iso-8859-1').strip()
    # same here, setting up nam1 as global variable, replacing the before-declared global value, that is...
    # formatting the name to get the complete one
    global name1
    name1 = (nam0 + " " + nam).decode('iso-8859-1')

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem
NavigationLayout:
    id: nav_layout
    txt1:txt1
    MDNavigationDrawer:
        id: nav_drawer
        txt1:txt1
        NavigationDrawerToolbar:
            title: "Opciones"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: u"Consulta rápida"
            on_release: app.root.ids.scr_mngr.current = 'Consulta'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Perfiles"
            on_release: app.root.ids.scr_mngr.current = 'Perfiles'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Agregar Perfiles"
            on_release: app.root.ids.scr_mngr.current = 'AgregarP'
    BoxLayout:
        txt1:txt1
        orientation: 'vertical'
        Toolbar:
            txt1:txt1
            id: toolbar
            title: 'Migraciones Argentina'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            txt1:txt1
            id: scr_mngr
            Screen:
                txt1:txt1
                name: 'Consulta'
                ScrollView:
                    txt1:txt1
                    BoxLayout:
                        txt1:txt1
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        Image:
                            source:'data/img/title.png'
                            size_hint_y: None
                            padding: dp(48)
                        GridLayout:
                            cols:2
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(24)
                            spacing: 4
                            MDTextField:
                                id:txt1
                                text:''
                                hint_text: u"Número de exp."
                                required:True
                                helper_text_mode: "on_error"
                            MDTextField:
                                id:txt2
                                hint_text: u"Año de exp."
                                required:True
                                helper_text_mode: "on_error"
                        GridLayout:
                            cols:3
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(24)
                            spacing: 4
                            MDTextField:
                                id:txt3
                                hint_text: u"Día de nac."
                                required:True
                                helper_text_mode: "on_error"
                            MDTextField:
                                id:txt4
                                hint_text: "Mes de nac."
                                required:True
                                helper_text_mode: "on_error"
                            MDTextField:
                                id:txt5
                                hint_text: u"Año de nac."
                                required:True
                                helper_text_mode: "on_error"
                        MDRaisedButton:
                            text: u"Consulta rápida"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release: app.loading(txt1.text,txt2.text,txt3.text,txt4.text,txt5.text);txt1.text="";txt2.text="";txt3.text="";txt4.text="";txt5.text=""
            Screen:
                name: 'Perfiles'
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        spacing:dp(14)
                        Image:
                            source:'data/img/title.png'
                            size_hint_y: None
                            padding: dp(48)
                        MDRaisedButton:
                            text: u"Consultar Perfil 1"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release: app.poppro1()
                        MDRaisedButton:
                            text: u"Consultar Perfil 2"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release: app.poppro2()
                        MDRaisedButton:
                            text: u"Consultar Perfil 3"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release: app.poppro3()
                        MDRaisedButton:
                            text: u"Consultar Perfil 4"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release: app.poppro4()
                        MDFloatingActionButton:
                            id:                    float_act_btn
                            icon:                'plus'
                            opposite_colors:    True
                            elevation_normal:    8
                            pos_hint:            {'center_x': 0.5, 'center_y': 0.2}
                            on_release:app.root.ids.scr_mngr.current = 'AgregarP'

            Screen:
                name: 'AgregarP'
                MDTabbedPanel:
                    id: tab_panel
                    tab_display_mode:'icons'
                    MDTab:
                        name: 'Perfil 1'
                        icon: "account-plus"
                        ScrollView:
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                Image:
                                    source:'data/img/title.png'
                                    size_hint_y: None
                                    padding: dp(48)
                                GridLayout:
                                    cols:2
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(14)
                                    spacing: 4
                                    MDTextField:
                                        id:expp1
                                        hint_text: u"Número de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:aexpp1
                                        hint_text: u"Año de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                GridLayout:
                                    cols:3
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(11)
                                    spacing: 4
                                    MDTextField:
                                        id:dexpp1
                                        hint_text: u"Día de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:mexpp1
                                        hint_text: "Mes de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:anxpp1
                                        hint_text: u"Año de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                MDRaisedButton:
                                    text: u"Añadir Perfil 1"
                                    elevation_normal: 2
                                    opposite_colors: True
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                                    on_release: app.loadingp1(expp1.text,aexpp1.text,dexpp1.text,mexpp1.text,anxpp1.text);expp1.text="";aexpp1.text="";dexpp1.text="";mexpp1.text="";anxpp1.text=""

                    MDTab:
                        name: 'Perfil 2'
                        icon: "account-plus"
                        ScrollView:
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                Image:
                                    source:'data/img/title.png'
                                    size_hint_y: None
                                    padding: dp(48)
                                GridLayout:
                                    cols:2
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(14)
                                    spacing: 4
                                    MDTextField:
                                        id:expp2
                                        hint_text: u"Número de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:aexpp2
                                        hint_text: u"Año de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                GridLayout:
                                    cols:3
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(11)
                                    spacing: 4
                                    MDTextField:
                                        id:dexpp2
                                        hint_text: u"Día de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:mexpp2
                                        hint_text: "Mes de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:anxpp2
                                        hint_text: u"Año de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                MDRaisedButton:
                                    text: u"Añadir Perfil 2"
                                    elevation_normal: 2
                                    opposite_colors: True
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                                    on_release: app.loadingp2(expp2.text,aexpp2.text,dexpp2.text,mexpp2.text,anxpp2.text);expp2.text="";aexpp2.text="";dexpp2.text="";mexpp2.text="";anxpp2.text=""

                    MDTab:
                        name: 'Perfil 3'
                        icon: "account-plus"
                        ScrollView:
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                Image:
                                    source:'data/img/title.png'
                                    size_hint_y: None
                                    padding: dp(48)
                                GridLayout:
                                    cols:2
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(14)
                                    spacing: 4
                                    MDTextField:
                                        id:expp3
                                        hint_text: u"Número de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:aexpp3
                                        hint_text: u"Año de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                GridLayout:
                                    cols:3
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(11)
                                    spacing: 4
                                    MDTextField:
                                        id:dexpp3
                                        hint_text: u"Día de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:mexpp3
                                        hint_text: "Mes de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:anxpp3
                                        hint_text: u"Año de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                MDRaisedButton:
                                    text: u"Añadir Perfil 3"
                                    elevation_normal: 2
                                    opposite_colors: True
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                                    on_release: app.loadingp3(expp3.text,aexpp3.text,dexpp3.text,mexpp3.text,anxpp3.text);expp3.text="";aexpp3.text="";dexpp3.text="";mexpp3.text="";anxpp3.text=""
                    MDTab:
                        name: 'Perfil 4'
                        icon: "account-plus"

                        ScrollView:
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                Image:
                                    source:'data/img/title.png'
                                    size_hint_y: None
                                    padding: dp(48)
                                GridLayout:
                                    cols:2
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(14)
                                    spacing: 4
                                    MDTextField:
                                        id:expp4
                                        hint_text: u"Número de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:aexpp4
                                        hint_text: u"Año de exp."
                                        required:True
                                        helper_text_mode: "on_error"
                                GridLayout:
                                    cols:3
                                    orientation: 'vertical'
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(11)
                                    spacing: 8
                                    MDTextField:
                                        id:dexpp4
                                        hint_text: u"Día de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:mexpp4
                                        hint_text: "Mes de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                    MDTextField:
                                        id:anxpp4
                                        hint_text: u"Año de nac."
                                        required:True
                                        helper_text_mode: "on_error"
                                MDRaisedButton:
                                    text: u"Añadir Perfil 4"
                                    elevation_normal: 2
                                    opposite_colors: True
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                                    on_release: app.loadingp4(expp4.text,aexpp4.text,dexpp4.text,mexpp4.text,anxpp4.text);expp4.text="";aexpp4.text="";dexpp4.text="";mexpp4.text="";anxpp4.text=""
            Screen:
                name: 'nav_drawer'
                NavDrawerH:
                    # NavigationDrawerToolbar:
                    #     title: "Navigation Drawer Widgets"
                    NavigationDrawerIconButton:
                        icon: 'checkbox-blank-circle'
                        text: "Badge text ---->"
                        badge_text: "99+"
                    NavigationDrawerIconButton:
                        active_color_type: 'accent'
                        text: "Accent active color"
                    NavigationDrawerIconButton:
                        active_color_type: 'custom'
                        text: "Custom active color"
                        active_color: [1, 0, 1, 1]
                    NavigationDrawerIconButton:
                        use_active: False
                        text: "Use active = False"
                    NavigationDrawerIconButton:
                        text: "Different icon"
                        icon: 'alarm'
                    NavigationDrawerDivider:
                    NavigationDrawerSubheader:
                        text: "NavigationDrawerSubheader"
                    NavigationDrawerIconButton:
                        text: "NavigationDrawerDivider \/"
                    NavigationDrawerDivider:

'''


store = JsonStore('data/db/dataMigra.json')
store2 = JsonStore('data/db/data2Migra.json')
store3 = JsonStore('data/db/data3Migra.json')
store4 = JsonStore('data/db/data4Migra.json')


exp= ''
anex=''
diana=''
mesna=''
ani= ''

class NavDrawerH(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)

class MigracionesP(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Migraciones Argentina"


    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        return main_widget

# !!!!!!!!!!     CONSULTA RAPIDA RESULTS !!!!!!!!!!!

    def results_dialog(self, dt):
        try:
            datascrape(exp, anex, diana, mesna, ani)
            priin= "El estado de tramite de " + name1+" es: "+ sr
        except mechanize._form.ItemNotFoundError:
            priin= 'Hubo un problema, verifique los datos ingresados'
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=priin,
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Estado de tramite",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(350),
                               auto_dismiss=True)

        self.dialog.add_action_button("Ok",
                                     action=lambda *x: self.dialog.dismiss())
        self.dialog2.dismiss()
        vibrator.vibrate(0.2)
        self.dialog.open()

# POPUP QUERY RAPIDO !!!!!!!!!!!!!!!!!!!!
    def loading(self, ex, aex, dian, mesn, an):
        content2 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=u"Procesando información",
                          size_hint_y=None,
                          valign='top')
        global exp, anex, diana, mesna, ani
        exp= ex.strip()
        anex= aex.strip()
        diana= dian.strip()
        mesna= mesn.strip()
        ani= an.strip()
        content2.bind(texture_size=content2.setter('size'))
        self.dialog2 = MDDialog(title="Consulta",
                               content=content2,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.dialog2.open()
        Clock.schedule_once(self.results_dialog, 1.5)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! PERFIL 1 - GENERAL !!!!!!!!!!!!!!!!!!!!!!!!!!!!111
# CONSULTA PERFIL 1
        # popup query profile 1 Processing popup and setting global variables to use it in consul1, that is the actual func

    def consul1(self, dt):
        try:
            datascrape(store.get('prof1')['exp'], store.get('prof1')['anioExp'], store.get('prof1')['dia'], store.get('prof1')['mes'], store.get('prof1')['anio'])
            priin1 = "El estado de tramite de " + name1 + " : " + sr
        except KeyError:
            priin1 = "Hay un problema, reingrese los datos del perfil"
        content01 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=priin1,
                          size_hint_y=None,
                          valign='top')
        content01.bind(texture_size=content01.setter('size'))
        self.dialog01 = MDDialog(title="Estado tramite",
                               content=content01,
                               size_hint=(.8, None),
                               height=dp(350),
                               auto_dismiss=False)

        self.dialog01.add_action_button("Ok",
                                      action=lambda *x: self.dialog01.dismiss())
        self.popuppro1.dismiss()
        vibrator.vibrate(0.2)
        self.dialog01.open()
# !!!!!!!!!!!!!!!!!!      POPUP AVISO QUERY PERFIL 1     !!!!!!!!!!!!!!!!!!
    def poppro1(self):
        contentpoppro1 = MDLabel(font_style='Body1',
                                 theme_text_color='Secondary',
                                 text=u"Procesando información",
                                 size_hint_y=None,
                                 valign='top')
        contentpoppro1.bind(texture_size=contentpoppro1.setter('size'))
        self.popuppro1 = MDDialog(title="Consulta",
                                  content=contentpoppro1,
                                  size_hint=(.8, None),
                                  height=dp(200),
                                  auto_dismiss=False)
        self.popuppro1.open()
        Clock.schedule_once(self.consul1, 1.5)
#!!!!!!!!!!!!!!!!!!! PERFIL 1- CARGA  GUARDADO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Cierra popup aviso carga perfil
    def deshacer1(self, dt):
        self.dialog3.dismiss()
# CARGA PERFIL 1 y AVISO
    def loadingp1(self, ex, aex, dian, mesn, an):
        content3 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Su perfil se ha guardado",
                          size_hint_y=None,
                          valign='top')
        expe= ex.strip()
        anex= aex.strip()
        diana= dian.strip()
        mesna= mesn.strip()
        ani= an.strip()
        store.put('prof1', exp=expe, anioExp=anex, dia=diana, mes=mesna, anio=ani)
        content3.bind(texture_size=content3.setter('size'))
        self.dialog3 = MDDialog(title="Perfil",
                               content=content3,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.dialog3.open()
        vibrator.vibrate(0.2)
        Clock.schedule_once(self.deshacer1, 2.7)

# !!!!!!!!!!!!!!!!!!!!!!!! Perfil 2 !!!!!!!!!!!!!!!!!!!!!!!!!

# CONSULTA PERFIL 2
    def consul2(self, dt):
        try:
            datascrape(store2.get('prof2')['exp'], store2.get('prof2')['anioExp'], store2.get('prof2')['dia'], store2.get('prof2')['mes'], store2.get('prof2')['anio'])
            priin2 = "El estado de tramite de " + name1 + " : " + sr
        except KeyError:
            priin2 = "Hay un problema, reingrese los datos del perfil"
        content002 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=priin2,
                          size_hint_y=None,
                          valign='top')
        content002.bind(texture_size=content002.setter('size'))
        self.dialog002 = MDDialog(title="Estado tramite",
                               content=content002,
                               size_hint=(.8, None),
                               height=dp(350),
                               auto_dismiss=False)

        self.dialog002.add_action_button("Ok",
                                      action=lambda *x: self.dialog002.dismiss())
        self.popuppro2.dismiss()
        vibrator.vibrate(0.2)
        self.dialog002.open()
# POPUP CONSULTA PERFIL 2
    def poppro2(self):
        contentpoppro2 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=u"Procesando información",
                          size_hint_y=None,
                          valign='top')
        contentpoppro2.bind(texture_size=contentpoppro2.setter('size'))
        self.popuppro2 = MDDialog(title="Consulta",
                               content=contentpoppro2,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.popuppro2.open()
        Clock.schedule_once(self.consul2, 1.5)
# !!!!!!!!!!!! PERFIL 2 - CARGA PERFIL!!!!!!!!!!!!!!!!!!!!!
# cierra popup de aviso carga perfil 2
    def deshacer2(self, dt):
        self.dialog02.dismiss()

# Carga datos PERFIL 2
    def loadingp2(self, ex, aex, dian, mesn, an):
        content02 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Su perfil se ha guardado",
                          size_hint_y=None,
                          valign='top')
        expe= ex.strip()
        anex= aex.strip()
        diana= dian.strip()
        mesna= mesn.strip()
        ani= an.strip()
        store2.put('prof2', exp=expe, anioExp=anex, dia=diana, mes=mesna, anio=ani)
        content02.bind(texture_size=content02.setter('size'))
        self.dialog02 = MDDialog(title="Perfil",
                               content=content02,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.dialog02.open()
        vibrator.vibrate(0.2)
        Clock.schedule_once(self.deshacer2, 2.7)

#  $$$$$$$$$$$$$$$    FIN PERFIL 2       $$$$$$$$$
# !!!!!!!!!!!!!!!! PERFIL 3    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CONSULTA P3 y AVISO
    def consul3(self, dt):
        try:
            datascrape(store3.get('prof3')['exp'], store3.get('prof3')['anioExp'], store3.get('prof3')['dia'],
                       store3.get('prof3')['mes'], store3.get('prof3')['anio'])
            priin3 = "El estado de tramite de " + name1 + " : " + sr
        except KeyError:
            priin3 = "Hay un problema, reingrese los datos del perfil"
        content003 = MDLabel(font_style='Body1',
                             theme_text_color='Secondary',
                             text=priin3,
                             size_hint_y=None,
                             valign='top')
        content003.bind(texture_size=content003.setter('size'))
        self.dialog003 = MDDialog(title="Estado tramite",
                                  content=content003,
                                  size_hint=(.8, None),
                                  height=dp(350),
                                  auto_dismiss=False)

        self.dialog003.add_action_button("Ok",
                                         action=lambda *x: self.dialog003.dismiss())
        self.popuppro3.dismiss()
        vibrator.vibrate(0.2)
        self.dialog003.open()

# POPUP PROCESANDO INFO QUERY P3
    def poppro3(self):
        contentpoppro3 = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=u"Procesando información",
                          size_hint_y=None,
                          valign='top')
        contentpoppro3.bind(texture_size=contentpoppro3.setter('size'))
        self.popuppro3 = MDDialog(title="Consulta",
                               content=contentpoppro3,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)
        self.popuppro3.open()
        Clock.schedule_once(self.consul3, 1.5)

    # !!!!!!!!!!!! PERFIL 3 - CARGA PERFIL!!!!!!!!!!!!!!!!!!!!!
    # cierra popup de aviso carga perfil 3
    def deshacer3(self, dt):
        self.dialog03.dismiss()

        # Carga datos PERFIL 2

    def loadingp3(self, ex, aex, dian, mesn, an):
        content03 = MDLabel(font_style='Body1',
                            theme_text_color='Secondary',
                            text="Su perfil se ha guardado",
                            size_hint_y=None,
                            valign='top')
        expe = ex.strip()
        anex = aex.strip()
        diana = dian.strip()
        mesna = mesn.strip()
        ani = an.strip()
        store3.put('prof3', exp=expe, anioExp=anex, dia=diana, mes=mesna, anio=ani)
        content03.bind(texture_size=content03.setter('size'))
        self.dialog03 = MDDialog(title="Perfil",
                                 content=content03,
                                 size_hint=(.8, None),
                                 height=dp(200),
                                 auto_dismiss=False)
        self.dialog03.open()
        vibrator.vibrate(0.2)
        Clock.schedule_once(self.deshacer3, 2.7)


# &&&&&&&&&& FIN PERFIL 3 %%%%%%%%%%

    # !!!!!!!!!!!!!!!! PERFIL 4    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CONSULTA P4 y AVISO
    def consul4(self, dt):
        try:
            datascrape(store4.get('prof4')['exp'], store4.get('prof4')['anioExp'], store4.get('prof4')['dia'],
                       store4.get('prof4')['mes'], store4.get('prof4')['anio'])
            priin4 = "El estado de tramite de " + name1 + " : " + sr
        except KeyError:
            priin4 = "Hay un problema, reingrese los datos del perfil"
        content004 = MDLabel(font_style='Body1',
                             theme_text_color='Secondary',
                             text=priin4,
                             size_hint_y=None,
                             valign='top')
        content004.bind(texture_size=content004.setter('size'))
        self.dialog004 = MDDialog(title="Estado tramite",
                                  content=content004,
                                  size_hint=(.8, None),
                                  height=dp(350),
                                  auto_dismiss=False)

        self.dialog004.add_action_button("Ok",
                                         action=lambda *x: self.dialog004.dismiss())
        self.popuppro4.dismiss()
        vibrator.vibrate(0.2)
        self.dialog004.open()

        # POPUP PROCESANDO INFO QUERY P4

    def poppro4(self):
        contentpoppro4 = MDLabel(font_style='Body1',
                                 theme_text_color='Secondary',
                                 text=u"Procesando información",
                                 size_hint_y=None,
                                 valign='top')
        contentpoppro4.bind(texture_size=contentpoppro4.setter('size'))
        self.popuppro4 = MDDialog(title="Consulta",
                                  content=contentpoppro4,
                                  size_hint=(.8, None),
                                  height=dp(200),
                                  auto_dismiss=False)
        self.popuppro4.open()
        Clock.schedule_once(self.consul4, 1.5)

    # !!!!!!!!!!!! PERFIL 4 - CARGA PERFIL!!!!!!!!!!!!!!!!!!!!!
    # cierra popup de aviso carga perfil 4
    def deshacer4(self, dt):
        self.dialog04.dismiss()

        # Carga datos PERFIL 4

    def loadingp4(self, ex, aex, dian, mesn, an):
        content04 = MDLabel(font_style='Body1',
                            theme_text_color='Secondary',
                            text="Su perfil se ha guardado",
                            size_hint_y=None,
                            valign='top')
        expe = ex.strip()
        anex = aex.strip()
        diana = dian.strip()
        mesna = mesn.strip()
        ani = an.strip()
        store4.put('prof4', exp=expe, anioExp=anex, dia=diana, mes=mesna, anio=ani)
        content04.bind(texture_size=content04.setter('size'))
        self.dialog04 = MDDialog(title="Perfil",
                                 content=content04,
                                 size_hint=(.8, None),
                                 height=dp(200),
                                 auto_dismiss=False)
        self.dialog04.open()
        vibrator.vibrate(0.2)
        Clock.schedule_once(self.deshacer4, 2.7)


        # &&&&&&&&&& FIN PERFIL 4 %%%%%%%%%%



        # SHIT ____________________________>



    # SHIT ____________________________>


    def on_pause(self):
        return True

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    MigracionesP().run()
