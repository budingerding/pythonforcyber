##usage replace the "https://example.com" with the URL you want to scrape.

import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
	try:
		# Send an HTTP GET request to the URL
		response = requests.get(url)
		response.raise_for_status() # Raise an HTTPError for bad response

		# Parse the HTML content of the page
		soup = BeautifulSoup(response.text, 'html.parser')

		# Example: Extract all headings (h1, h2, h3, etc.)
		headings = {f'h{i}': [tag.text.strip() for tag in soup.find_all(f'h{i}')] for i in range(1, 7)}

		# Example: Extract all links (anchor tags with href)
		links = [a['href'] for a in soup.find_all('a', href=True)]

		# Example: Extract all paragraphs
		paragraphs = [p.text.strip() for p in soup.find_all('p')]

		return {
			"headings": headings,
			"links": links,
			"paragraphs": paragraphs,
		}

	except requests.exceptions.RequestException as e:
		print(f"Error fetching {url}: {e}")
		return None

if __name__ == "__main__":
	# URL to scrape
	url = "https://example.com"

	# Call the scrape_wabpage function
	scraped_data = scrape_webpage(url)

	if scraped_data:
		print("Headings:")
		for heading, texts in scraped_data['headings'].items():
			print(f" {heading}: {texts}")

		print("\nLinks:")
		for link in scraped_data['links']:
			print(f" {link}")

		print("\nParagraphs:")
		for paragraph in scraped_data['paragraphs']:
			print(f" {paragraph}")