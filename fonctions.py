import re
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pendulum
import pytz

data = pd.read_excel(r"kholloscope_full.xls")


def bad_to_good(raw: str) -> dict:
    """
    :param raw: de la forme "nom (jour 00h, SALLE5)"
    :return: dictionnaire avec les clés "nom", "day", "start_hour", "room"
    """
    keys = ("name", "day", "start_hour", "room")
    pattern = r"(.+) \((\w{3}) (\d{2}h), (.+)\)"
    result = re.search(pattern, raw)
    return dict(zip(keys, result.groups()))


def find_lines(column, group):
    indexs = []
    for i, elem in enumerate(column):
        if elem == group:
            indexs.append(i)
    return indexs


def _find_info_on_line(i, data):
    return bad_to_good(data["profs"][i])


def request_info(group, week_num, data) -> list[dict, dict]:
    L = []
    column = data[week_num]
    indexs = find_lines(column, group)
    for i in indexs:
        dico = _find_info_on_line(i, data)
        dico["matiere"] = _matiere(i)
        dico["week_num"] = week_num
        L.append(dico)
    return L


def _matiere(x):
    if x < 13:
        return "Maths"
    elif x <= 21:
        return "Physique"
    else:
        return "Anglais"


keys = list(range(1, 23))
d = ['13/09', '20/09', '27/09', '04/10', '11/10', '18/10', '08/11', '15/11', '22/11', '29/11', '06/12', '13/12',
     '03/01', '10/01', '17/01', '24/01', '31/01', '21/02', '28/02', '07/03', '14/03', '21/03']
dicj = {"lun": 0, "mar": 1, "mer": 2, "jeu": 3, "ven": 4}


def formated_date(numero, mois, jour, year="2021"):
    if mois < 8:
        year = "2022"
    datetime_str = year + "-" + str(mois) + "-" + str(numero)
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d')
    newdate = datetime_obj + timedelta(days=dicj[jour])

    date_f = newdate.strftime("%Y-%m-%d")
    # print("{} + {}  ->  {}".format(datetime_str,dicj[jour],date_f))
    return date_f


def get_datetime_from_dico(dico):
    numero, mois = d[dico["week_num"] - 1].split("/")
    jour = dico["day"]
    year = "2021"
    heure = dico["start_hour"][0:2]
    if int(mois) < 8:
        year = "2022"
    datetime_str = numero + "/" + mois + "/" + year + "/" + heure
    datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y/%H')
    newdate = datetime_obj + timedelta(days=dicj[jour])
    tz = pytz.timezone("Europe/Paris")
    newdate = tz.localize(newdate)
    return newdate


def all_colles_dict(group) -> dict:
    """
    :return dict(datetime, data)
    """
    keys = []
    info = []
    for i in range(1, 22):
        a = request_info(group, i, data)
        for elem in a:
            keys.append(get_datetime_from_dico(elem))
            info.append(elem)
    return dict(zip(keys, info))


def find_next_two_colles(dico):
    now = pendulum.now()
    dico = dico
    cles = dico.keys()
    deux_colles = []
    for date in cles:
        if date > now.add(hours=- 1):
            colle = dico[date]
            colle["this_week"] = is_next_week(colle)
            deux_colles.append(colle)
        if len(deux_colles) >= 2:
            break
    return deux_colles


def is_next_week(colle):
    now = pendulum.now()
    date_time_colle = get_datetime_from_dico(colle)
    return now.weekday() > date_time_colle.weekday() or now.add(days=7) <= date_time_colle
