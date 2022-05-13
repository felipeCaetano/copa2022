from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
# from kivy.core.window.window import Window

# Your layouts.
Builder.load_string(
    '''
#:import Window kivy.core.window.Window
#:import IconLeftWidget kivymd.uix.list.IconLeftWidget


<ItemBackdropFrontLayer@TwoLineAvatarListItem>
    icon: "android"

    IconLeftWidget:
        icon: root.icon


<MyBackdropFrontLayer@ItemBackdropFrontLayer>
    text: ""
    identifier: ""
    backdrop: None
    text: root.text
    secondary_text: " by 50 %"
    icon: "stadium"
    on_press: root.backdrop.parent.when_open(self.identifier)#root.backdrop.open(-Window.height / 2)
    pos_hint: {"top": 1}
    _no_ripple_effect: True


<MyBackdropBackLayer@Image>
    size_hint: .8, .8
    source: ""
    pos_hint: {"center_x": .5, "center_y": .6}
'''
)

# Usage example of MDBackdrop.
Builder.load_string(
    '''
<ExampleBackdrop>
    MDCard:
        id: card
        MDLabel:
            text: 'testando'

    MDBackdrop:
        id: backdrop
        left_action_items: [['menu', lambda x: self.open()]]
        title: "Example Backdrop"
        radius_left: "25dp"
        radius_right: "0dp"
        header_text: "Estádio:"
        
        MDBackdropBackLayer:
            MyBackdropBackLayer:
                id: backlayer

        MDBackdropFrontLayer:
            orientation: 'vertical'
            MDLabel:
                id: info 
                text:""
            MyBackdropFrontLayer:
                identifier: 'albayt'
                backdrop: backdrop
                text: "Estádio al Bayt"
            MyBackdropFrontLayer:
                identifier: 'lusail'
                backdrop: card
                text: "Estádio Lusail"
'''
)


class ExampleBackdrop(MDScreen):
    identifiers ={
        'lusail': """Com capacidade para 80 mil pessoas, vai receber a final do campeonato. O design é inspirado pelo jogo de luz e sombra visto nas lanternas Fanar.\nA forma estrutural e a fachada repetem os motivos intricados de peças de arte e mobiliário encontradas pelos mundos árabe e islâmico. Com o fim do evento, o local será transformado em um hub comunitário polivalente.
                
        O estádio foi inaugurado no final de 2021.""",
        'albayt': ""
    }

    def when_open(self, identifier):
        print(identifier)
        self.ids.backlayer.source = f"assets/images/stadiums/{identifier}.png"
        self.ids.info.text = self.identifiers[identifier]
        self.ids.backdrop.open(-Window.height / 2)

    def on_header(self, *args):
        print("on_header")
        print(args)


class TestBackdrop(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return ExampleBackdrop()


TestBackdrop().run()