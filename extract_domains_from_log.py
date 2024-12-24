import re
import sys

def extract_domains_from_log(file_path):
	"""
	Extract all domain names from a given log file.

	:param file_path: Path to the log file
	:return: A set of domain names
	"""

	# Define a regex pattern to match domain names
	domain_pattern = re.compile(
		r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}\b'
	)

	domains = set()

	try:
		with open(file_path, 'r') as log_file:
			for line in log_file:
				# Find all domain names in the line
				matches = domain_pattern.findall(line)
				if matches:
					domains.update(matches)
	except FileNotFoundError:
		print(f"Error: File not found: {file_path}")
	except Exception as e:
		print(f"Error: {e}")

	return domains

def main():
	if len(sys.argv) < 2:
		print("Usage: extract_domains.py -f filepath")
		sys.exit(1)

	file_path = sys.argv[2]
	extracted_domains = extract_domains_from_log(file_path)

	if extracted_domains:
		print("Extracted domain names:")
		for domain in sorted(extracted_domains):
			print(domain)
	else:
		print("No domain names found in the log")

if __name__ == "__main__":
	main()
