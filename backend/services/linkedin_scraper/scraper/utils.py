async def scroll_jobs_container(page, container_selector: str = "div.scaffold-layout__list", max_scrolls: int = 30):
    previous_height = 0

    for _ in range(max_scrolls):
        current_height = await page.evaluate(f"""
            () => {{
                const container = document.querySelector("{container_selector}");
                return container ? container.scrollHeight : 0;
            }}
        """)

        await page.evaluate(f"""
            () => {{
                const container = document.querySelector("{container_selector}");
                if (container) container.scrollBy(0, container.scrollHeight);
            }}
        """)

        await page.wait_for_timeout(1000)

        if current_height == previous_height:
            break 
        previous_height = current_height
        