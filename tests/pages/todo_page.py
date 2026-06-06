from playwright.async_api import Page, expect

class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.input = page.locator("input.task-input")
        self.add_button = page.locator("button.add-button")
        
        self.filters = {
            "all": page.get_by_text("All", exact=True),
            "active": page.get_by_text("Active", exact=True),
            "completed": page.get_by_text("Completed", exact=True)
        }
        
        self.task_items = page.locator(".task-item")
        self.task_titles = page.locator(".task-title")
        self.checkboxes = page.locator(".task-checkbox")
        self.edit_buttons = page.locator(".edit-button")
        self.delete_buttons = page.locator(".delete-button")

    async def add_task(self, text: str):
        await self.input.fill(text)
        await self.add_button.click()
        await self.page.wait_for_timeout(2000)

    async def ensure_tasks_exist(self, min_count: int = 3):
        current = await self.get_tasks_count()
        needed = min_count - current
        if needed <= 0:
            return
        print(f"🔄 Создаём {needed} тестовых задач...")
        for i in range(needed):
            await self.add_task(f"AutoTest Task {i+1}")
        await self.page.wait_for_timeout(1000)

    async def get_tasks_count(self) -> int:
        await self.page.wait_for_timeout(800)
        return await self.task_items.count()

    async def toggle_task(self, index: int = 0):
        checkbox = self.checkboxes.nth(index)
        await expect(checkbox).to_be_visible(timeout=15000)
        await checkbox.click()
        await self.page.wait_for_timeout(1200)

    async def edit_task(self, index: int, new_text: str):
        edit_btn = self.edit_buttons.nth(index)
        await expect(edit_btn).to_be_visible(timeout=15000)
        await edit_btn.click()
        edit_input = self.page.locator(".edit-input").nth(index)
        await expect(edit_input).to_be_visible(timeout=10000)
        await edit_input.fill(new_text)
        await self.page.keyboard.press("Enter")
        await self.page.wait_for_timeout(1500)

    async def delete_task(self, index: int = 0):
        delete_btn = self.delete_buttons.nth(index)
        await expect(delete_btn).to_be_visible(timeout=15000)
        await delete_btn.click()
        await self.page.wait_for_timeout(1500)

    async def filter_by(self, name: str):
        await expect(self.filters[name]).to_be_visible(timeout=10000)
        await self.filters[name].click()
        await self.page.wait_for_timeout(1000)

    async def get_task_text(self, index: int) -> str:
        return await self.task_titles.nth(index).inner_text()

    async def is_task_completed(self, index: int) -> bool:
        cls = await self.task_titles.nth(index).get_attribute("class") or ""
        return "completed" in cls.lower()