from utils import *
from utils.styles import *
import backend as be
from utils.useful_functions import separate
import base64


class ArticleItem(ft.Container):
    def __init__(self, cp: object, infos: dict):
        super().__init__()
        self.cp = cp
        self.infos = infos
        # Convertir les données BLOB en image affichable
        self.base64_image = base64.b64encode(infos['image']).decode("utf-8")

        if infos["product_type"] == "BOISSON":
            icone = ft.icons.LIQUOR_OUTLINED
        else:
            icone = ft.icons.SHOPPING_CART_OUTLINED

        if infos['is_in_promo'] == 1:
            visible = True
        else:
            visible = False

        self.promo = ft.Container(
            padding=ft.padding.only(10, 3, 10, 3), border_radius=16,
            bgcolor=ft.colors.GREEN_50, border=ft.border.all(1, ft.colors.GREEN), visible=visible,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.CHECK, color=ft.colors.GREEN, size=16),
                    ft.Text("En promo", size=11)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=3
            )
        )

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=50, height=50,  # border_radius=6,
                            shape=ft.BoxShape.CIRCLE,
                            content=ft.Image(src_base64=self.base64_image, fit=ft.ImageFit.COVER),
                        ),
                        ft.TextField(
                            **readonly_field_style, value=infos["designation"], width=400, label="Désignation",
                            prefix_icon=icone
                        ),
                        ft.TextField(**readonly_field_style, value=infos["stock"], width=80, label="Qté"),
                        ft.TextField(**readonly_field_style, value=f"{separate(infos["price"])}", width=150, label="Prix"),
                        self.promo
                    ]
                ),
                ft.Row(
                    controls=[
                        CtButton(ft.icons.EDIT_OUTLINED, "Modifier", infos, self.open_edit_ref_window),
                        CtButton(ft.icons.DELETE_OUTLINED, "Supprimer", infos, None),
                    ], spacing=0
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_edit_ref_window(self, e):
        self.cp.edit_ref_window.scale = 1
        self.cp.edit_ref_window.update()
        self.cp.main_window.opacity = 0.2
        self.cp.main_window.disabled = True
        self.cp.main_window.update()


class Stock(ft.Container):
    def __init__(self, cp: object):
        super().__init__(expand=True, bgcolor="white")
        self.cp = cp

        self.title = ft.Container(
            bgcolor="#f2f2f2", border_radius=16, padding=10,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.HOME, size=36, color="black"),
                    ft.Text(**title_text_style, value="Stocks")
                ]
            )
        )

        self.search = ft.TextField(
            **search_field_style, width=300, label="Chercher", prefix_icon=ft.icons.CONTENT_PASTE_SEARCH,
            on_change=self.filter_datas
        )
        self.results = ft.Text(**normal_text_style, color="grey", italic=True)
        self.table = ft.ListView(expand=True, divider_thickness=1, spacing=10)
        self.new_button = ft.FloatingActionButton(
            bgcolor="black87", opacity=0.8,
            content=ft.Row([ft.Icon("add", color="white")], alignment=ft.MainAxisAlignment.CENTER),
            scale=0.8, on_click=self.open_new_ref_window
        )
        self.main_window = ft.Container(
            expand=True, padding=ft.padding.only(20, 15, 20, 15),
            border_radius=16, bgcolor="white",
            content=ft.Column(
                expand=True,
                controls=[
                    self.title,
                    ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                    ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            self.search,
                            AnyButton(MAIN_COLOR, ft.icons.FILE_OPEN, "Extraire stock", "white", 180, None)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Text(**normal_text_style, value="Table des artciles", italic=True, color="grey"),
                            self.results
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Stack(
                        expand=True,
                        controls=[
                            self.table,
                            self.new_button
                        ], alignment=ft.alignment.bottom_right
                    )
                ]
            )
        )

        # Nouvel article window
        self.des = ft.TextField(
            **field_style, prefix_icon=ft.icons.DISCOUNT_OUTLINED, width=500,
            label="Désignation"
        )
        self.prod_type = ft.Dropdown(
            **drop_style, width=170, label="Type de produit", on_change=self.on_change_type_produit,
            options=[
                ft.dropdown.Option("BOISSON"), ft.dropdown.Option("FOOD"), ft.dropdown.Option("epicerie".upper()),
            ]
        )
        self.section = ft.Dropdown(
            **drop_style, width=170, label="Section",
            options=[
                ft.dropdown.Option("CHAMPAGNE"), ft.dropdown.Option("VINS"), ft.dropdown.Option("WHISKY"),
            ]
        )
        self.box_number = ft.TextField(
            **numbers_field_style, width=120, label="Qté carton", prefix_icon=ft.icons.GIF_BOX_OUTLINED
        )
        self.prix = ft.TextField(
            **numbers_field_style, width=130, label="Prix", prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED
        )
        self.reduction = ft.TextField(
            **numbers_field_style, width=130, label="Réduction", prefix_icon=ft.icons.ATTACH_MONEY_OUTLINED
        )
        self.prix_promo = ft.TextField(
            **numbers_field_style, width=130, label="Prix Promo", prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED
        )
        self.is_promo = ft.Switch(
            track_outline_color="black", active_color=SECOND_COLOR, scale=0.7
        )
        self.selected_image = ft.Image(src="assets/not-available.webp", fit=ft.ImageFit.CONTAIN)
        self.ct_image = ft.Container(
            bgcolor="#f0f0f6", width=100, height=100, border_radius=16,
            border=ft.border.all(1, "black87"),
            content=self.selected_image
        )
        self.picture = ""
        self.cp.fp_select_image.on_result = self.selectionner_image
        self.select_button = CtButton(
            ft.icons.ADD_PHOTO_ALTERNATE_OUTLINED, "Modifier image", None,
            lambda _: self.cp.fp_select_image.pick_files(
                allow_multiple=False, allowed_extensions=['webp', "jpg", "png", "avif"]
            )
        )

        self.new_ref_window = ft.Container(
            bgcolor="#f0f0f6", width=600, height=600, border_radius=16,
            padding=10, expand=True,
            shadow=ft.BoxShadow(spread_radius=5, blur_radius=15, color=ft.colors.BLACK38),
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            content=ft.Container(
                padding=10, border_radius=16, bgcolor="white", expand=True,
                content=ft.ListView(
                    expand=True, spacing=10,
                    controls=[
                        ft.Container(
                            bgcolor="#f0f0f6", border_radius=16, padding=10,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ADD_BUSINESS_OUTLINED, size=36, color="black"),
                                            ft.Text(**title_text_style, value="Nouvel article")
                                        ]
                                    ),
                                    ft.IconButton("close", icon_color="black", bgcolor="#f0f0f6", scale=0.7, on_click=self.close_new_ref_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Nom et catégorie".upper(), weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        ft.Divider(height=2, color=ft.colors.TRANSPARENT),
                        self.des,
                        ft.Row([self.prod_type, self.section]),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Pricing".upper(),
                                        weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),ft.Divider(height=2, color=ft.colors.TRANSPARENT),

                        ft.Row([self.prix, self.prix_promo, self.reduction, self.box_number]),
                        ft.Row(
                            controls=[
                                ft.Text(**normal_text_style, value="Mettre en promo"),
                                self.is_promo
                            ]
                        ),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Image".upper(),
                                        weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        ft.Divider(height=2, color=ft.colors.TRANSPARENT),
                        ft.Row(
                            controls=[
                                ft.Stack(
                                    controls=[
                                        self.ct_image, self.select_button
                                    ], alignment=ft.alignment.bottom_right
                                ),
                                AnyButton(
                                    MAIN_COLOR, "check", "Valider", "white", 200, self.create_article
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )

                    ]
                )
            )
        )

        # Fenêtre d'édition de référence
        # Nouvel article window
        self.edit_des = ft.TextField(
            **readonly_date_style, prefix_icon=ft.icons.DISCOUNT_OUTLINED, width=500,
            label="Désignation"
        )
        self.edit_prod_type = ft.TextField(
            **readonly_date_style, prefix_icon=ft.icons.DISCOUNT_OUTLINED, width=170,
            label="Type de produit"
        )
        self.edit_section = ft.TextField(
            **readonly_date_style, prefix_icon=ft.icons.DISCOUNT_OUTLINED, width=170,
            label="Section"
        )
        self.edit_box_number = ft.TextField(
            **numbers_field_style, width=120, label="Qté carton", prefix_icon=ft.icons.GIF_BOX_OUTLINED
        )
        self.edit_prix = ft.TextField(
            **numbers_field_style, width=130, label="Prix", prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED
        )
        self.edit_reduction = ft.TextField(
            **numbers_field_style, width=130, label="Réduction", prefix_icon=ft.icons.ATTACH_MONEY_OUTLINED
        )
        self.edit_prix_promo = ft.TextField(
            **numbers_field_style, width=130, label="Prix Promo", prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED
        )
        self.edit_is_promo = ft.Switch(
            track_outline_color="black", active_color=SECOND_COLOR, scale=0.7
        )
        self.edit_selected_image = ft.Image(fit=ft.ImageFit.CONTAIN)
        self.edit_ct_image = ft.Container(
            bgcolor="#f0f0f6", width=100, height=100, border_radius=16,
            border=ft.border.all(1, "black87"),
            content=self.edit_selected_image
        )
        self.edit_picture = ""
        self.cp.fp_edit_image.on_result = None
        self.edit_select_button = CtButton(
            ft.icons.ADD_PHOTO_ALTERNATE_OUTLINED, "Modifier image", None,
            lambda _: self.cp.fp_edit_image.pick_files(
                allow_multiple=False, allowed_extensions=['webp', "jpg", "png", "avif"]
            )
        )

        self.edit_ref_window = ft.Container(
            bgcolor="#f0f0f6", width=600, height=600, border_radius=16,
            padding=10, expand=True,
            shadow=ft.BoxShadow(spread_radius=5, blur_radius=15, color=ft.colors.BLACK38),
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            content=ft.Container(
                padding=10, border_radius=16, bgcolor="white", expand=True,
                content=ft.ListView(
                    expand=True, spacing=10,
                    controls=[
                        ft.Container(
                            bgcolor="#f0f0f6", border_radius=16, padding=10,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ADD_BUSINESS_OUTLINED, size=36, color="black"),
                                            ft.Text(**title_text_style, value="Modifier article")
                                        ]
                                    ),
                                    ft.IconButton("close", icon_color="black", bgcolor="#f0f0f6", scale=0.7,
                                                  on_click=self.close_edit_ref_window)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Nom et catégorie".upper(),
                                        weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        ft.Divider(height=2, color=ft.colors.TRANSPARENT),
                        self.edit_des,
                        ft.Row([self.edit_prod_type, self.edit_section]),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Pricing".upper(),
                                        weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ), ft.Divider(height=2, color=ft.colors.TRANSPARENT),

                        ft.Row([self.edit_prix, self.edit_prix_promo, self.edit_reduction, self.edit_box_number]),
                        ft.Row(
                            controls=[
                                ft.Text(**normal_text_style, value="Mettre en promo"),
                                self.edit_is_promo
                            ]
                        ),
                        ft.Divider(height=4, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            controls=[
                                ft.Text(**normal_text_style, value="Image".upper(),
                                        weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, thickness=1)
                            ], spacing=0
                        ),
                        ft.Divider(height=2, color=ft.colors.TRANSPARENT),
                        ft.Row(
                            controls=[
                                ft.Stack(
                                    controls=[
                                        self.edit_ct_image, self.edit_select_button
                                    ], alignment=ft.alignment.bottom_right
                                ),
                                AnyButton(
                                    MAIN_COLOR, "check", "Valider", "white", 200, None
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )

                    ]
                )
            )
        )

        self.content = ft.Stack(
            controls=[
                self.main_window, self.new_ref_window, self.edit_ref_window
            ], alignment=ft.alignment.center
        )
        self.load_datas()

    def load_datas(self):
        datas = be.all_products()
        number_refs = 0

        for widget in self.table.controls[:]:
            self.table.controls.remove(widget)

        for data in datas:
            number_refs += 1
            self.table.controls.append(ArticleItem(self, data))

        self.results.value = f"{number_refs} Résultat(s)"

    def filter_datas(self, e):
        datas = be.all_products()
        number_refs = 0

        rech = self.search.value if self.search.value is not None else ""
        filtered_datas = list(filter(lambda x: rech in x["product_type"] or rech in x["designation"] or rech in x["section"], datas))

        for widget in self.table.controls[:]:
            self.table.controls.remove(widget)

        for data in filtered_datas:
            number_refs += 1
            self.table.controls.append(
                ArticleItem(self, data)
            )

        self.results.value = f"{number_refs} Résultat(s)"
        self.results.update()
        self.table.update()

    def open_new_ref_window(self, e):
        self.new_ref_window.scale = 1
        self.new_ref_window.update()
        self.main_window.opacity = 0.2
        self.main_window.disabled = True
        self.main_window.update()

    def close_new_ref_window(self, e):
        self.new_ref_window.scale = 0
        self.new_ref_window.update()
        self.main_window.opacity = 1
        self.main_window.disabled = False
        self.main_window.update()

    def selectionner_image(self, e: ft.FilePickerResultEvent):
        if not e.files:
            pass
        else:
            # enregistre l'image dans une variable en bytes
            picture = be.convert_binary(e.files[0].path)
            self.picture = picture

            # Mettre à jour l'image selectionnée
            self.selected_image.src = None
            self.selected_image.src_base64 = base64.b64encode(picture).decode("utf-8")
            self.selected_image.update()

    def on_change_type_produit(self, e):
        if self.prod_type.value == "BOISSON":
            for widget in (self.section, self.prix_promo, self.reduction, self.is_promo, self.box_number):
                widget.value = None
                widget.disabled = False
                widget.update()
        else:
            for widget in (self.section, self.prix_promo, self.reduction, self.is_promo, self.box_number):
                widget.value = None
                widget.disabled = True
                widget.update()

    # Creer un nouvel article
    def create_article(self, e):
        # Si le produit est une boisson
        if self.prod_type.value == "BOISSON":
            count = 0
            for widget in (
            self.des, self.section, self.prix, self.prix_promo, self.reduction, self.box_number):
                if widget.value is None or widget.value == "":
                    count += 1

            # S'il y a au moins un champ vide
            if count > 0:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Tous les champs actifs sont obligatoires"
                self.cp.box.open = True
                self.cp.box.update()

            # Si tous les champs sont remplis
            else:
                # Si une image est sélectionnée
                if self.picture != "":
                    in_promo = 1 if self.is_promo.value is True else 0
                    be.add_product(
                        self.des.value, self.prod_type.value,
                        int(self.box_number.value), int(self.prix.value), int(self.reduction.value),
                        int(self.prix_promo.value),
                        self.section.value, in_promo, self.picture, 0
                    )
                    self.cp.box.title.value = "Validé"
                    self.cp.box.content.value = "Produit crééé"
                    self.cp.box.open = True
                    self.cp.box.update()

                    self.load_datas()
                    self.table.update()
                    self.results.update()

                    for widget in (
                        self.des, self.section, self.prix, self.prix_promo, self.reduction,
                        self.box_number,
                        self.is_promo):
                        widget.value = None
                        widget.update()
                    self.picture = ""

                # Si aucune image n'est sélectionnée
                else:
                    picture = be.convert_binary("assets/not-available.webp")
                    in_promo = 1 if self.is_promo.value is True else 0
                    be.add_product(
                        self.des.value, self.prod_type.value,
                        int(self.box_number.value), int(self.prix.value), int(self.reduction.value),
                        int(self.prix_promo.value),
                        self.section.value, in_promo, picture, 0
                    )
                    self.cp.box.title.value = "Validé"
                    self.cp.box.content.value = "Produit crééé"
                    self.cp.box.open = True
                    self.cp.box.update()

                    self.load_datas()
                    self.table.update()
                    self.results.update()

                    for widget in (
                            self.des, self.section, self.prix, self.prix_promo, self.reduction,
                            self.box_number,
                            self.is_promo):
                        widget.value = None
                        widget.update()
                    self.picture = ""

                self.selected_image.src="assets/not-available.webp"
                self.selected_image.src_base64 = None
                self.selected_image.update()

        # Si le produit est diffrérent de boisson
        else:
            count = 0
            for widget in (self.des, self.prix):
                if widget.value is None or widget.value == "":
                    count += 1

            if count > 0:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = "Tous les champs actifs sont obligatoires"
                self.cp.box.open = True
                self.cp.box.update()
            else:
                if self.picture != "":
                    in_promo = 1 if self.is_promo.value is True else 0
                    be.add_product(
                        self.des.value, self.prod_type.value,
                        0, int(self.prix.value), 0, 0,
                        "", in_promo, self.picture, 0
                    )
                    self.cp.box.title.value = "Validé"
                    self.cp.box.content.value = "Produit crééé"
                    self.cp.box.open = True
                    self.cp.box.update()

                    self.load_datas()
                    self.table.update()
                    self.results.update()

                    for widget in (
                            self.des, self.section, self.prix, self.prix_promo, self.reduction,
                            self.box_number,
                            self.is_promo, self.prod_type):
                        widget.value = None
                        widget.update()
                    self.picture = ""

                    self.selected_image.src = "assets/not-available.webp"
                    self.selected_image.src_base64 = None
                    self.selected_image.update()

                else:
                    picture = be.convert_binary("assets/not-available.webp")
                    in_promo = 1 if self.is_promo.value is True else 0
                    be.add_product(
                        self.des.value, self.prod_type.value,
                        0, int(self.prix.value), 0, 0,
                        "", in_promo, picture, 0
                    )
                    self.cp.box.title.value = "Validé"
                    self.cp.box.content.value = "Produit crééé"
                    self.cp.box.open = True
                    self.cp.box.update()

                    self.load_datas()
                    self.table.update()
                    self.results.update()

                    for widget in (
                            self.des, self.section, self.prix, self.prix_promo, self.reduction,
                            self.box_number,
                            self.is_promo, self.prod_type):
                        widget.value = None
                        widget.update()
                    self.picture = ""

                    self.selected_image.src = "assets/not-available.webp"
                    self.selected_image.src_base64 = None
                    self.selected_image.update()

    def close_edit_ref_window(self, e):
        self.edit_ref_window.scale = 0
        self.edit_ref_window.update()
        self.main_window.opacity = 1
        self.main_window.disabled = False
        self.main_window.update()



