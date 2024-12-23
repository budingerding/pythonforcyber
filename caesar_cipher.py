import sys

def caesar_cipher(text, shift):
	"""Encrypts or decrypts text using the Caesar cipher."""

	result = ""
	for char in text:
		if char.isalpha():
			# Get the character's ASCII value
			char_code = ord(char)
			
			# Determine whether the character is uppercase or lowercase
			is_upper = char.isupper()

			# Shift the character code
			shifted_code = char_code + shift

			# Wrap around the alphabet if neccessary
			if is_upper:
				shifted_code = (shifted_code - ord('A')) % 26 + ord('A')
			else:
				shifted_code = (shifted_code - ord('a')) % 26 + ord('a')

			# Convert the shifted code back to character
			result += chr(shifted_code)

		else:
			# Keep non-alphabetic charaters as they are
			result += char

	return result



def main():
	if len(sys.argv) < 3:
		print("Usage: script.py <-e|-d> <text> <shift>")
		sys.exit(1)
	
	mode = sys.argv[1]
	text = sys.argv[2]
	shift = int(sys.argv[3])

	if mode == "-e":
		print("Encrypted text:", caesar_cipher(text, shift))
	elif mode == "-d":
		print("Decrypted text:", caesar_cipher(text, -shift))
	else:
		print("Something wrong with argument")
		sys.exit(1)


if __name__ == "__main__":
	main()

	