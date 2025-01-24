from utils import MAIN_COLOR, SECOND_COLOR
import flet as ft

normal_text_style: dict = dict(
    font_family="Poppins-Medium", size=12
)
title_text_style: dict = dict(
    font_family="Poppins-Bold", size=24
)
datatable_style: dict = dict(
    data_text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    heading_text_style=ft.TextStyle(size=11, font_family="Poppins-Medium", color="grey"),
)
search_field_style: dict = dict(
    dense=True,
    border_color="#f2f2f2", bgcolor="#f2f2f2",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
field_style: dict = dict(
    dense=True,
    focused_border_color=MAIN_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
numbers_field_style: dict = dict(
    dense=True,
    focused_border_color=MAIN_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=11, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=2,
    input_filter=ft.NumbersOnlyInputFilter(), text_align=ft.TextAlign.RIGHT.RIGHT
)
login_style: dict = dict(
    dense=True,
    focused_border_color=MAIN_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=2,
)
inactive_field_style: dict = dict(
    dense=True, disabled=True,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
readonly_field_style: dict = dict(
    dense=True, read_only=True,
    border_color=None, bgcolor=None, border=ft.InputBorder.NONE,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
readonly_field_style2: dict = dict(
    dense=True, read_only=True,
    border_color="#f2f2f2", bgcolor="#f2f2f2",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
readonly_date_style: dict = dict(
    dense=True, read_only=True,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=11, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, focused_border_width=2,
    capitalization=ft.TextCapitalization.CHARACTERS
)
date_field_style: dict = dict(
    height=45,
    focused_border_width=2, focused_border_color=MAIN_COLOR,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=13, font_family="Poppins-Medium"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)
drop_style: dict = dict(
    dense=True, height=45, border_radius=12,
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins-Medium", color="black"),
    focused_border_color=MAIN_COLOR, border_width=1,
    focused_border_width=2,
)
radio_style = dict(
    label_style=ft.TextStyle(size=12, font_family="Poppins-Medium"),
    fill_color=SECOND_COLOR
)