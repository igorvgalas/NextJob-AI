import json
import os
from playwright.async_api import async_playwright
from config import EMAIL, PASSWORD
from .utils import scroll_jobs_container


async def scrape_linkedin_jobs(search_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(search_url)
        print(f"[*] Navigated to {search_url}")
        await page.click('#base-contextual-sign-in-modal > div > section > div > div > div > div.sign-in-modal > button')

        # Wait for the login form to appear
        await page.wait_for_selector('#base-sign-in-modal > div > section > div > div > h2', timeout=10000)

        # Fill in the login form
        await page.fill('#base-sign-in-modal_session_key', EMAIL)
        await page.fill('#base-sign-in-modal_session_password', PASSWORD)
        await page.click('#base-sign-in-modal > div > section > div > div > form > div.flex.justify-between.sign-in-form__footer--full-width > button')

        await page.wait_for_timeout(8000)
        await page.wait_for_selector("div[data-job-id]", timeout=10000)
        await scroll_jobs_container(page, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div")
        job_elements = await page.query_selector_all('div[data-job-id]')

        job_data = []
        for job in job_elements:
            job_id = await job.get_attribute("data-job-id")

            # Job title
            title_el = await job.query_selector("a.job-card-container__link")
            job_title = await title_el.inner_text() if title_el else ""

            # Apply link
            apply_href = await title_el.get_attribute("href") if title_el else ""
            apply_link = f"https://www.linkedin.com{apply_href}" if apply_href else ""

            # Company name
            company_el = await job.query_selector(".artdeco-entity-lockup__subtitle span")
            company_name = await company_el.inner_text() if company_el else ""

            # Location
            location_el = await job.query_selector("li.job-card-container__metadata-wrapper li span")
            location = await location_el.inner_text() if location_el else ""

            job_data.append({
                "job_id": job_id,
                "job_title": job_title.strip(),
                "company_name": company_name.strip(),
                "location": location.strip(),
                "apply_link": apply_link.strip()
            })

        # Save results
        os.makedirs("output", exist_ok=True)
        with open("output/jobs.json", "w", encoding="utf-8") as f:
            json.dump(job_data, f, indent=2)

        print(f"Saved {len(job_data)} jobs to output/jobs.json")
        await browser.close()
