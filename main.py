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
Builder.load_file('stadiums.kv')


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


class Stadiums(BaseScreenView):
    pass


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
    # grupos = {
    #     'Grupo A': ['Catar', 'Equador', 'Senegal', 'Holanda'],
    #     'Grupo B': ['Inglaterra', 'Irã', 'EUA', 'País de Gales'],
    #     'Grupo C': ['Argentina', 'Arábia Saudita', 'México', 'Polônia'],
    #     'Grupo D': ['França', 'IC Play-off 1', 'Dinamarca', 'Tunísia'],
    #     'Grupo E': ['Espanha', 'IC Play-off 2', 'Alemanha', 'Japão'],
    #     'Grupo F': ['Bélgica', 'Canadá', 'Marrocos', 'Croácia'],
    #     'Grupo G': ['Brasil', 'Sérvia', 'Suíça', 'Camarões'],
    #     'Grupo H': ['Portugal', 'Gana', 'Uruguai', 'Coréia do Sul'],
    #     '': ['Catar', 'Equador', 'Senegal', 'Holanda'],
    # }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('copa2022.kv')
        self.controller = RootScreenController()

        with open('teams.json', 'r', encoding='utf-8') as grupos:
            data = json.load(grupos)
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
        chamada cada vez que se toca na aba do grupo,
        ou na aba das partidas (rodadas).
        """
        if tab_text in self.teams and tab_text != '':
            self.update_tab(instance_tab, tab_text)
        else:
            self.create_match(instance_tab, tab_text)

    def create_match(self, instace_tab, tab_text):
        """
        Cria um confronto vazio e coloca na tela de partidas
        :param instace_tab: aba onde será colocado o confronto
        :param tab_text: nome da aba onde será colocado o confronto (rodada)
        :return: None
        """
        data = self.load_matches(tab_text)
        for match in data.keys():
            gamecard = Factory.GameCard()
            instace_tab.ids.cards.add_widget(gamecard)
            self.set_game_card(data, gamecard, match)

    def set_game_card(self, data, gamecard, match):
        """
        Coloca os atributos em cada gamecard que será exibido.
        A partida atual fica destacada.
        :param data: dicinário de partidas
        :param gamecard: objeto que contem os dados da partida
        :param match: partida a ser colocada no gamecard
        :return:
        """
        try:
            gamecard.grupo_text = data[match]["grupo_text"] + "h"
            gamecard.time1 = data[match]['time1']
            gamecard.time2 = data[match]['time2']
            gamecard.flag1 = self.teams[gamecard.time1]['flag']
            print(data[match]['time2'])
            gamecard.flag2 = self.teams[gamecard.time2]['flag']
            gamecard.stadium = data[match]["stadium"]
            # hora = datetime.datetime.now()
            # print(hora.)
        except KeyError:
            if gamecard.time1 == 'País de Gales' or gamecard.time1 == 'austrália' or gamecard.time1 == 'IC Play-off 2':
                gamecard.flag1 = "assets/images/unknown.png"
                gamecard.flag2 = self.teams[gamecard.time2]['flag']
            elif gamecard.time2 == 'País de Gales' or gamecard.time2 == 'austrália' or gamecard.time2 == 'IC Play-off 2':
                gamecard.flag2 = "assets/images/unknown.png"
                gamecard.flag1 = self.teams[gamecard.time1]['flag']
            gamecard.stadium = data[match]["stadium"]

    def load_matches(self, tab_text):
        """
        Carrega os dados do .json correspondente as partidas da fases do torneio.
        :param tab_text: Nome da rodada do torneio
        :return: dicionário de partidas correspondente, data.
        """
        # res = None
        data = {}
        if tab_text == '1ª Rodada':
            data = self.get_data('rodada1.json', tab_text)
        elif tab_text == '2ª Rodada':
            data = self.get_data('rodada1.json', tab_text)
        elif tab_text == '3ª Rodada':
            data = self.get_data('rodada1.json', tab_text)
        elif tab_text == '8ª de Final':
            data = self.get_data('oitavas.json', tab_text)
        elif tab_text == '4ª de Final':
            data = self.get_data('oitavas.json', tab_text)
        elif tab_text == 'Semi-Finais':
            data = self.get_data('oitavas.json', tab_text)
        # try:
        #     res.close()
        # except AttributeError:
        #     print(f"{tab_text=}, não está definido.")
        # except UnboundLocalError:
        #     pass
        return data

    def get_data(self, json_file, key):
        """
        Carrega um .json específico para ser usado no app.
        :param json_file: arquivo a ser lido
        :param res: result do json
        :param key: dicinário a ser selecionado
        :return:
        """
        # res = open(json_file, 'r', encoding='utf-8')
        # data = json.load(res)
        # data = data[key]
        with open(json_file, 'r', encoding='utf-8') as res:
            data = json.load(res)
            data = data[key]
        return data

    def make_group(self, instance_tab, tab_text):
        """
        Cria os grupos da tabela colocando cada pais na sua posição dentro do
        grupo.
        :param instance_tab: Tab que conterá os times do grupo.
        :param tab_text: Nome do grupo
        :return: None
        """
        cont_team = {
            0: instance_tab.ids.time1,
            1: instance_tab.ids.time2,
            2: instance_tab.ids.time3,
            3: instance_tab.ids.time4,
        }
        for pos in range(4):
            path = tab_text.replace(' ', '')
            selection = list(self.teams[tab_text].keys())[pos]
            team = selection.lower()
            cont_team[pos].text = selection
            cont_team[pos].flag = f'assets/images/{path}/{team}/{team}.png'

    def create_team(self, team, group):
        """
        Cria time para ser exibido na respectiva tela.
        :param team:
        :return:
        """
        grupo = group.replace(" ", "")
        selecao = team.name.lower()
        for group, teams in self.teams.items():
            if team.name in teams:
                list_team = list(teams[team.name].keys())[4:]
                for i in list_team:
                    team.ids.box.add_widget(
                        MDExpansionPanel(
                            icon=f'assets/images/{grupo}/{selecao}/players/{i}.png',
                            content=Content(),
                            panel_cls=MDExpansionPanelThreeLine(
                                text=teams[team.name][i][1],
                                secondary_text=teams[team.name][i][2],
                                tertiary_text=teams[team.name][i][4],
                            ),
                        )
                    )
                break

    def update_tab(self, instance_tab, tab_text):
        """
        Atualiza os resultados dos grupos de acordo com o resultado das partidas
        :param instance_tab:
        :param tab_text:
        :return: None
        """
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
        print(tab.tab, tab.text)
        self.create_match(tab.tab, tab.text)

    def show_team(self, *args):
        team = Catar(name=args[0])
        for group, teams in self.teams.items():
            if args[0] in teams:
                team.team_name = f"Seleção {teams[args[0]]['Nome']}"
                team.treinador = f"{teams[args[0]]['Treinador']}"
                team.flag = teams[args[0]]['flag']
                break
        try:
            team = self.root.ids.screen_manager.get_screen(args[0])
            self.root.ids.screen_manager.current = team.name
        except ScreenManagerException:
            self.create_team(team, group)
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
        },
        'stadiums': {
            'model': None,
            'controller': GenericController,
            'view': Stadiums
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
