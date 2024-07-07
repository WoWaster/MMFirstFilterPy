import pandas as pd
import argparse

from constants import MATH_LISTS, REDUNDANT_COLUMNS


def process(args):
    args = vars(args)

    oneS = pd.read_excel(args["1С.xlsx"])
    print(f"Количество анкет в 1С: {len(oneS)}")

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    epgu_mm = epgu[epgu["Uid конкурса"].isin(MATH_LISTS)]
    print(f"Количество заявлений на матмех: {len(epgu_mm)}")

    epgu_mm_fst = epgu_mm[epgu_mm["Приоритет"] == 1]
    print(f"Количество заявлений на матмех первым приоритетом: {len(epgu_mm_fst)}")

    joined = pd.merge(
        oneS,
        epgu_mm_fst,
        how="inner",
        left_on="UID профиля",
        right_on="Guid поступающего",
    )
    print(f"Количество строк в 1С с первым приоритетом (с дублями): {len(joined)}")

    print(f"Количество уникальных абитуриентов: {joined["UID профиля"].nunique()}")

    joined.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    joined.to_excel(args["Обработать.xlsx"], index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Поиск абитуриентов с первым приоритетом"
    )
    parser.add_argument(
        "1С.xlsx",
        help="Выгрузка из 1С в формате .xlsx",
    )
    parser.add_argument(
        "ЕГПУ.xlsx",
        help='Выгрузка "Все заявления" из ССПВО',
    )
    parser.add_argument(
        "Обработать.xlsx",
        help="Выходной файл",
    )

    args = parser.parse_args()
    process(args)
