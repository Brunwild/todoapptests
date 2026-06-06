import pytest
import allure
from playwright.async_api import async_playwright

@pytest.fixture(scope="function")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def page(browser):
    context = await browser.new_context(viewport={"width": 1366, "height": 900})
    page = await context.new_page()

    # Mocking API для стабильности
    async def handle_todos(route):
        if route.request.method == "POST":
            data = route.request.post_data_json or {}
            await route.fulfill(status=201, json={**data, "id": 999})
        elif route.request.method in ["PUT", "PATCH"]:
            data = route.request.post_data_json or {}
            await route.fulfill(status=200, json=data)
        elif route.request.method == "DELETE":
            await route.fulfill(status=200, json={})
        else:
            await route.continue_()

    await page.route("**/todos**", handle_todos)

    await page.goto("http://localhost:4200/", wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector("input.task-input", timeout=30000)

    try:
        await page.wait_for_selector(".task-item", timeout=15000)
    except:
        print("⚠️ Начальный список задач не загрузился")

    yield page
    await context.close()


# Allure — скриншот при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs.get("page")
            if page:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name="Скриншот ошибки",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception:
            pass