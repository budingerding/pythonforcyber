import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def is_potential_phishing_site(url):
	try:
		# Send an HTTP GET request to the URL
		response = requests.get(url, timeout=10)
		response.raise_for_status()

		# Parse the HTML content
		soup = BeautifulSoup(response.text, 'html.parser')

		# Extract the domain of the URL
		domain = urlparse(url).netloc

		# Check for input fields that could be used for credentials
		input_fields = soup.find_all('input')
		credential_fields = [field for field in input_fields if field.get('type') in ('password', 'email', 'text')]

		# Check for suspicious keywords in the page text or forms
		suspicious_keywords = ['login', 'verify', 'password', 'account', 'secure', 'update']
		page_text = soup.get_text(" ").lower()
		found_keywords = [keyword for keyword in suspicious_keywords if keyword in page_text]

		# Check for links to external domains
		external_links = []
		for a_tag in soup.find_all('a', href=True):
			href = a_tag['href']
			link_domain = urlparse(urljoin(url,href)).netloc
			if link_domain and link_domain != domain:
				external_links.append(href)

		# Check for embedded scripts that load external resources
		suspicious_scripts = []
		for script_tag in soup.find_all('script', src=True):
			script_src = urljoin(url, script_tag['src'])
			if urlparse(script_src).netloc != domain:
				suspicious_scripts.append(script_src)

		# Check if the URL contains phishing indicators
		phishing_indicators = []
		if any(char.isdigit() for char in domain.split('.')):
			phishing_indicators.append("IP-based domain")
		if '-' in domain:
			phishing_indicators.append("Hyphenated domain")

		# Compile results
		results = {
		"credential_fields": len(credential_fields),
		"suspicious_keywords": found_keywords,
		"external_links": external_links,
		"suspicious_scripts": suspicious_scripts,
		"phishing_indicators": phishing_indicators,
		}

		return results

	except requests.exceptions.RequestException as e:
		print(f"Error check {url}: {e}")
		return None

if __name__ == "__main__":
	# URL to analyze
	url = "https://auth-yweb.github.io/newone"

	# Analyze the site
	analysis = is_potential_phishing_site(url)

	if analysis:
		print("Potential Phishing Indicators:")
		print(f"  Credential Input Fields: {analysis['credential_fields']}")
		print(f"  Suspicious Keywords: {', '.join(analysis['suspicious_keywords'])}")
		print(f"  External Links: {len(analysis['external_links'])}")
		for link in analysis['external_links']:
			print(f"  {link}")
		print(f"  Suspicious Scripts: {len(analysis['suspicious_scripts'])}")
		for script in analysis['suspicious_scripts']:
			print(f"  {script}")
		print(f"  Phishing Indicators: {', '.join(analysis['phishing_indicators'])}")