import pandas as pd
import argparse

MM_LISTS = pd.Series(
    [
        "1c32f6b6-4257-475a-9998-d4f2d53913d6",  # Астрономия
        "abb23dea-769d-43d3-af5e-13e4eb775c8f",  # Астрономия
        "b87727f6-bbfc-48a1-8707-31b9e05afda3",  # Астрономия
        "f233bd3e-11b4-47b7-8d1f-c253c7849ca0",  # Астрономия
        "c34b65c1-51c5-4048-bdba-ea353461d9ee",  # ИИиНоД
        "2c134126-037e-40cf-8371-c086e4d0c473",  # ИИиНоД
        "5c5942ed-5823-4d19-adf4-fd573adac91d",  # ИИиНоД
        "24df45ba-3e10-4fc7-ab19-e4405ec273f9",  # ИИиНоД
        "ce1ced7d-7bda-4c12-a997-94b5a3309167",  # ИИиНоД
        "cc0ddc69-47c4-489e-826a-9c688d5ca09e",  # МиКН
        "49deecbf-211e-4331-9921-756fa9bafbf9",  # МиКН
        "892169ad-3ca5-4dd0-b4fd-06fd8b4f8045",  # МиКН
        "aa5797eb-3580-4a60-a54b-5c65e786cfa3",  # МиКН
        "a67f8b2c-429c-434f-a434-93b1f9eeb850",  # МиКН
        "8049bfa0-c826-4979-b2d1-f39b4942d4c4",  # МиКН
        "02f23e1a-1f99-4d6a-83de-4c79da68985f",  # МиММ
        "e8c62d07-2a3b-456b-a26d-57b8d88f2bef",  # МиММ
        "7c0d4cef-330a-4a48-8181-92d2904f95a3",  # МиММ
        "0b46920c-07c0-4ea1-bfba-76e0bdac9077",  # МиММ
        "41b072a7-e4dd-4120-b674-5f4516c08cb3",  # МиММ
        "42caef52-3b06-4e40-ada2-e9d3f3f9e188",  # ПМИ
        "5b8499c9-62c7-4e9c-89da-5d29cc334800",  # ПМИ
        "71c75eff-ae68-418c-a249-adf914529737",  # ПМИ
        "999ebebe-0383-4615-91b9-4ee85a7e1fe0",  # ПМИ
        "c43f850b-52ac-4a11-9baa-7fbe29cf0b03",  # ПМИ
        "acaf286b-dfe6-4071-a3fb-34dd44831d12",  # ПМИ
        "6b2f4498-c8d5-454b-aa8b-ef5cbfd64ec0",  # ПИ
        "ef219dda-5d1c-4884-9152-0e46871d1c87",  # ПИ
        "179d481d-fc5c-4ac1-a85f-659c48696448",  # ПИ
        "c7431414-526c-4fc8-9d52-bf5d85464a9b",  # ПИ
        "8168d89d-8cdb-4883-883b-d3d6cd44cd68",  # ПИ
        "44f22ccd-2dd6-4977-90ca-ed4ccd885660",  # ТП
        "343b0c31-a603-4654-a869-e045fa2ba707",  # ТП
        "6fb7d759-46bc-4c17-bc30-679bd8435be6",  # ТП
        "50bd93f0-5fb9-479b-bb60-7e53416d915f",  # ТП
        "c0872c5c-476f-4407-b592-892c8cfe7217",  # ТП
        "07ace51d-66ea-4145-9221-9bd92f29e11e",  # ФундМат
        "e84b0722-4543-4351-919d-8ed744287944",  # ФундМат
        "b4d80ca9-7d93-4d6c-a962-b8d66dea66df",  # ФундМат
        "ad039d29-6850-4f44-9720-4abd46e18318",  # ФундМат
        "c99a78d8-7ce1-42c2-9d72-1bef636a32ca",  # ФундМат
        "7ace5020-3f76-4665-a050-858c384149c4",  # ФундМех
        "3d043ab7-81d6-4ed0-b3b3-dca7c4eaad54",  # ФундМех
        "a932bbb0-7d8f-4fbf-8f88-6a9e2aec2bc1",  # ФундМех
        "e60699ab-3efc-49e1-a0ea-4cf72476a1c9",  # ФундМех
        "bcf33059-eb42-4ed2-b286-a9f7d4689e45",  # ФундМех
    ]
)


def process(args):
    args = vars(args)

    oneS = pd.read_excel(args["1С.xlsx"])
    print(f"Количество анкет в 1С: {len(oneS)}")

    epgu = pd.read_excel(args["ЕГПУ.xlsx"])
    print(f"Количество заявлений в СПбГУ: {len(epgu)}")

    epgu_mm = epgu[epgu["Uid конкурса"].isin(MM_LISTS)]
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

    joined.to_excel(args["Обработать.xlsx"])


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
