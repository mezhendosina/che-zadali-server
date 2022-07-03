from bs4 import BeautifulSoup
import pandas as pd


class Grades:
    def __init__(self, html: str):
        self.html = html

    def get_options(self) -> dict:
        data = {}
        soup = BeautifulSoup(self.html, "lxml")

        form_controls = soup.find_all("div", class_="filters-panel col-md-12")[0].find_all("div",
                                                                                           "col-md-8 col-lg-5 col-sm-8")

        for item in form_controls:
            select_tag = item.find_all("select")
            inputs_tag = item.find_all("input")

            if len(select_tag) != 0:
                options_item = select_tag[0].find_all("option")
                option_list = []

                selected_item = select_tag[0].find("option", selected="")

                for select_item in options_item:
                    is_selected = False

                    if selected_item == select_item:
                        is_selected = True

                    option_list.append(
                        {
                            "name": select_item.get_text(),
                            "value": select_item["value"],
                            "is_selected": is_selected
                        }
                    )

                data.update({select_tag[0]["name"]: option_list})
            elif len(inputs_tag) != 0:
                input_item = {}

                name = ""
                value = ""
                item_type = ""

                for input_tag in inputs_tag:
                    if input_tag["type"] == "text":
                        name = input_tag["value"]
                    elif input_tag["type"] == "hidden":
                        item_type = input_tag["name"]
                        value = input_tag["value"]
                input_item.update({item_type: {"name": name, "value": value}})

                data.update(input_item)
        return data

    def extract(self) -> str:
        soup = BeautifulSoup(self.html, features="lxml").find("table", class_="table-print")
        table = pd.read_html(str(soup), encoding="utf-8", skiprows=1, thousands=".", decimal=",", header=0)[0]

        table.columns = [
            i.replace("Предмет", "name")
            .replace("Ср. балл", "avg")
            .replace('\"', "")
            .replace("5", "five")
            .replace("4", "four")
            .replace("3", "three")
            .replace("2", "two")
            .replace("1", "one") for i in
            table.columns]

        return table.to_json(orient="records")


if __name__ == "__main__":
    with open("html.html", "r", encoding="utf-8") as f:
        print(Grades(f).get_options())
