import csv
from datetime import datetime
from constant import COL_DATE, COL_PRICE_CLOSE



def normalize_price(price: str):
    # convert from str to float: Example: 1,23 to 1.23
    return float(price.replace(',', '.').strip())


def normalize_date(s: str):
    # normalize dates to Y/m/d format to make it easier to sort by date. Example: '1/5/2022' -> '2022/05/01'
    d, m, y = map(int, s.split('/'))
    # result = datetime(y, m, d).strftime("%d/%m/%Y").strip()
    result = datetime(y, m, d).strftime("%Y-%m-%d").strip()
    return result


def write_data_to_csv(data, filename):
    # write data into file csv
    field_names= [COL_DATE, COL_PRICE_CLOSE]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
