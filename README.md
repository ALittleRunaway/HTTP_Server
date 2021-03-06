# HTTP-сервер для предоставления информации по географическим объектам.

Это HTTP-сервер, реализующий REST API с исходными данными, передаваемыми методом HTTP GET.

Результаты возвращаются в формате **json**. Данные взяты из географической базы данных GeoNames.

## Методы и их использование:

### 1. Информация о городе
Метод принимает идентификатор geonameid и возвращает информацию о городе.

`/city-info?geonameid={string}
`
### 2. Города на странице
Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией.

`/page-with-cities?page={int}&number={int}
`
### 3. Сравнение двух городов
Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее, одинаковая ли у них временная зона и если нет - на сколько часов они различаются.

`/two-cities?city1={string}&city2={string}
`
### 4. Продолжение названия
Метод принимает часть названия города (на английском языке) и возвращает подсказку с возможными вариантами продолжений.

`/name-hint?name={string}`

## Формат вывода данных
Пример для одного города:
```{
  "city":
  {
    "geonameid": "451769",
    "name": "Yavidovo",
    "asciiname": "Yavidovo",
    "alternatenames": "Javidovo,Yavidovo,Явидово",
    "latitude"          : "56.87068",
    "longitude"         : "34.51994",
    "feature class"     : "P",
    "feature code"      : "PPL",
    "country code"      : "RU",
    "cc2"               : "",
    "admin1 code"       : "77",
    "admin2 code"       : "",
    "admin3 code"       : "",
    "admin4 code"       : "",
    "population"        : "0",
    "elevation"         : "",
    "dem"               : "217",
    "timezone"          : "Europe/Moscow",
    "modification date" : ""
  }
}
```
Пример дополнительной информации для метода "two-cities":
```
  "info": {
    "nothern": {
      "geonameid": "7460571", 
      "name": "Umilen’ye", 
      "russian_name": "Умиленье"
    }, 
    "same_timezone": true, 
    "timezone_difference": {
      "not_absolute_difference": 0, # Разница по времени в часах с учётом знака
      "absolute_difference": 0 # Разница по времени в часах без учёта знака
    }
  }
```
### Требования
- Windows 10 OS
- Python interpreter
- Flask library 

### Среда выполнения
- Python 3.8.1

### Библиотеки
- Flask 1.1.2
- csv

### Протестированные конфигурации
- Windows 10, Python 3.8.1, Flask 1.1.2
- Ubuntu 18.04, Python 3.6.9, Flask 1.1.2

### Обзор архива
- **script.py** - основной скрипт, непосредственно отвечающий за создание сервера.
- **my_functions.py** - модуль с функциями, для обработки запросов.
- **errors.py** - модуль для обработки исключений.
- **RU.txt** - основная база данных с географическими объектами.
- **timezones.txt** - база данных с временными зонами.
- **templates/main_screen.html** - html файл для создания главной страницы.
- **static/css/main_screen.css** - файл со стилями для главной страницы.

### Комментарии
- В данной работе я не прибегала к использованию баз данных.
- Так же я оформила главную страницу, которая отображается при обращении к серверу без параметров. Но она может быть не идеальна, т.к. я не frontend-разработчик. Однако с её помощью работать с сервером становится намного удобнее, потому как вы сразу видите все возможные методы, к которым можно обращаться, а так же их использование.

### Благодарности
Спасибо за уделённое этому проекту время.
