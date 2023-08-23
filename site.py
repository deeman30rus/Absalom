from records import parse_message, Record, Lap
from dateutil.parser import parse
import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

l1 = [
    Lap.parse_string("00:01:26.823"),
    Lap.parse_string("00:01:24.625"),
    Lap.parse_string("00:01:32.154"),
    Lap.parse_string("00:01:24.743"),
    Lap.parse_string("00:01:28.006"),
]


l2 = [
    Lap.parse_string("00:01:35.797"),
    Lap.parse_string("00:01:37.027"),
    Lap.parse_string("00:01:37.023"),
    Lap.parse_string("00:01:32.876"),
    Lap.parse_string("00:01:37.335"),
]

l3 = [
    Lap.parse_string("00:01:35.549"),
    Lap.parse_string("00:01:36.459"),
    Lap.parse_string("00:01:37.194"),
    Lap.parse_string("00:01:30.375"),
    Lap.parse_string("00:01:36.583"),
]

r1 = Record("Аркадий", l1)
r2 = Record("Ирина", l2)
r3 = Record("Стас", l3)

text = """
Мультитаймер Список кругов
Мидас 
№ ; Duration ; Круг
1 ; 00:00:31.940 ; 00:00:31.940
2 ; 00:00:35.648 ; 00:00:03.708
3 ; 00:00:38.230 ; 00:00:02.582
4 ; 00:00:56.686 ; 00:00:18.456
""".strip()

def test_table():
    records = [r1, r2, r3]

    df = pd.DataFrame()

    df['#'] =  ['total:'] + list(range(calc_max(records)))

    for r in records: 
        df[r.person()] = [str(r.laps_total())] + [ str(l) for l in r.laps()] 

    fig,ax = render_mpl_table(df, header_columns=0, col_width=2.0)
    fig.savefig("/Users/theroom101/Desktop/table_mpl.png")

    # df['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '', '']
    # df['calories'] = [2200, 2100, 1500, 123, 123]
    # df['sleep hours'] = [8, 7.5, 8.2, 8.2, 9.1]
    # df['gym'] = [True, False, False, True, True]


    # print(r.microsecond / 1000)

def test_laps():
    l = Lap.parse_string("00:01:01:001")

    ts = l.total_millis()

    print(l)
    print(Lap.create_from_timestamp(ts))

def main(): 
   test_table()
    
if __name__ == "__main__":
    main()