import pandas as pd
import argparse

from constants import MATH_LISTS, REDUNDANT_COLUMNS


def process(args):
    args = vars(args)

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    epgu_mm = epgu[epgu["Uid конкурса"].isin(MATH_LISTS)]
    print(f"Количество заявлений на матмех: {len(epgu_mm)}")

    epgu_mm.to_excel(args["Матмеховские.xlsx"], index=False, freeze_panes=(1, 0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Поиск заявлений только на матмех")
    parser.add_argument(
        "ЕГПУ.xlsx",
        help='Выгрузка "Все заявления" из ССПВО',
    )
    parser.add_argument(
        "Матмеховские.xlsx",
        help="Выходной файл",
    )

    args = parser.parse_args()
    process(args)
