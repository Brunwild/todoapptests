import pytest
import allure
from pages.todo_page import TodoPage


@allure.feature("Todo Application")
@allure.story("Основной функционал")
class TestTodoFunctionality:

    @allure.title("TC-01: Добавление новой задачи")
    @allure.description("Пользователь может добавить новую задачу")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "positive")
    @pytest.mark.asyncio
    async def test_add_new_task(self, page):
        todo = TodoPage(page)
        await todo.ensure_tasks_exist(1)
        count_before = await todo.get_tasks_count()
        await todo.add_task("Купить молоко")
        count_after = await todo.get_tasks_count()
        assert count_after > count_before

    @allure.title("TC-02: Отметка задачи как выполненной")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive")
    @pytest.mark.asyncio
    async def test_mark_as_completed(self, page):
        todo = TodoPage(page)
        await todo.ensure_tasks_exist(1)
        await todo.toggle_task(0)
        assert await todo.is_task_completed(0)

    @allure.title("TC-03: Редактирование задачи")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive")
    @pytest.mark.asyncio
    async def test_edit_task(self, page):
        todo = TodoPage(page)
        await todo.ensure_tasks_exist(1)
        await todo.edit_task(0, "Отредактировано Playwright")
        assert "Отредактировано Playwright" in await todo.get_task_text(0)

    @allure.title("TC-04: Удаление задачи")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive")
    @pytest.mark.asyncio
    async def test_delete_task(self, page):
        todo = TodoPage(page)
        await todo.ensure_tasks_exist(2)
        count_before = await todo.get_tasks_count()
        await todo.delete_task(0)
        count_after = await todo.get_tasks_count()
        assert count_after < count_before

    @allure.title("TC-05: Фильтрация Active")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("positive")
    @pytest.mark.asyncio
    async def test_active_filter(self, page):
        todo = TodoPage(page)
        await todo.filter_by("active")