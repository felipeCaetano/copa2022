import datetime
import json

from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import (
    MDExpansionPanel,
    MDExpansionPanelThreeLine,
)
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import (
    IRightBodyTouch,
    OneLineAvatarIconListItem,
    ILeftBodyTouch,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase
from kivymd.utils import asynckivy

from catar import Content

Builder.load_file('tabela.kv')
Builder.load_file('catar.kv')
Builder.load_file('matchs.kv')
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


class Catar(BaseScreenView):
    team_name = StringProperty()
    treinador = StringProperty()
    flag = StringProperty()


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
        if tab_text != '':
            self.update_tab(instance_tab, tab_text)

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
        PAREI AQUI TÀ QUASE CERTO
        :param team:
        :return:
        """
        players = {
            'Catar': {
                'grupo': 'A',
                0: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                1: ['1', 'Saad Al-Sheeb', 'Goleiro', '32', 'Al-Sadd SC'],
                2: ['21', 'Yousef Hassan', 'Goleiro', '25', 'Al-Gharafa SC'],
                3: ['2', 'Pedro Miguel', 'Zagueiro', '31', 'Al-Sadd SC'],
                4: ['5', 'Tarek Salman', 'Zagueiro', '31', 'Al-Sadd SC'],
                5: ['15', 'Bassam Al-Rawi', 'Zagueiro', '24', 'Al-Duhail SC'],
                6: ['16', 'Boualem Khoukhi', 'Zagueiro', '31', 'Al-Sadd SC'],
                7: [
                    '3',
                    'Abdelkarim Hassan',
                    'Lateral Esq.',
                    '28',
                    'Al-Sadd SC',
                ],
                8: [
                    '24',
                    'Homam Ahmed',
                    'Lateral Esq.',
                    '22',
                    'Al-Gharafa SC',
                ],
                9: ['13', 'Musab Khoder', 'Lateral Dir.', '29', 'Al-Sadd SC'],
                10: ['12', 'Karim Boudiaf', 'Volante', '31', 'Al-Duhail SC'],
                11: ['23', 'Assim Madibo', 'Volante', '25', 'Al-Duhail SC'],
                12: ['-', 'Salem Al-Hajri', 'Volante', '26', 'Al-Sadd SC'],
                13: [
                    '-',
                    'Jassem Gaber Abdulsallam',
                    'Volante',
                    '20',
                    'Al-Arabi SC',
                ],
                14: [
                    '-',
                    'Abdulaziz Hatem',
                    'Meia Central',
                    '31',
                    'Al-Rayyan SC',
                ],
                15: ['-', 'Ahmed Fathi', 'Meia Central', '28', 'Al-Arabi SC'],
                16: ['-', 'Ahmad Doozandeh', 'Meia Central', '26', 'Qatar SC'],
                17: [
                    '-',
                    'Abdullah Marafee',
                    'Meia Central',
                    '30',
                    'Al-Arabi SC',
                ],
                18: ['4', 'Mohammed Waad', 'Meia Central', '22', 'Al-Sadd SC'],
                19: [
                    '20',
                    'Abdullah Al-Ahrak',
                    'Meia Ofensivo',
                    '24',
                    'Al-Sadd SC',
                ],
                20: ['8', "Ali Asad", 'Meia Ofensivo', '29', 'Al-Sadd SC'],
                21: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                22: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                23: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
            },
            'Equador': {
                'grupo': 'A',
                0: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                1: ['1', 'Saad Al-Sheeb', 'Goleiro', '32', 'Al-Sadd SC'],
                2: ['21', 'Yousef Hassan', 'Goleiro', '25', 'Al-Gharafa SC'],
                3: ['2', 'Pedro Miguel', 'Zagueiro', '31', 'Al-Sadd SC'],
                4: ['5', 'Tarek Salman', 'Zagueiro', '31', 'Al-Sadd SC'],
                5: ['15', 'Bassam Al-Rawi', 'Zagueiro', '24', 'Al-Duhail SC'],
                6: ['16', 'Boualem Khoukhi', 'Zagueiro', '31', 'Al-Sadd SC'],
                7: [
                    '3',
                    'Abdelkarim Hassan',
                    'Lateral Esq.',
                    '28',
                    'Al-Sadd SC',
                ],
                8: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                9: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                10: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                11: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                12: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                13: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                14: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                15: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                16: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                17: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                18: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                19: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                20: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                21: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                22: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
                23: ['22', 'Meshaal Barsham', 'Goleiro', '24', 'Al-Sadd SC'],
            },
        }

        grupo = players[team.name]['grupo']
        selec = team.name.lower()
        for i in range(24):
            team.ids.box.add_widget(
                MDExpansionPanel(
                    icon=f'assets/images/Grupo{grupo}/{selec}/players/{i}.png',
                    content=Content(),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=players[team.name][i][1],
                        secondary_text=players[team.name][i][2],
                        tertiary_text=players[team.name][i][4],
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
        print(
            args[0].ids.screen_manager.get_screen('matchs').ids)
        print( args[0].ids.screen_manager.get_screen('matchs').ids.time1.text)

    def show_team(self, *args):
        teams = {
            'Catar': {
                'Nome': 'do Catar',
                'Treinador': 'Treinador do Catar',
                'flag': 'assets/images/GrupoA/catar/catar.png',
            },
            'Equador': {
                'Nome': 'do Equador',
                'Treinador': 'Treinador do Equador',
                'flag': 'assets/images/GrupoA/equador/equador.png',
            },
            'Holanda': {
                'Nome': 'da Holanda',
                'Treinador': 'Treinador do Holanda',
                'flag': 'assets/images/GrupoA/holanda/holanda.png',
            },
            'Senegal': {
                'Nome': 'do Senegal',
                'Treinador': 'Treinador do Senegal',
                'flag': 'assets/images/GrupoA/senegal/senegal.png',
            },
            'EUA': {
                'Nome': 'dos Estados Unidos',
                'Treinador': 'Treinador do EUA',
                'flag': 'assets/images/GrupoB/eua/eua.png',
            },
            'Euro Play-off': {
                'Nome': 'do Euro Play-off',
                'Treinador': 'Treinador do Euro Play-off',
                'flag': 'assets/images/GrupoB/euro play-off/euro play-off.png',
            },
            'Inglaterra': {
                'Nome': 'da Inglaterra',
                'Treinador': 'Treinador do Inglaterra',
                'flag': 'assets/images/GrupoB/inglaterra/inglaterra.png',
            },
            'Irã': {
                'Nome': 'do Irã',
                'Treinador': 'Treinador do Irã',
                'flag': 'assets/images/GrupoB/irã/irã.png',
            },
            'Argentina': {
                'Nome': 'da Argentina',
                'Treinador': 'Treinador daArgentina',
                'flag': 'assets/images/GrupoC/argentina/argentina.png',
            },
            'México': {
                'Nome': 'do México',
                'Treinador': 'Treinador do México',
                'flag': 'assets/images/GrupoC/méxico/méxico.png',
            },
            'Arábia Saudita': {
                'Nome': 'da Arábia Saudita',
                'Treinador': 'Treinador da Arábia Saudita',
                'flag': 'assets/images/GrupoC/arábia saudita/arábia saudita.png',
            },
            'Polonia': {
                'Nome': 'da Polonia',
                'Treinador': 'Treinador da Polonia',
                'flag': 'assets/images/GrupoC/polonia/polonia.png',
            },
        }
        team = Catar(name=args[0])
        team.team_name = f"Seleção {teams[args[0]]['Nome']}"
        team.treinador = f"{teams[args[0]]['Treinador']}"
        team.flag = teams[args[0]]['flag']
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
