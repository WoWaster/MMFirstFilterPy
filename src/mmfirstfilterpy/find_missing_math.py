import pandas as pd
import argparse

from constants import MATH_LISTS


def process(args):
    args = vars(args)

    oneS = pd.read_excel(args["1С.xlsx"])
    print(f"Количество анкет в 1С: {len(oneS)}")

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    epgu_mm = epgu[epgu["Uid конкурса"].isin(MATH_LISTS)]
    print(f"Количество заявлений на матмех: {len(epgu_mm)}")

    oneS_uids = oneS["UID профиля"]

    lost = epgu_mm.query("`Guid поступающего` not in @oneS_uids")
    print(f"Количество потеряшек (с дублями): {len(lost)}")

    print(f"Количество уникальных абитуриентов: {lost["Guid поступающего"].nunique()}")

    # joined.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    lost.to_excel(args["Потеряшки-мм.xlsx"], index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Поиск потеряшек на матмехе")
    parser.add_argument(
        "1С.xlsx",
        help="Выгрузка из 1С в формате .xlsx",
    )
    parser.add_argument(
        "ЕГПУ.xlsx",
        help='Выгрузка "Все заявления" из ССПВО',
    )
    parser.add_argument(
        "Потеряшки-мм.xlsx",
        help="Выходной файл",
    )

    args = parser.parse_args()
    process(args)
