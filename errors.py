"""Errors"""
def errors(error_name, name=""):
    """Handles errors and returns appropriate json dictionary"""
    d = {'error_info': {}}
    d['error_info']['error_name'] = error_name
    et = ""

    # General
    if error_name == "IntValueError":
        et = "Please, enter numbers, not letters."
    if error_name == "NoneTypesError":
        et = "Please, enter both arguments."
    if error_name == "NoneTypeError":
        et = "Please, enter the argument."
    if error_name == "FileNotFoundDBError":
        et = "Can't find the main database file (RU.txt)."
    if error_name == "FileNotFoundTZError":
        et = "Can't find the timezone database file (timezones.txt)."

    # city_info
    if error_name == "GeonameidValueError":
        et = "Please, enter geonameid value."
    if error_name == "NoSuchGeonameidError":
        et = "There is no such city. Please, enter valid geonameid."

    # page_with_cities
    if error_name == "PageAndNumberValueError":
        et = "Please, enter page and number values."
    if error_name == "PageValueError":
        et = "Please, enter page value."
    if error_name == "NumberValueError":
        et = "Please, enter number value."
    if error_name == "NotEnoughCitiesError":
        et = "Some of the cities are absent or there is just not enough" \
               " of them. Please, enter valid numbers."

    # two_cities
    if error_name == "City1AndCity2ValueError":
        et = "Please, enter city1 and city2 values."
    if error_name == "City1ValueError":
        et = "Please, enter city1 value."
    if error_name == "City2ValueError":
        et = "Please, enter city2 value."

    if error_name == "NoSuchCitiesError":
        et = "There are no such cities. Please, enter valid names."
    if error_name == "NoSuchCity1Error":
        et = "There is no city named as city1. Please, enter valid name."
    if error_name == "NoSuchCity2Error":
        et = "There is no city named as city2. Please, enter valid name."

    # name_hint
    if error_name == "NameValueError":
        et = "Please, enter a start of a city name."
    if error_name == "NoSuitableCities":
        et = f"There are no cities which start with '{name}'."

    d['error_info']['error_text'] = et

    return d
