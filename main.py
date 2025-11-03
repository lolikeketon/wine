import collections
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler


from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel


def pluralize_year(year):
    if year % 10 == 0 or 5 <= year % 10 <= 9 or 11 <= year % 100 <= 14:
        return 'лет'
    elif 2 <= year % 10 <= 4:
        return 'года'
    return 'год'


def excel_for_dict(path):
    excel_data = read_excel(path, keep_default_na=False).to_dict(orient="records")
    normalized_excel = collections.defaultdict(list)

    for drink in excel_data:
        normalized_excel[drink['Категория']].append(drink)

    return normalized_excel


def make_page(years, data):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    html = template.render(
        years_with_you=years,
        pluralize=pluralize_year(years),
        data=data
    )

    with open('index.html', 'w', encoding="utf-8") as f:
        f.write(html)


def main():
    years = (datetime.now() - datetime(1920, 1, 1)).days // 365
    data = excel_for_dict('wine3.xlsx')

    make_page(years, data)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print("Переходи тут: http://127.0.0.1:8000")

    server.serve_forever()


if __name__ == '__main__':
    main()
