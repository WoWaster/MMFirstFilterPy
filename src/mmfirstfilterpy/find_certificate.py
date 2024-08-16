import pandas as pd
import argparse

from constants import MATH_LISTS, REDUNDANT_COLUMNS


def process(args):
    args = vars(args)

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    epgu_first_priory = epgu.loc[
        epgu.groupby("Guid заявления")["Приоритет"].idxmin()
    ].reset_index(drop=True)

    epgu_mm = epgu_first_priory[epgu_first_priory["Uid конкурса"].isin(MATH_LISTS)]
    print(f"Количество заявлений на матмех первым приоритетом: {len(epgu_mm)}")

    changes = pd.read_excel(args["Изменения.xlsx"])
    print(f"Количество изменений: {len(changes)}")

    joined = pd.merge(
        changes,
        epgu_mm,
        how="inner",
        left_on="Guid заявления",
        right_on="Guid заявления",
    )
    print(f"Количество строк в 1С к обработке (надеюсь): {joined["Guid заявления"].nunique()}")
    # print(f"Количество уникальных абитуриентов: {joined["UID профиля"].nunique()}")

    # joined.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    joined.to_excel(args["Обработать.xlsx"], index=False, freeze_panes=(1, 0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Поиск абитуриентов с первым приоритетом"
    )
    parser.add_argument(
        "ЕГПУ.xlsx",
        help='Выгрузка "Все заявления" из ССПВО',
    )
    parser.add_argument(
        "Изменения.xlsx",
        help="Выгрузка изменений из ССПВО",
    )
    parser.add_argument(
        "Обработать.xlsx",
        help="Выходной файл",
    )

    args = parser.parse_args()
    process(args)
