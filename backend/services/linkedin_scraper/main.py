import argparse
import urllib.parse
import asyncio
from scraper.jobs import scrape_linkedin_jobs

def build_search_url(keyword: str, location: str, removed: str) -> str:
    base_url = "https://www.linkedin.com/jobs/search/"
    query_params = {
        "keywords": keyword,
        "location": location,
        "trk": "public_jobs_jobs-search-bar_search-submit",
    }
    if removed:
        query_params["removed"] = removed
    return f"{base_url}?{urllib.parse.urlencode(query_params)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Job Scraper")
    parser.add_argument("--keyword", required=False, help="Job keyword (e.g. Python Developer)")
    parser.add_argument("--location", required=False, help="Job location (e.g. Leeds)")
    parser.add_argument("--removed", required=False, help="Removed jobs filter")

    args = parser.parse_args()
    search_url = build_search_url(args.keyword, args.location, args.removed)

    print(f"[*] Scraping jobs for '{args.keyword}' in '{args.location}'")
    asyncio.run(scrape_linkedin_jobs(search_url=search_url))
