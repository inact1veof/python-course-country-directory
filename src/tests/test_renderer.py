"""
Тестирование функций генерации выходных данных.
"""

import pytest
from collectors.models import (
    CountryDTO,
    CurrencyInfoDTO,
    LanguagesInfoDTO,
    LocationInfoDTO,
    NewsInfoDTO,
    WeatherInfoDTO,
)
from renderer import Renderer


class TestRenderer:
    location = LocationInfoDTO(
        location=CountryDTO(
            alpha2code="RU",
            capital="Moscow",
            currencies={CurrencyInfoDTO(code="USD")},
            languages={LanguagesInfoDTO(name="Russian", native_name="Русский")},
            flag="test",
            subregion="test",
            name="Russia",
            population=3,
            area=3,
            longitude=3,
            latitude=3,
            alt_spellings=["test"],
            timezones=[3],
        ),
        weather=WeatherInfoDTO(
            timezone=3,
            temp=3,
            pressure=3,
            humidity=3,
            wind_speed=3,
            visibility=3,
            dt=1,
            description="test",
        ),
        currency_rates={"USD": 1.0},
        news=[
            NewsInfoDTO(
                source="test",
                published_at=0,
                title="test",
                content="test",
                description="test",
                url="test",
                url_to_image="test",
            )
        ],
    )

    @pytest.mark.asyncio
    async def test_render(self):
        renderer = Renderer(self.location)
        results = await renderer.render()
        assert len(results) == 7

    @pytest.mark.asyncio
    async def test_format_languages(self):
        renderer = Renderer(self.location)
        result = await renderer._format_languages()
        assert result == "Russian (Русский)"

    @pytest.mark.asyncio
    async def test_format_currencies_rates(self):
        renderer = Renderer(self.location)
        result = await renderer._format_currency_rates()
        assert result == "USD = 1.00 руб."

    @pytest.mark.asyncio
    async def test_format_population(self):
        renderer = Renderer(self.location)
        result = await renderer._format_population()
        assert result == "3"

    @pytest.mark.asyncio
    async def test_format_table(self):
        renderer = Renderer(self.location)
        result = await renderer.render()

        main_info = [
            "Основное",
            f"Страна: 1",
            f"Столица: 1",
            f"Регион: 1",
            f"Языки: 1",
            f"Население страны: 1",
        ]

        geo_info = ["География", f"Долгота: 1", f"Широта: 1", f"Площадь страны: 1"]

        weather_info = [
            "Погода",
            f"Температура: 1",
            f"Скорость ветра: 1",
            f"Видимость: 1",
            f"Характеристика: 1",
        ]

        another_info = [
            "Доп.инфо",
            f"Курсы валют: 1",
            f"Местное время: 1",
            f"Часовой пояс: 1",
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

        strings.append("test news")
        assert len(result) == len(strings)
