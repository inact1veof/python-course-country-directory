"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """
        main_info = [
            "Основное",
            f"Страна: {self.location_info.location.name}",
            f"Столица: {self.location_info.location.capital}",
            f"Регион: {self.location_info.location.subregion}",
            f"Языки: {await self._format_languages()}",
            f"Население страны: {await self._format_population()} чел.",
        ]

        geo_info = [
            "География",
            f"Долгота: {self.location_info.location.longitude}",
            f"Широта: {self.location_info.location.latitude}",
            f"Площадь страны: {self.location_info.location.area} км^2",
        ]

        weather_info = [
            "Погода",
            f"Температура: {self.location_info.weather.temp} °C",
            f"Скорость ветра: {self.location_info.weather.wind_speed} м/c",
            f"Видимость: {self.location_info.weather.visibility} метров",
            f"Характеристика: {self.location_info.weather.description}",
        ]

        another_info = [
            "Доп.инфо",
            f"Курсы валют: {await self._format_currency_rates()}",
            f"Местное время: {self.location_info.weather.dt.strftime('%H:%M')}",
            f"Часовой пояс: UTC + {self.location_info.weather.timezone}",
        ]
        all_info = [main_info, geo_info, weather_info, another_info]
        strings = ["", "", "", "", "", ""]
        columns_len = [0, 0, 0, 0]
        for col_item in range(0, len(all_info)):
            columns_len[col_item] = max(len(item) for item in all_info[0]) + 1
        for str_item in range(0, len(main_info)):
            res = ""

            for item in range(0, len(all_info)):
                if str_item >= len(all_info[item]):
                    res += (" " * (columns_len[item] - 1)) + "|"
                else:
                    res += (
                        str(all_info[item][str_item])
                        + (
                            " "
                            * ((columns_len[item] - len(all_info[item][str_item])) - 1)
                        )
                        + "|"
                    )
            all_long = ""
            for len_col in range(0, len(all_info)):
                all_long += ("-" * (columns_len[len_col] - 1)) + "|"
            res += "\n" + all_long
            strings[str_item] = res
        if self.location_info.news is not None:
            count = min([3, len(self.location_info.news)])
            for i in range(0, count):
                news_item = f"Новость {i+1}: {self.location_info.news[i].title} | {self.location_info.news[i].author} | {self.location_info.news[i].published_at}"
                strings.append(news_item)
        else:
            strings.append("К сожалению, новостей нет")
        return tuple(strings)

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
