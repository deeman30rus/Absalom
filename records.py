from datetime import datetime
from dateutil.parser import parse

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Lap: 
    _minutes = 0
    _seconds = 0
    _millis = 0

    def __init__(self, minutes: int, seconds: int, millis: int) -> None:
        self._minutes = minutes
        self._seconds = seconds
        self._millis = millis

    def __str__(self) -> str:
        min = sec = mls = ""

        if self._minutes < 10:
            min = "0" + str(self._minutes)
        else: 
            min = str(self._minutes)

        if self._seconds < 10: 
            sec = "0" + str(self._seconds)
        else:
            sec = str(self._seconds)
        
        if self._millis < 10: 
            mls = "00" + str(self._millis)
        elif self._millis < 100: 
            mls = "0" + str(self._millis)
        else: 
            mls = str(self._millis)
        

        return "{m}:{s}.{ml}".format(m=min, s=sec, ml=mls)

    def total_millis(self) -> int: 
        return self._minutes * 60 * 1000 + self._seconds * 1000 + self._millis

    def _parse_string(self, string: str) -> None: 
        self._millis = self._parse_millis(string)
        self._seconds = self._parse_seconds(string)
        self._minutes = self._parse_minutes(string)

    @classmethod
    def create_from_timestamp(cls, ts: int):
        return Lap(
            minutes=Lap._minutes_in_timestamp(ts),
            seconds=Lap._seconds_in_timestamp(ts),
            millis=Lap._millis_in_timestamp(ts),
        )

    @classmethod
    def parse_string(cls, string: str): 
        return Lap(
            minutes=Lap._parse_minutes(string),
            seconds=Lap._parse_seconds(string),
            millis=Lap._parse_millis(string),
        )

    @classmethod
    def _parse_millis(cls, string: str) -> int:
        return int(string[-3:])

    @classmethod
    def _parse_seconds(cls, string: str) -> int:
        return int(string[-6:-4])

    @classmethod
    def _parse_minutes(cls, string: str) -> int:
        return int(string[-9:-7])

    @classmethod 
    def _minutes_in_timestamp(cls, ts: int) -> int:
        return ts // (60 * 1000)
    
    @classmethod
    def _seconds_in_timestamp(cls, ts: int) -> int: 
        r = ts // 1000

        return r % 60

    @classmethod
    def _millis_in_timestamp(cls, ts: int) -> int:
        return ts % 1000


class Record:
    __person = ""
    __laps: list[Lap] = []

    def __init__(self, name: str, laps: list[Lap]) -> None:
        self.__person = name
        self.__laps = laps

    def person(self) -> str: 
        return self.__person

    def laps(self) -> list[datetime]:
        return self.__laps

    def laps_total(self) -> Lap: # пересчитать тут, выровнять недостающие lap
        ts = sum(map(lambda x: x.total_millis(), self.__laps), 0)
        return Lap.create_from_timestamp(ts)


def parse_message(text: str) -> Record: 
    lines = text.split("\n")

    name = lines[1]

    laps = [__parse_lap_line(lap_line) for lap_line in lines[3:]]

    return Record(name, laps)

def __parse_lap_line(line: str) -> Lap: 
    l = "".join(line.split())

    return __parse_time_string(l.split(";")[2])

def __parse_time_string(string: str) -> Lap:
    # парсим время в формате 00:00:32.051

    return Lap.parse_string(string)

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax

def calc_max(records: list[Record]) -> int:
    return max([len(r.laps()) for r in records])


def save_table(records: list[Record]) -> str:

    df = pd.DataFrame()

    max = calc_max(records)

    df['#'] =  ['total:'] + list(range(max))

    for r in records: 
        df[r.person()] = [str(r.laps_total())] + [ str(l) for l in r.laps() ] + [ None ] * (max - len(r.laps()))

    ts = datetime.now()
    filedir = os.environ['TIMER_IMG_DIR']
    filename = "{dir}/{png_name}.png".format(dir=filedir, png_name=ts)
    # filename = "/Users/theroom101/Desktop/table_mpl.png"
    # filename = "/img/{t}.png".format(t=ts)

    fig,ax = render_mpl_table(df, header_columns=0, col_width=2.0)
    fig.savefig(filename)

    return filename