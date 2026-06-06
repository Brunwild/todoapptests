import pytest
import allure
from pages.todo_page import TodoPage


@allure.feature("Todo Application")
@allure.story("Edge Cases & Negative")
class TestEdgeCases:

    @allure.title("TC-06: Добавление пустой задачи")
    @allure.description("Проверка валидации пустой задачи (Баг-репорт №1)")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("negative")
    @pytest.mark.asyncio
    async def test_empty_task_not_added(self, page):
        todo = TodoPage(page)
        count_before = await todo.get_tasks_count()
        await todo.input.fill("")
        await todo.add_button.click()
        await page.wait_for_timeout(1000)
        assert await todo.get_tasks_count() == count_before

    @allure.title("TC-07: Добавление очень длинного текста")
    @allure.description("Проверка обработки длинного текста (Баг-репорт №2)")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("boundary")
    @pytest.mark.asyncio
    async def test_long_text(self, page):
        todo = TodoPage(page)
        long_text = "A" * 500
        await todo.add_task(long_text)
        count_after = await todo.get_tasks_count()
        assert count_after > 0, "Длинная задача не добавилась"