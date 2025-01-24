import sqlite3 as sql
import datetime
import time

my_base = "stock.db"


def convert_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
        return photo_image


def connexion():
    conn = sql.connect(my_base)
    cur = conn.cursor()

    # Table produits
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT NOT NULL,
            product_type BLOB NOT NULL,
            box_number INTEGER,
            price NUMERIC,
            reduction NUMERIC,
            promo_price NUMERIC,
            section TEXT,
            is_in_promo INTEGER,
            image BLOB,
            stock INTEGER
        )
    """)

    # Tables des entrées
    cur.execute("""
       CREATE TABLE IF NOT EXISTS entrees (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           creation_date  TEXT,
           creation_hour  TEXT,
           creation_month  TEXT,
           created_by   TEXT,
           numero_reception  TEXT,
           montant   NUMERIC
       )
    """)

    # Tables des détails entrées
    cur.execute("""
       CREATE TABLE IF NOT EXISTS entrees_details (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           creation_at  TEXT,
           numero  TEXT,
           designation  TEXT,
           qte   INTEGER,
           prix   NUMERIC
       )
    """)

    # Tables des factures
    cur.execute("""
       CREATE TABLE IF NOT EXISTS factures (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           creation_date  TEXT,
           creation_hour  TEXT,
           creation_month  TEXT,
           created_by   TEXT,
           numero_fac  TEXT,
           montant   NUMERIC
       )
    """)

    # Tables des détails factures
    cur.execute("""
       CREATE TABLE IF NOT EXISTS factures_details (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           creation_at  TEXT,
           numero  TEXT,
           designation  TEXT,
           qte   INTEGER,
           prix   NUMERIC
       )
    """)

    # Table historique
    cur.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type  TEXT,
            designation TEXT,
            date TEXT, 
            numero_reference TEXT,
            qte_mvt INTEGER,
            stock_avant INTEGER,
            stock_apres INTEGER
        )
    """)

    # Tables des inventaires
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventaires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at  TEXT,
            numero  TEXT,
            montant NUMERIC,
            statut   TEXT,
            nb_ref   INTEGER
        )
    """)

    # Tables des details inventaires
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventaires_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_inv  TEXT,
            date  TEXT,
            designation  NUMERIC,
            prix   NUMERIC,
            qte_theorique   INTEGER,
            qte_physique   INTEGER,
            ecart    NUMERIC,
            ecart_montant   NUMERIC
        )
    """)

    # Tables des utilisateurs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at  TEXT,
            created_by  TEXT,
            name  TEXT,
            login   TEXT,
            password   TEXT,
            rights   TEXT
        )
    """)

    conn.commit()
    conn.close()


def find_all_users():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT login, password FROM users""")
    all_users = cur.fetchall()
    final = [{"login": user[0], "password": user[1]} for user in all_users]
    conn.commit()
    conn.close()
    return final


def all_products():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products""")
    products = cur.fetchall()
    final = [
        {
            "id": item[0], "designation": item[1], "product_type": item[2], "box_number": item[3], "price": item[4],
            "reduction": item[5], "promo_price": item[6], "section": item[7], "is_in_promo": item[8],
            "image": item[9], "stock": item[10]
        }
        for item in products
    ]
    conn.commit()
    conn.close()
    return final


def one_product_stock(designation):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM products WHERE designation = ?""", (designation,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[10]


def update_product(price, reduction, promo_price, is_in_promo, designation):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """UPDATE products SET
            price = ?,
            reduction = ?,
            promo_price = ?,
            is_in_promo = ? 
            WHERE designation = ?
        """, (price, reduction, promo_price, is_in_promo, designation)
    )
    conn.commit()
    conn.close()


def update_stock_product(stock, designation):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """UPDATE products SET
            stock = ?
            WHERE designation = ?
        """, (stock, designation)
    )
    conn.commit()
    conn.close()


def add_product(designation, product_type, box_number, price, reduction, promo_price, section, is_in_promo, image, stock):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO products values (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (cur.lastrowid,  designation, product_type, box_number, price, reduction, promo_price, section, is_in_promo, image, stock)
    )
    conn.commit()
    conn.close()


def product_history(designation):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM historique WHERE designation = ? ORDER BY id DESC""", (designation,)
    )
    result = cur.fetchall()
    final = [
        { "id": row[0], "type": row[1], "designation": row[2], "date": row[3], "numero_reference": row[4], "qte_mvt": row[5],
          "stock_avant": row[6], "stock_apres": row[7]} for row in result
    ]
    conn.commit()
    conn.close()
    return final


def product_by_type(product_type):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM products WHERE product_type = ?""", (product_type,)
    )
    result = cur.fetchall()
    final = [
        {
            "id": item[0], "designation": item[1], "product_type": item[2], "box_number": item[3], "price": item[4],
            "reduction": item[5], "promo_price": item[6], "section": item[7], "is_in_promo": item[8],
            "image": item[9], "stock": item[10]
        }
        for item in result
    ]
    conn.commit()
    conn.close()
    return final


def all_inventaires():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM inventaires"""
    )
    result = cur.fetchall()
    final = [
        {"id": row[0], "created_at": row[1], "numero": row[2], "montant": row[3], "statut": row[4], "nb_ref": row[5]} for row in result
    ]
    conn.commit()
    conn.close()
    return final


def inventaires_details_by_numero(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM inventaires_details WHERE numero_inv = ?""", (numero, )
    )
    result = cur.fetchall()
    final = [
        {"id": row[0], "numero_inv": row[1], "date": row[2], "designation": row[3], "prix": row[4],
         "qte_theorique": row[5], "qte_physique": row[6], "ecart": row[7], "ecart_montant": row[8]} for row in result
    ]
    conn.commit()
    conn.close()
    return final


def update_inventaires_details(qte_physique, ecart, ecart_montant, inv_id):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """UPDATE inventaires_details SET
            qte_physique = ?,
            ecart = ?,
            ecart_montant = ?
            WHERE id = ?
        """, (qte_physique, ecart, ecart_montant, inv_id)
    )
    conn.commit()
    conn.close()


def update_montant_inventaires(montant, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """UPDATE inventaires SET
            montant = ?
            WHERE numero = ?
        """, (montant, numero)
    )
    conn.commit()
    conn.close()


def update_statut_inventaires(statut, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """UPDATE inventaires SET
            statut = ?
            WHERE numero = ?
        """, (statut, numero)
    )
    conn.commit()
    conn.close()


def add_inventaire_details(numero_inv, date, designation, prix, qte_theorique, qte_physique, ecart, ecart_montant):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO inventaires_details values (?,?,?,?,?,?,?,?,?)
        """, (cur.lastrowid, numero_inv, date, designation, prix, qte_theorique, qte_physique, ecart, ecart_montant)
    )
    conn.commit()
    conn.close()


def add_inventaire(created_at, numero, montant, statut, nb_ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO inventaires values (?,?,?,?,?,?)
        """, (cur.lastrowid, created_at, numero, montant, statut, nb_ref)
    )
    conn.commit()
    conn.close()


def product_not_food(product_type="FOOD"):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM products WHERE product_type != ?""", (product_type,)
    )
    result = cur.fetchall()
    final = [
        {
            "id": item[0], "designation": item[1], "product_type": item[2], "box_number": item[3], "price": item[4],
            "reduction": item[5], "promo_price": item[6], "section": item[7], "is_in_promo": item[8],
            "image": item[9], "stock": item[10]
        }
        for item in result
    ]
    conn.commit()
    conn.close()
    return final


def all_entrees():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entrees""")
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_date": row[1], "creation_hour": row[2], "creation_month": row[3], "created_by": row[4],
            "numero_reception": row[5], "montant": row[6]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def add_entree(creation_month, created_by, numero_reception, montant):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO entrees values (?,?,?,?,?,?,?)""",(cur.lastrowid, str(datetime.date.today()), datetime.datetime.now().strftime("%H:%M:%S"), creation_month, created_by, numero_reception, montant)
    )
    conn.commit()
    conn.close()


def add_entree_details(numero, designation, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO entrees_details values (?,?,?,?,?,?)""", (cur.lastrowid, datetime.datetime.now().strftime("%H:%M:%S"), numero, designation, qte, prix)
    )
    conn.commit()
    conn.close()


def entrees_by_period(creation_month):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entrees WHERE creation_month = ?""", (creation_month,))
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_date": row[1], "creation_hour": row[2], "creation_month": row[3], "created_by": row[4],
            "numero_reception": row[5], "montant": row[6]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def all_entrees_details():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entrees_details""")
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_at": row[1], "numero": row[2], "designation": row[3], "qte": row[4], "prix": row[5]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def entrees_details_by_numero(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entrees_details WHERE numero =?""", (numero,))
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_at": row[1], "numero": row[2], "designation": row[3], "qte": row[4], "prix": row[5]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def add_historique(typp, designation, date, numero_reference, qte_mvt, stock_avant, stock_apres):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO  historique values (?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, typp, designation, date, numero_reference, qte_mvt, stock_avant, stock_apres))
    conn.commit()
    conn.close()


def all_factures():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM factures""")
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_date": row[1], "creation_hour": row[2], "creation_month": row[3],
            "created_by": row[4], "numero_fac": row[5], "montant": row[6]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def add_factures(creation_month, created_by, numero_fac, montant):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO factures values (?,?,?,?,?,?,?)""",
                (cur.lastrowid, str(datetime.date.today()), datetime.datetime.now().strftime("%H:%M:%S"), creation_month, created_by, numero_fac, montant))
    conn.commit()
    conn.close()


def factures_by_period(creation_month):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM factures WHERE creation_month = ?""", (creation_month, ))
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_date": row[1], "creation_hour": row[2], "creation_month": row[3],
            "created_by": row[4], "numero_fac": row[5], "montant": row[6]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def add_factures_details(numero, designation, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO factures_details values (?,?,?,?,?,?)""",
        (cur.lastrowid, str(datetime.date.today()), numero, designation, qte, prix)
    )
    conn.commit()
    conn.close()


def factures_details_by_numero(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM factures_details WHERE numero =?""", (numero,))
    result = cur.fetchall()
    final = [
        {
            "id": row[0], "creation_at": row[1], "numero": row[2], "designation": row[3], "qte": row[4], "prix": row[5]
        }
        for row in result
    ]
    conn.commit()
    conn.close()
    return final


def delete_inventaire(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM inventaires WHERE numero = ?""", (numero, ))
    conn.commit()
    conn.close()


def delete_inventaires_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM inventaires_details WHERE numero_inv = ?""", (numero, ))
    conn.commit()
    conn.close()

