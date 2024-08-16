import pandas as pd
import argparse

from constants import MATH_LISTS


def process(args):
    args = vars(args)

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    mm = epgu[epgu["Uid конкурса"].isin(MATH_LISTS)]
    # mm = epgu[
    #     epgu["Uid конкурса"].isin(
    #         [
    #             "02f23e1a-1f99-4d6a-83de-4c79da68985f",
    #             "7ace5020-3f76-4665-a050-858c384149c4",
    #         ]
    #     )
    # ]
    mm_sorted = mm.sort_values(by=["Guid поступающего", "Статус"])
    mm_unique = mm_sorted.drop_duplicates(subset=["Guid поступающего"], keep="last")
    mm_unique["Диагноз"] = mm_unique.apply(
        lambda row: (
            row["Статус"]
            if row["Статус"] == "Отозвано"
            else (
                row["Вуз, в который подан оригинал"]
                if row["Вуз, в который подан оригинал"] != "NaN"
                else ""
            )
        ),
        axis=1,
    )

    # mm_unique["СНИЛС"] = mm_unique["СНИЛС"].astype("Int64").astype(str)

    # mm_unique["СНИЛС 2"] = mm_unique.apply(
    #     lambda row: row["СНИЛС"][0:3]
    #     + "-"
    #     + row["СНИЛС"][3:6]
    #     + "-"
    #     + row["СНИЛС"][6:9]
    #     + " "
    #     + row["СНИЛС"][9:11],
    #     axis=1,
    # )

    mm_unique[
        [
            "Guid поступающего",
            "ФИО",
            # "Почта",
            # "Телефон",
            # "Пол",
            "СНИЛС",
            # "СНИЛС 2",
            "Диагноз",
        ]
    ].to_excel(args["Обработать.xlsx"], index=False, freeze_panes=(1, 0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Выгрузка диагнозов")
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
