import json

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManagerException
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.tab import MDTabsBase

from catar import Catar
from tabela import Tabela


Builder.load_file('tabela.kv')
Builder.load_file('catar.kv')
Builder.load_file('baseclass/grupoa/team1/convocados.kv')


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class TeamContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

# class ContentNavigationDrawer(MDBoxLayout):
#     screen_manager = ObjectProperty()
#     nav_drawer = ObjectProperty()


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

    def build(self):
        return Builder.load_file('copa2022.kv')

    def on_start(self):
        for i in range(65, 73):
            tab_text = f"Grupo {chr(i)}"
            instance_tab = Tab(title=tab_text)
            self.root.ids.screen_manager.get_screen('results').ids.tabs.add_widget(instance_tab)
            self.make_group(instance_tab, tab_text)
            self.update_tab(instance_tab, tab_text)

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
        path = tab_text.replace(' ', '')
        flag1 = self.grupos[tab_text][0].lower()
        flag2 = self.grupos[tab_text][1].lower()
        flag3 = self.grupos[tab_text][2].lower()
        flag4 = self.grupos[tab_text][3].lower()
        instance_tab.ids.time1.text = self.grupos[tab_text][0]
        instance_tab.ids.flag1.source = f"assets/images/{path}/{flag1}.png"
        instance_tab.ids.time2.text = self.grupos[tab_text][1]
        instance_tab.ids.flag2.source = f"assets/images/{path}/{flag2}.png"
        instance_tab.ids.time3.text = self.grupos[tab_text][2]
        instance_tab.ids.flag3.source = f"assets/images/{path}/{flag3}.png"
        instance_tab.ids.time4.text = self.grupos[tab_text][3]
        instance_tab.ids.flag4.source = f"assets/images/{path}/{flag4}.png"

    def update_tab(self, instance_tab, tab_text):
        cont_team = {
            'time1': instance_tab.ids.container1,
            'time2': instance_tab.ids.container2,
            'time3': instance_tab.ids.container3,
            'time4': instance_tab.ids.container4
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
        print(*args)
        print(self.root.ids.screen_manager.screens)

        try:
            team = self.root.ids.screen_manager.get_screen(args[0])
            self.root.ids.screen_manager.current = team.name
        except ScreenManagerException:
            team = Catar(name=args[0])
            self.root.ids.screen_manager.add_widget(team)
            self.root.ids.screen_manager.current = team.name

    def create_team(self, team):
        pass


Copa2022().run()
