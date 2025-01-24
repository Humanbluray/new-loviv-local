import flet as ft
import time
import asyncio
import base64

MAIN_COLOR = "#C23028"
SECOND_COLOR = ft.colors.DEEP_ORANGE
THIRD_COLOR = "#C5C5C6"
FOURTH_COLOR = "#EBB016"
FIFTH_COLOR = "white"


# Tous les boutons du logiciel
class AnyButton(ft.ElevatedButton):
    def __init__(self, theme_color:str, my_icon: str, title: str, text_color: str, my_width, click):
        super().__init__(
            bgcolor=theme_color,
            height=40, width=my_width, elevation=1,
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=22)
            ),
            content=ft.Row(
                controls=[
                    # ft.Icon(
                    #     my_icon, color="white", size=16,
                    #     scale=ft.transform.Scale(1),
                    #     animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                    # ),
                    ft.Text(
                        title, size=12, font_family="Poppins-Medium", color=text_color,
                        scale=ft.transform.Scale(1),
                        animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=click, on_hover=self.hover_bt
        )
        self.theme_color = theme_color

    def hover_bt(self, e):
        if e.data == "true":
            for widget in self.content.controls[:]:
                widget.scale = 1.3
                widget.update()
            self.bgcolor=SECOND_COLOR
            self.update()
        else:
            for widget in self.content.controls[:]:
                widget.scale = 1
                widget.update()

            self.bgcolor = self.theme_color
            self.update()



# tous les containerBoutons du logiciel
class CtButton(ft.Container):
    def __init__(self, my_icon, my_tool,my_datas, on_click_function,):
        super().__init__(
            border_radius=6, padding=5,
            on_click=on_click_function,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            on_hover=self.hover_ct,
            data=my_datas,
            tooltip=my_tool,
            content=ft.Icon(
                my_icon,
                color=ft.colors.BLACK45,
            )
        )
        self.my_icon = my_icon

    def hover_ct(self, e):
        if e.data == "true":
            self.scale = 1.2
            self.update()
        else:
            self.scale = 1
            self.update()

