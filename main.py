import urllib.request
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# Fondo AMOLED (#121212)
Window.clearcolor = (0.07, 0.07, 0.07, 1)

class TarjetaDND(BoxLayout):
    def __init__(self, titulo, color_titulo, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=8, size_hint_y=None, height=120, **kwargs)
        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[12])
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.lbl_titulo = Label(text=titulo, font_size='18sp', bold=True, color=color_titulo, size_hint_y=None, height=30)
        self.lbl_valores = Label(text="[Toca consultar para ver runas]", font_size='16sp', color=(1, 1, 1, 1), size_hint_y=None, height=40)
        
        self.add_widget(self.lbl_titulo)
        self.add_widget(self.lbl_valores)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class DragonsHoardApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=15, spacing=12)

        lbl_header = Label(text="🐲 DRAGON'S HOARD 🐲", font_size='22sp', bold=True, color=(1, 0.76, 0.03, 1), size_hint_y=None, height=45)
        self.lbl_bote = Label(text="Bote: 54 Millones de Orros", font_size='15sp', color=(0.8, 0.8, 0.8, 1), size_hint_y=None, height=25)
        root.add_widget(lbl_header)
        root.add_widget(self.lbl_bote)

        scroll = ScrollView(size_hint=(1, 1))
        contenedor_apuestas = BoxLayout(orientation='vertical', spacing=12, size_hint_y=None)
        contenedor_apuestas.bind(minimum_height=contenedor_apuestas.setter('height'))

        self.card_hibrida = TarjetaDND("🐉 Escama Híbrida (Equilibrada)", (1, 0.76, 0.03, 1))
        self.card_fuego = TarjetaDND("🔥 Aliento de Fuego (Calientes)", (1, 0.34, 0.13, 1))
        self.card_hielo = TarjetaDND("❄️ Hielo del Tiempo (Fríos)", (0, 0.9, 1, 1))

        contenedor_apuestas.add_widget(self.card_hibrida)
        contenedor_apuestas.add_widget(self.card_fuego)
        contenedor_apuestas.add_widget(self.card_hielo)
        scroll.add_widget(contenedor_apuestas)
        root.add_widget(scroll)

        btn_consultar = Button(
            text="⚔️ CONSULTAR ORÁCULO ⚔️", 
            font_size='16sp', 
            bold=True, 
            background_normal='', 
            background_color=(1, 0.76, 0.03, 1), 
            color=(0, 0, 0, 1), 
            size_hint_y=None, 
            height=55
        )
        btn_consultar.bind(on_press=self.consultar_oraculo)
        root.add_widget(btn_consultar)

        return root

    def consultar_oraculo(self, instance):
        try:
            url = "https://jeriko.pythonanywhere.com/api/predicciones"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                self.lbl_bote.text = f"Bote: {data.get('bote_estimado', 'Consultado')}"
                
                apuestas = data.get('apuestas', [])
                if len(apuestas) >= 3:
                    n1 = " - ".join(map(str, apuestas[0]['numeros']))
                    e1 = f" ⭐ {apuestas[0]['estrellas'][0]} - {apuestas[0]['estrellas'][1]}"
                    self.card_hibrida.lbl_valores.text = f"{n1} |{e1}"

                    n2 = " - ".join(map(str, apuestas[1]['numeros']))
                    e2 = f" ⭐ {apuestas[1]['estrellas'][0]} - {apuestas[1]['estrellas'][1]}"
                    self.card_fuego.lbl_valores.text = f"{n2} |{e2}"

                    n3 = " - ".join(map(str, apuestas[2]['numeros']))
                    e3 = f" ⭐ {apuestas[2]['estrellas'][0]} - {apuestas[2]['estrellas'][1]}"
                    self.card_hielo.lbl_valores.text = f"{n3} |{e3}"
        except Exception:
            self.lbl_bote.text = "Error al conectar con el servidor"

if __name__ == '__main__':
    DragonsHoardApp().run()
