def find_month_facture(string_date: str):
    """This function writes the _date of the day"""

    def find_month_name(month_number):
        year_months = [
            'janv', "Fev", "Mar", "Avr", "Mai", "Jun",
            "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"
        ]
        return year_months[month_number - 1]

    the_month = int(string_date[5: 7])
    the_year = string_date[0: 4]

    return f"{the_year}_{find_month_name(the_month).upper()}"


def write_date(string_date: str):
    """This function writes the _date of the day"""

    def find_month_name(month_number):
        year_months = [
            'janvier', "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        return year_months[month_number - 1]

    the_year = string_date[0: 4]
    the_month = string_date[5: 7]
    the_day = string_date[8:10]
    month_name = find_month_name(int(the_month))
    return str(the_day) + " " + month_name + " " + str(the_year)


def separate(my_number: int):
    string_number = str(my_number)[::-1]
    result = ""
    for i, string_number in enumerate(string_number, 1):
        formatted_number = string_number + " " if i % 3 == 0 and i != len(string_number) else string_number
        result += formatted_number

    return result[::-1]
