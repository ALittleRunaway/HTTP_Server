"""Functions for the script.py"""
import csv
from errors import errors


def reading_tsv_city_info(geonameid):
    """Reads the tsv for 'city-info' function"""
    with open("RU.txt", "r", encoding="utf-8") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter="\t")

        for row in read_tsv:
            if row[0] == geonameid:
                return row


def reading_tsv_page_with_cities(first_city, last_city):
    """Reads the tsv for 'page-with-cities' function"""
    with open("RU.txt", "r", encoding="utf-8") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        rows = []
        n = 1
        for row in read_tsv:
            if first_city <= n <= last_city:
                rows.append(row)
            if n > last_city:
                break
            n += 1
        return rows


def reading_tsv_two_cities(city1, city2):
    """Reads the tsv for 'two-cities' function"""
    with open("RU.txt", "r", encoding="utf-8") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        # -1 instead of 0, so that the template will be replaced with a city anyway (if the population is 0)
        rows = [['-1' for i in range(19)], ['-1' for i in range(19)]] # Templates for city1 and city2

        for row in read_tsv:
            if city1.lower() in row[3].lower().split(','):
                if int(row[14]) > int(rows[0][14]):
                    rows[0] = row

            if city2.lower() in row[3].lower().split(','):
                if int(row[14]) > int(rows[1][14]):
                    rows[1] = row
        return rows


def reading_tsv_name_hint(name):
    """Reads the tsv for 'name-hint' function"""
    with open("RU.txt", "r", encoding="utf-8") as tsv_file:
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        names = set() # to avoid repetitions
        for row in read_tsv:
            if row[1].lower().startswith(name.lower()):
                set.add(names, row[1])
        return names


def making_json(rows, n=1, mode="city_info"):
    """Forms the json dictionary for all functions"""
    d = {}
    if mode == "page_with_cities":
        d['cities'] = []
    for i in range(n): # Makes the basic dictionary for any city
        base_d = {}
        base_d['geonameid'] = rows[i][0]
        base_d['name'] = rows[i][1]
        base_d['asciiname'] = rows[i][2]
        base_d['alternatenames'] = rows[i][3]
        base_d['latitude'] = rows[i][4]
        base_d['longitude'] = rows[i][5]
        base_d['feature class'] = rows[i][6]
        base_d['feature code'] = rows[i][7]
        base_d['country code'] = rows[i][8]
        base_d['cc2'] = rows[i][9]
        base_d['admin1 code'] = rows[i][10]
        base_d['admin2 code'] = rows[i][11]
        base_d['admin3 code'] = rows[i][12]
        base_d['admin4 code'] = rows[i][13]
        base_d['population'] = rows[i][14]
        base_d['elevation'] = rows[i][15]
        base_d['dem'] = rows[i][16]
        base_d['timezone'] = rows[i][17]
        base_d['modification date'] = rows[i][18]
        # Puts this dictionary where it belongs to, depending on the method
        if mode == "page_with_cities":
            d['cities'].append(base_d)
        elif mode == "two_cities":
            if i == 0:
                d['city1'] = base_d
            else:
                d['city2'] = base_d
        else:
            d['city'] = base_d

    return d


def compare_timezones(city1_timezone, city2_timezone):
    """Compares timezones of two cities"""
    with open("timezones.txt", "r", encoding="utf-8") as csv_file:
        read_tsv = csv.reader(csv_file, delimiter=",")

        for row in read_tsv:
            if row[0] == city1_timezone:
                city1_time = int(row[1])
            if row[0] == city2_timezone:
                city2_time = int(row[1])

        try: # Calculates the difference time
            time_abs = int(abs(city1_time - city2_time) / 3600) # Without the sign
            time_not_abs = int((city1_time - city2_time) / 3600) # With the sign
        except: # If there is no data at the timezone database
            return False, False
        return time_abs, time_not_abs


def complete_json_two_cities(d, city1, city2):
    """Makes additional info for 'two-cities' json response"""
    d['info'] = {}

    # Latitude
    d['info']['nothern'] = {}
    if float(d['city1']['latitude']) > float(d['city2']['latitude']):
        d['info']['nothern']['geonameid'] = d['city1']['geonameid']
        d['info']['nothern']['name'] = d['city1']['name']
        d['info']['nothern']['russian_name'] = city1
    else:
        d['info']['nothern']['geonameid'] = d['city2']['geonameid']
        d['info']['nothern']['name'] = d['city2']['name']
        d['info']['nothern']['russian_name'] = city2

    # Same timezone
    if d['city1']['timezone'] == d['city2']['timezone']:
        d['info']['same_timezone'] = True
    else:
        d['info']['same_timezone'] = False

    # Timezone difference
    d['info']['timezone_difference'] = {}

    try:
        time_abs, time_not_abs = compare_timezones(d['city1']['timezone'], d['city2']['timezone'])
    except FileNotFoundError:
        return errors("FileNotFoundTZError")

    if not time_abs and not time_not_abs: # If there is no data
        d['info']['timezone_difference']['not_absolute_difference'] = 'missing data'
        d['info']['timezone_difference']['absolute_difference'] = 'missing data'
    # If the data exists
    d['info']['timezone_difference']['not_absolute_difference'] = time_not_abs
    d['info']['timezone_difference']['absolute_difference'] = time_abs

    return d


def city_info(geonameid):
    """The main 'city-info' function"""
    if geonameid == "":
        return errors("GeonameidValueError")

    try:
        row = reading_tsv_city_info(geonameid)
    except FileNotFoundError:
        return errors("FileNotFoundDBError")
    if row is None:
        return errors("NoSuchGeonameidError")

    row = [row]
    return making_json(row)


def page_with_cities(page, number):
    """The main 'page-with-cities' function"""
    if (page == "" and number == "") or (page == "0" and number == "0"):
        return errors("PageAndNumberValueError")
    if (page == "") or (page == "0"):
        return errors("PageValueError")
    if (number == "") or (number == "0"):
        return errors("NumberValueError")

    try:
        first_city = ((int(page) - 1) * int(number)) + 1
        last_city = int(page) * int(number)
    except ValueError:
        return errors("IntValueError")
    except TypeError:
        return errors("NoneTypesError")
    except AttributeError:
        return errors("NoneTypesError")

    try:
        rows = reading_tsv_page_with_cities(first_city, last_city)
    except FileNotFoundError:
        return errors("FileNotFoundDBError")

    if len(rows) != last_city - first_city + 1:
        return errors("NotEnoughCitiesError")

    return making_json(rows, len(rows), "page_with_cities")


def two_cities(city1, city2):
    """The main 'two-cities' function"""
    if city1 == "" and city2 == "":
        return errors("City1AndCity2ValueError")
    if city1 == "":
        return errors("City1ValueError")
    if city2 == "":
        return errors("City2ValueError")

    try:
        rows = reading_tsv_two_cities(city1, city2)
    except TypeError:
        return errors("NoneTypesError")
    except AttributeError:
        return errors("NoneTypesError")
    except FileNotFoundError:
        return errors("FileNotFoundDBError")

    if rows[0][14] == '-1' and rows[1][14] == '-1':
        return errors("NoSuchCitiesError")
    if rows[0][14] == '-1':
        return errors("NoSuchCity1Error")
    if rows[1][14] == '-1':
        return errors("NoSuchCity2Error")

    d = making_json(rows, len(rows), "two_cities")
    return complete_json_two_cities(d, city1, city2)


def name_hint(name):
    """The main 'name-hint' function"""
    if name == "":
        return errors("NameValueError")

    try:
        names = reading_tsv_name_hint(name)
    except TypeError:
        return errors("NoneTypeError")
    except AttributeError:
        return errors("NoneTypeError")
    except FileNotFoundError:
        return errors("FileNotFoundDBError")

    if len(names) == 0:
        return errors("NoSuitableCities", name)
    return {'possible_city_names': list(sorted(names))}
