"""Modela a Classe UI da Seleção do Catar"""
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, \
    MDExpansionPanelThreeLine
from kivymd.uix.screen import MDScreen

from baseclass.grupoa.team1.convocados import Convocados


class Content(MDBoxLayout):
    '''Custom content.'''


class Catar(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.name = kwargs['name']


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