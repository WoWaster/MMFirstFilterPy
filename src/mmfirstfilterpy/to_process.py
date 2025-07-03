import pandas as pd
import argparse

from constants import MATH_LISTS, REDUNDANT_COLUMNS, СОПОСТАВЛЕНИЕ_ID_КГ_ОП


def process(args):
    args = vars(args)

    oneS = pd.read_excel(args["1С.xlsx"])
    print(f"Количество анкет в 1С: {len(oneS)}")

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    # epgu_actual = epgu[epgu["Актуальность"] == "Действующее"]
    # print(f"Количество актуальных заявлений: {len(epgu_actual)}")
    epgu_actual = epgu

    epgu_first_priory = epgu_actual.loc[
        epgu_actual.groupby("Id заявления")["Приоритет"].idxmin()
    ].reset_index(drop=True)

    epgu_mm = epgu_first_priory[epgu_first_priory["Id конкурса"].isin(MATH_LISTS)]
    print(f"Количество заявлений на матмех первым приоритетом: {len(epgu_mm)}")

    joined = pd.merge(
        oneS,
        epgu_mm,
        how="inner",
        left_on="Id заявления",
        right_on="Id заявления",
    )
    joined["Обр.программа"] = joined.apply(
        lambda row: СОПОСТАВЛЕНИЕ_ID_КГ_ОП[row["Id конкурса"]], axis=1
    )
    print(
        f"Количество строк в 1С к обработке (надеюсь): {joined['Id заявления'].nunique()}"
    )
    print(f"Количество уникальных абитуриентов: {joined['Id профиля'].nunique()}")

    joined.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    joined.to_excel(args["Обработать.xlsx"], index=False, freeze_panes=(1, 0))


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
