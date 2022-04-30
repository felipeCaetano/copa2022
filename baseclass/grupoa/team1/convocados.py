"""base class para as escalações dos times."""
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, \
    MDExpansionPanelThreeLine


class Content(MDBoxLayout):
    '''Custom content.'''


class Convocados(MDBoxLayout):
    def __int__(self):
        super(Convocados, self).__int__()

    def create_team(self):
        print("fui chamado")
        for i in range(10):
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