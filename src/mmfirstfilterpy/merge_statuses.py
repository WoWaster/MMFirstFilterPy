import pandas as pd
import argparse

from constants import MATH_LISTS, REDUNDANT_COLUMNS


def process(args):
    args = vars(args)

    new = pd.read_excel(args["Новые.xlsx"])

    old = pd.read_excel(args["Старые.xlsx"])
    # old = old.drop(
    #     columns=[
    #         "Период",
    #         "Статус обработки",
    #         "Есть необработанные",
    #         "UID профиля",
    #         # "UID заявления",
    #         "СНИЛС_x",
    #         "Бюджет",
    #         "ФИО",
    #         "Guid заявления",
    #         "Uid конкурса",
    #         "Наименование конкурсной группы",
    #         "Вид мест",
    #         "Приоритет",
    #         "Статус",
    #         "Подан бумажный оригинал",
    #         "Подан электронный оригинал",
    #         "Вуз, в который подан оригинал",
    #     ],
    # )
    # old.loc[old["Статус клиента"] == 1] = ""

    joined = pd.merge(new, old, how="left", on=["UID заявления"])

    joined.to_excel(args["Обработать.xlsx"], index=False, freeze_panes=(1, 0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обновление таблицы на обработку")
    parser.add_argument(
        "Новые.xlsx",
        help="Таблица с новыми заявлениями на обработку",
    )
    parser.add_argument(
        "Старые.xlsx",
        help="Таблица с новыми заявлениями на обработку",
    )
    parser.add_argument(
        "Обработать.xlsx",
        help="Выходной файл",
    )

    args = parser.parse_args()
    process(args)
