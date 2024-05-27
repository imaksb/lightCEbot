from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from prettytable import PrettyTable

BASE_URL = "https://oblenergo.cv.ua/shutdowns/"


EMOJI = {
    "в": "🔴",
    "з": "🟢️",
    "мз": "⚪️"
}


def is_two_digit(number):
    return 10 <= number <= 99


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Graphic(metaclass=SingletonMeta):
    graphic_table = []

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Graphic, cls).__new__(cls)
        return cls.instance

    def __print_data(self):
        table = PrettyTable()
        fields = ["group"] + [f"{i}:00" for i in range(0, 24)]

        table.field_names = fields.copy()
        for i, group_data in enumerate(self.graphic_table):
            table.add_row([f"Група {i + 1}", *group_data])

    def get_next_shutdown(self, group: int):
        row = self.get_row(group)
        hour = datetime.now().hour

        for i in range(hour, 24):
            if row[i] == "в":
                for j in range(i, 24):
                    if row[j] != "в":
                        return [i, j]

                return [i, "00"]

    def pprint_row(self, group: int):
        row = self.get_row(group)
        pretty_row = ""
        now_hour = 0

        for col in range(4):
            for i in range(6):
                tab = "\t" if not is_two_digit(now_hour) else ""
                space = " " if is_two_digit(now_hour) else ""
                pretty_row += f"{tab}{now_hour} {tab}{space}{EMOJI[row[now_hour]]}\t"
                now_hour += 1
            pretty_row += "\n"

        return pretty_row

    def get_row(self, group: int):
        return self.graphic_table[group - 1]

    async def update_graphic(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")

                new_graphic = []
                for i in range(15):
                    elem = soup.find("div", {"id": f"inf{i + 1}"})
                    children = elem.findChildren()
                    group_data = []

                    for child in children:
                        group_data.append(child.text)

                    new_graphic.append(group_data)
        return self.compare_graphic(new_graphic)

    def compare_graphic(self, new_graphic):
        if len(self.graphic_table) == 0:
            self.graphic_table = new_graphic
            return True

        for i in range(len(new_graphic)):
            if new_graphic[i] != self.graphic_table[i]:
                self.graphic_table = new_graphic
                return True
        return False


async def main():
    graphic = Graphic()
    await graphic.update_graphic()
    print(graphic.pprint_row(15))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
