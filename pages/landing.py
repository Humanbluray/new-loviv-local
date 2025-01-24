from utils import AnyButton, MAIN_COLOR, SECOND_COLOR
import flet as ft
from utils.styles import login_style


class Landing(ft.View):
    def __init__(self, page):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            route="/", bgcolor="white"
        )
        self.page = page

        self.login = ft.TextField(
            **login_style, prefix_icon=ft.icons.PERSON_OUTLINE_OUTLINED, label="Login"
        )
        self.passw = ft.TextField(
            **login_style, prefix_icon=ft.icons.KEY_OUTLINED, label="Pass",
            password=True, can_reveal_password=True
        )
        self.bt_connect = AnyButton(MAIN_COLOR, "check", "Connecter", "white", None,self.connexion)
        self.bt_first_connect = AnyButton(MAIN_COLOR, ft.icons.SUBSCRIPTIONS_SHARP, "Inscrire", "white", None, self.connexion)

        # Dialog box
        self.box = ft.AlertDialog(
            surface_tint_color="white",
            title=ft.Text("", size=20, font_family="Poppins Light"),
            content=ft.Text("", size=12, font_family="Poppins Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins Medium", color=MAIN_COLOR)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ), width=120,
                    on_click=self.close_box
                )
            ]
        )
        self.card = ft.Card(
            elevation=10, surface_tint_color="white",
            scale=ft.transform.Scale(0),
            animate_scale=ft.animation.Animation(600, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
            content=ft.Container(
                border_radius=16, padding=20, width=250, bgcolor="white",
                content=ft.Column(
                    controls=[
                        ft.Image(src="assets/logo/Ovive LOGO.png", width=130, height=130),
                        ft.Divider(height=1, color="transparent"),
                        # ft.Column(
                        #     controls=[
                        #         ft.Text("ENtrez vos informations".upper(), size=11, font_family="Poppins Medium"),
                        #         ft.Divider(thickness=1, height=1),
                        #     ], spacing=0,  horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        # ),
                        ft.Divider(height=1, color="transparent"),
                        ft.Column([self.login, self.passw, self.bt_connect, self.bt_first_connect], spacing=10),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        self.splash = ft.Container(
            width=400, height=400, on_click=self.load_datas,
            content=ft.Image(src="assets/logo/Ovive LOGO.png", fit=ft.ImageFit.CONTAIN)
        )
        self.controls = [
            ft.Stack(
                controls=[
                    self.splash, self.card,
                ], alignment=ft.alignment.center
            )
        ]

    def load_datas(self, e):
        self.splash.scale = 0
        self.card.scale = 1

        for widget in (self.splash, self.card):
            widget.update()

    def close_box(self, e):
        self.box.open = False
        self.box.update()

    def connexion(self, e):
        self.page.go("/welcome")