import datetime
import json

from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import (
    MDExpansionPanel,
    MDExpansionPanelThreeLine,
)
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import (
    IRightBodyTouch,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase

from catar import Content

Builder.load_file('tabela.kv')
Builder.load_file('catar.kv')
Builder.load_file('matchs.kv')
Builder.load_file('playoffs16.kv')
Builder.load_file('baseclass/grupoa/team1/convocados.kv')


class BaseScreenView(ThemableBehavior, MDScreen):
    controller = ObjectProperty()
    model = ObjectProperty()
    screen_manager = ObjectProperty()

    def goto_screen(self, screen_name):
        if 'nav_drawer' in self.ids and self.ids.nav_drawer is not None:
            if self.ids.nav_drawer.state == 'open':
                self.ids.nav_drawer.set_state('close')
            Clock.schedule_once(
                lambda x: self.transition_to_screen(screen_name), 0.2
            )

    def transition_to_screen(self, screen):
        self.controller.transition_to_screen(screen)


class RootScreen(BaseScreenView):
    pass


class Tabela(BaseScreenView):
    pass


class YourContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class Matchs(BaseScreenView):
    pass


class PlayOffs(BaseScreenView):
    "classe para a tela dos playoffs."
    pass


class Catar(BaseScreenView):
    team_name = StringProperty()
    treinador = StringProperty()
    flag = StringProperty()


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class GameTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a gametab."""


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
        'Grupo C': ['Argentina', 'Arábia Saudita', 'México', 'Polônia'],
        'Grupo D': ['França', 'IC Play-off 1', 'Dinamarca', 'Tunísia'],
        'Grupo E': ['Espanha', 'IC Play-off 2', 'Alemanha', 'Japão'],
        'Grupo F': ['Bélgica', 'Canadá', 'Marrocos', 'Croácia'],
        'Grupo G': ['Brasil', 'Sérvia', 'Suíça', 'Camarões'],
        'Grupo H': ['Portugal', 'Gana', 'Uruguai', 'Coréia do Sul'],
        '': ['Catar', 'Equador', 'Senegal', 'Holanda'],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('copa2022.kv')
        self.controller = RootScreenController()

        with open('teams.json', 'r', encoding='utf-8') as selecoes:
            data = json.load(selecoes)
            self.teams = data

    def build(self):
        return self.controller.get_screen()

    def on_start(self):
        tab_list = self.root.ids.screen_manager.get_screen(
            'results'
        ).ids.tabs.get_tab_list()
        for tab in tab_list:
            self.make_group(tab.tab, tab.text)
        self.root.dispatch('on_enter')

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        """Called when switching tabs.
        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """
        if tab_text in self.grupos and tab_text != '':
            self.update_tab(instance_tab, tab_text)
        else:
            self.create_match(instance_tab, tab_text)

    def create_match(self, instace_tab, tab_text):
        data = self.load_matches(tab_text)
        for match in data.keys():
            gamecard = Factory.GameCard()
            instace_tab.ids.cards.add_widget(gamecard)
            self.set_game_card(data, gamecard, match)

    def set_game_card(self, data, gamecard, match):
        try:
            gamecard.grupo_text = data[match]["grupo_text"] + "h"
            gamecard.time1 = data[match]['time1']
            gamecard.time2 = data[match]['time2']
            gamecard.flag1 = self.teams[gamecard.time1]['flag']
            gamecard.flag2 = self.teams[gamecard.time2]['flag']
            gamecard.stadium = data[match]["stadium"]
            # hora = datetime.datetime.now()
            # print(hora.)
        except KeyError:
            print(
                f"Pelo menos um destes times não estao na lista"
                f" {gamecard.time1, gamecard.time2}")
            gamecard.flag1 = "assets/images/unknown.png"
            gamecard.flag2 = "assets/images/unknown.png"
            gamecard.stadium = data[match]["stadium"]

    def load_matches(self, tab_text):
        res = None
        data = {}
        if tab_text == '1ª Rodada':
            data, res = self.get_data('rodada1.json', res, tab_text)
        elif tab_text == '2ª Rodada':
            data, res = self.get_data('rodada1.json', res, tab_text)
        elif tab_text == '3ª Rodada':
            data, res = self.get_data('rodada1.json', res, tab_text)
        elif tab_text == '8ª de Final':
            res = open('oitavas.json', 'r', encoding='utf-8')
            data = json.load(res)
            data = data[tab_text]
        elif tab_text == '4ª de Final':
            res = open('oitavas.json', 'r', encoding='utf-8')
            data = json.load(res)
            data = data[tab_text]
        elif tab_text == 'Semi-Finais':
            res = open('oitavas.json', 'r', encoding='utf-8')
            data = json.load(res)
            data = data[tab_text]
        try:
            res.close()
        except AttributeError:
            print(f"{tab_text=}, não está definido.")
        except UnboundLocalError:
            pass
        return data

    def get_data(self, json_file, res, tab_text):
        res = open(json_file, 'r', encoding='utf-8')
        data = json.load(res)
        data = data[tab_text]
        return data, res

    def make_group(self, instance_tab, tab_text):
        cont_team = {
            0: instance_tab.ids.time1,
            1: instance_tab.ids.time2,
            2: instance_tab.ids.time3,
            3: instance_tab.ids.time4,
        }
        for pos in range(4):
            path = tab_text.replace(' ', '')
            flag = self.grupos[tab_text][pos].lower()
            team = self.grupos[tab_text][pos].lower()
            cont_team[pos].text = self.grupos[tab_text][pos]
            cont_team[pos].flag = f'assets/images/{path}/{team}/{flag}.png'

    def create_team(self, team):
        """
        :param team:
        :return:
        """
        grupo = self.teams[team.name]['grupo']
        selecao = team.name.lower()
        for i in range(24):
            team.ids.box.add_widget(
                MDExpansionPanel(
                    icon=f'assets/images/Grupo{grupo}/{selecao}/players/{i}.png',
                    content=Content(),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=self.teams[team.name][str(i)][1],
                        secondary_text=self.teams[team.name][str(i)][2],
                        tertiary_text=self.teams[team.name][str(i)][4],
                    ),
                )
            )

    def update_tab(self, instance_tab, tab_text):
        cont_team = {
            'time1': instance_tab.ids.time1.ids.container1,
            'time2': instance_tab.ids.time2.ids.container1,
            'time3': instance_tab.ids.time3.ids.container1,
            'time4': instance_tab.ids.time4.ids.container1,
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

    def show_matchs(self, *args):
        tab = args[0].ids.screen_manager.get_screen(
            'matchs'
        ).ids.tabs.get_tab_list()[0]
        self.create_match(tab.tab, tab.text)

    def show_team(self, *args):
        team = Catar(name=args[0])
        team.team_name = f"Seleção {self.teams[args[0]]['Nome']}"
        team.treinador = f"{self.teams[args[0]]['Treinador']}"
        team.flag = self.teams[args[0]]['flag']
        try:
            team = self.root.ids.screen_manager.get_screen(args[0])
            self.root.ids.screen_manager.current = team.name
        except ScreenManagerException:
            self.create_team(team)
            self.root.ids.screen_manager.add_widget(team)
            self.root.ids.screen_manager.current = team.name


class RootScreenController:
    screens = {
        'results': {
            'model': None,
            'controller': GenericController,
            'view': Tabela,
        },
        'team': {
            'model': None,
            'controller': GenericController,
            'view': Catar,
        },
        'matchs': {
            'model': None,
            'controller': GenericController,
            'view': Matchs,
        },
        'playoffs16': {
            'model': None,
            'controller': GenericController,
            'view': PlayOffs
        }
    }

    def __init__(self) -> None:
        self.view = RootScreen(controller=self, name='root')
        self.screen_manager = self.view.ids.screen_manager

        for i, name_screen in enumerate(self.screens.keys()):
            model = self.screens[name_screen]['model']
            controller = self.screens[name_screen]['controller'](
                model, self.screens[name_screen]['view']
            )
            view = controller.get_screen()
            view.screen_manager = self.screen_manager
            view.name = name_screen
            self.screen_manager.add_widget(view)

    def get_screen(self):
        return self.view

    def transition_to_screen(self, screen_name):
        self.screen_manager.current = screen_name


Copa2022().run()
