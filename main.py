import json

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, \
    MDExpansionPanelThreeLine
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase

from catar import Content

Builder.load_file('tabela.kv')
Builder.load_file('catar.kv')
Builder.load_file('baseclass/grupoa/team1/convocados.kv')


class BaseScreenView(ThemableBehavior, MDScreen):
    controller = ObjectProperty()
    model = ObjectProperty()
    screen_manager = ObjectProperty()

    def goto_screen(self, screen_name):
        if 'nav_drawer' in self.ids and self.ids.nav_drawer is not None:
            if self.ids.nav_drawer.state == "open":
                self.ids.nav_drawer.set_state("close")
            Clock.schedule_once(
                lambda x: self.transition_to_screen(screen_name), 0.2)

    def transition_to_screen(self, screen):
        self.controller.transition_to_screen(screen)


class RootScreen(BaseScreenView):
    pass


class Tabela(BaseScreenView):
    pass


class Catar(BaseScreenView):
    def on_enter(self, *args):
        for i in range(24):
            self.ids.box.add_widget(
                MDExpansionPanel(
                    icon="assets/images/GrupoA/catar/img.png",
                    content=Content(),
                    panel_cls=MDExpansionPanelThreeLine(
                        text="Text",
                        secondary_text="Secondary text",
                        tertiary_text="Tertiary text",
                    )
                )
            )


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class TeamContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class GenericController:
    def __init__(self, model, view):
        self.view = view(controller=self)
        self.model = model

    def get_screen(self):
        return self.view


class Copa2022(MDApp):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    grupos = {
        'Grupo A': ['Catar', 'Equador', 'Senegal', 'Holanda'],
        'Grupo B': ['Inglaterra', 'Irã', 'EUA', 'Euro Play-off'],
        'Grupo C': ['Argentina', 'Arábia Saudita', 'México', 'Polonia'],
        'Grupo D': ['França', 'IC Play-off 1', 'Dinamarca', 'Tunísia'],
        'Grupo E': ['Espanha', 'IC Play-off 2', 'Alemanha', 'Japão'],
        'Grupo F': ['Bélgica', 'Canadá', 'Marrocos', 'Croácia'],
        'Grupo G': ['Brasil', 'Sérvia', 'Suíça', 'Camarões'],
        'Grupo H': ['Portugal', 'Gana', 'Uruguai', 'Coreia do Sul'],
        '': ['Catar', 'Equador', 'Senegal', 'Holanda'],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('copa2022.kv')
        self.controller = RootScreenController()

    def build(self):
        return self.controller.get_screen()

    def on_start(self):
        tab_list = self.root.ids.screen_manager.get_screen(
            'results').ids.tabs.get_tab_list()
        for tab in tab_list:
            self.make_group(tab.tab, tab.text)
        self.root.dispatch("on_enter")

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Called when switching tabs.
            :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
            :param instance_tab: <__main__.Tab object>;
            :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
            :param tab_text: text or name icon of tab;
        """
        if tab_text != '':
            self.update_tab(instance_tab, tab_text)

    def make_group(self, instance_tab, tab_text):
        cont_team = {
            0: instance_tab.ids.time1,
            1: instance_tab.ids.time2,
            2: instance_tab.ids.time3,
            3: instance_tab.ids.time4
        }
        for pos in range(4):
            path = tab_text.replace(' ', '')
            flag = self.grupos[tab_text][pos].lower()
            cont_team[pos].text = self.grupos[tab_text][pos]
            cont_team[pos].flag = f"assets/images/{path}/{flag}.png"

    def update_tab(self, instance_tab, tab_text):
        cont_team = {
            'time1': instance_tab.ids.time1.ids.container1,
            'time2': instance_tab.ids.time2.ids.container1,
            'time3': instance_tab.ids.time3.ids.container1,
            'time4': instance_tab.ids.time4.ids.container1
        }
        res = open('results.json', 'r')
        data = json.load(res)
        if tab_text != '':
            for stats in data[tab_text].keys():
                cont_team[stats].ids.pts.text = data[tab_text][stats][0]
                cont_team[stats].ids.v.text = data[tab_text][stats][1]
                cont_team[stats].ids.e.text = data[tab_text][stats][2]
                cont_team[stats].ids.d.text = data[tab_text][stats][3]
                cont_team[stats].ids.gp.text = data[tab_text][stats][4]
                cont_team[stats].ids.gc.text = data[tab_text][stats][5]
                cont_team[stats].ids.sg.text = data[tab_text][stats][6]
        res.close()

    def show_team(self, *args):
        print(self.controller.screens)
        team = self.controller.screen_manager.get_screen('team')
        # team.name = args[0]
        try:
            team = self.root.ids.screen_manager.get_screen(args[0])
            self.root.ids.screen_manager.current = team.name
        except ScreenManagerException:
            print("deu exception")
            team = Catar(name=args[0])
            self.root.ids.screen_manager.add_widget(team)
            self.root.ids.screen_manager.current = team.name

    def create_team(self, team):
        pass


class RootScreenController:
    screens = {
        'results':  {
            "model": None,
            "controller": GenericController,
            "view": Tabela
        },
        'team': {
            "model": None,
            "controller": GenericController,
            "view": Catar
        }
    }

    def __init__(self) -> None:
        self.view = RootScreen(controller=self, name="root")
        self.screen_manager = self.view.ids.screen_manager

        for i, name_screen in enumerate(self.screens.keys()):
            model = self.screens[name_screen]["model"]
            controller = self.screens[name_screen]["controller"](
                model, self.screens[name_screen]["view"])
            view = controller.get_screen()
            view.screen_manager = self.screen_manager
            view.name = name_screen
            self.screen_manager.add_widget(view)

    def get_screen(self):
        return self.view

    def transition_to_screen(self, screen_name):
        self.screen_manager.current = screen_name


Copa2022().run()
