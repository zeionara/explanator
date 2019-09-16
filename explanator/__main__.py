import json, sys, functools

DICT_FILE = "dictionary.json"
INPUT_FILE = "words.txt"
OUTPUT_FILE = "definitions.txt"
DEFINITIONS_SEPARATOR = " is like "
ORDER_FLAG = "-o"

def handle_file_error(func):
	@functools.wraps(func)
	def print_file_error(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except FileNotFoundError:
			print("No such file")
	return print_file_error

@handle_file_error
def read_dictionary(filename):
	with open(filename, "r") as f:
		return json.load(f)

def get_synonyms(word, dictionary):
	return set([synonym.strip().lower() for synonym in dictionary.get(word.upper(), "").split(".")[0].split(";") if synonym != ''])

@handle_file_error
def read_words(filename):
	with open(filename, "r") as f:
		return set({word.replace('\n', '').lower() for word in f.readlines()})

def write_definitions(lookup_result, order=False):
	with open(OUTPUT_FILE, "w") as f:
		f.writelines([f"{word} {DEFINITIONS_SEPARATOR} {' or '.join([synonym for synonym in lookup_result[word]])}\n" for word in (lookup_result.keys() if not order else sorted(lookup_result.keys())) if len(lookup_result[word]) > 0])


if len(sys.argv) < 2 or len(sys.argv) == 2 and ORDER_FLAG in sys.argv:
	input_filename = INPUT_FILE
else:
	input_filename = sys.argv[1]

dictionary = read_dictionary(DICT_FILE)
write_definitions({word: get_synonyms(word, dictionary) for word in read_words(input_filename)}, ORDER_FLAG in sys.argv)