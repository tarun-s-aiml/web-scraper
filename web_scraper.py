import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"

        print("\n===== WEBSITE INFORMATION =====")
        print("Title:", title)

        headings = soup.find_all(["h1", "h2", "h3"])

        print("\n===== HEADINGS =====")

        if headings:
            for index, heading in enumerate(headings[:20], start=1):
                text = heading.get_text(" ", strip=True)

                if text:
                    print(f"{index}. {text}")
        else:
            print("No headings found.")

        links = soup.find_all("a", href=True)

        print("\n===== LINKS =====")

        for index, link in enumerate(links[:20], start=1):
            text = link.get_text(" ", strip=True)
            href = urljoin(url, link["href"])

            print(f"{index}. {text or 'No text'}")
            print("   ", href)

    except requests.exceptions.RequestException as error:
        print("Error accessing website:", error)


print("===== SIMPLE WEB SCRAPER =====")

url = input("Enter website URL: ").strip()

if not url.startswith(("http://", "https://")):
    url = "https://" + url

scrape_website(url)
