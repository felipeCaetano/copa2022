from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivymd.app import MDApp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior, \
    RectangularRippleBehavior
from kivymd.uix.label import MDLabel

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import FitImage kivymd.uix.fitimage 


<CardItem>
    size_hint_y: None
    height: "86dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    ripple_behavior: True
    on_release:
        app.set_card(self)

    FitImage:
        source: root.source
        radius: root.radius
        size_hint_x: None
        width: root.height

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        spacing: "4dp"
        padding: "10dp", 0, 0, 0
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.stadium
            font_style: "H6"
            bold: True
            adaptive_height: True

        MDLabel:
            text: root.city
            theme_text_color: "Hint"
            adaptive_height: True

MDScreen:

    MDSliverAppbar:
        background_color: get_color_from_hex("#7b133d")

        MDSliverAppbarHeader:
            MDRelativeLayout:
                FitImage:
                    id: back
                    source: "assets/images/logo.png"

        MDSliverAppbarContent:
            id: content
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            adaptive_height: True
'''


class CardItem(MDCard,
               RoundedRectangularElevationBehavior,
               RectangularRippleBehavior,
               ButtonBehavior):

   stadium = StringProperty()
   city = StringProperty()
   info = StringProperty()
   source = StringProperty()


class Example(MDApp):
    stadiums = {
        "albayt": "Al Bayt Stadium",
        "education": "Education City Stadium",
        "lusail": "Lusail Stadium",
        "974": "Stadium 974",
        "ahmad": "Ahmad Bin Ali Stadium",
        "janoub": "Al Janoub Stadium",
        "thumama": "Al Thumama Stadium",
        "khalifa": "Khalifa International Stadium",
    }
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        for stadium in self.stadiums:
            self.root.ids.content.add_widget(CardItem(
                stadium=self.stadiums[stadium],
                city=self.stadiums[stadium],
                source=f"assets/images/stadiums/{stadium}.png"
            ))

    def set_card(self, carditem):
        self.root.ids.back.source = carditem.source
        label = MDLabel(text="gostei", halign='center')
        modal = ModalView(
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': .5, 'center_y': .8},
            background_color=(.48, .07, .24, .3),
            overlay_color=(1, 0, 0, 0),
        )
        modal.add_widget(label)
        modal.open()


Example().run()