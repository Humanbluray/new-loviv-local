import flet as ft
from utils import MAIN_COLOR
from utils.lateral_menu import Menu


class Welcome(ft.View):
    def __init__(self, page):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, route="/welcome", bgcolor="#f2f2f2"
        )
        self.page = page
        self.menu = Menu(self, page)
        self.barre = ft.Container(
            content=ft.Column(controls=[self.menu]),
            border_radius=12, width=180,
        )
        self.contenu = ft.Container(
            border_radius=16, padding=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Image(src="assets/logo/logo NB.png", width=400, height=400, opacity=0.4)
                        ], alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
            )
        )
        # Dialog box
        self.box = ft.AlertDialog(
            title=ft.Text("", size=20, font_family="Poppins-Light"),
            content=ft.Text("", size=12, font_family="Poppins-Medium"),
            actions=[
                ft.TextButton(
                    content=ft.Row(
                        [ft.Text("Quitter", size=12, font_family="Poppins-Medium", color=MAIN_COLOR)],
                        alignment=ft.MainAxisAlignment.CENTER
                    ), width=120,
                    on_click=self.close_box
                )
            ]
        )
        self.fp_select_image = ft.FilePicker()
        self.fp_edit_image = ft.FilePicker()

        for widget in (self.box, self.fp_select_image, self.fp_edit_image):
            self.page.overlay.append(widget)

        self.controls = [
            ft.Container(
                expand=True, margin=5,
                content=ft.Row(
                    controls=[self.barre,self.contenu],
                    spacing=10, vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        ]

    def close_box(self, e):
        self.box.open = False
        self.box.update()