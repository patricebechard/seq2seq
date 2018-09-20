import re
import json
import gzip
import unicodedata
import re
import pickle

# text corpuses
DATADIR = 'data/'
source = 'europarl-v7.fr-en.en'
target = 'europarl-v7.fr-en.fr'

# lookup dictionaries to map indices to words
ix2word_source_file = DATADIR + 'ix2word_en.json'
word2ix_source_file = DATADIR + 'word2ix_en.json'
ix2word_target_file = DATADIR + 'ix2word_fr.json'
word2ix_target_file = DATADIR + 'word2ix_fr.json'

ix2word_source = {'0': 'UNK', '1': '<BOS>', '2': '<EOS>', '3': '<PAD>'}
word2ix_source = {'UNK': '0', '<BOS>': '1', '<EOS>': '2', '<PAD>': '3'}
ix2word_target = {'0': 'UNK', '1': '<BOS>', '2': '<EOS>', '3': '<PAD>'}
word2ix_target = {'UNK': '0', '<BOS>': '1', '<EOS>': '2', '<PAD>': '3'}

# list containing source/target pairs
pairs_file = DATADIR + 'pairs_en_fr.json'
pairs = []

# filtering parameters
filtering = True

if filtering:
	min_word_occurence = 10
	max_seq_length = 30
	word_freq_source = {}
	word_freq_target = {}

	# filtered versions of file names
	ix2word_source_file = DATADIR + 'ix2word_en_filtered.json'
	word2ix_source_file = DATADIR + 'word2ix_en_filtered.json'
	ix2word_target_file = DATADIR + 'ix2word_fr_filtered.json'
	word2ix_target_file = DATADIR + 'word2ix_fr_filtered.json'

	pairs_file = DATADIR + 'pairs_en_fr_filtered.json'


def normalize_sentence(s):
	"""
	Normalizing the string by converting to ascii, converting to lower, deleting symbols
	Preprocessing taken from the pytorch seq2seq tutorial for machine translation
	http://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
	"""
	s = s.decode('utf-8')
	s = s.lower().strip()
	s = ''.join(c for c in unicodedata.normalize('NFD', s) 
				if unicodedata.category(c) != 'Mn')
	s = re.sub(r"([.!?])", r" \1", s)
	s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
	return s

def preprocess_data():

	# source language
	print("Processing source language...")

	with open(DATADIR + source, 'rb') as f:

		if filtering:
			#1st pass for word frequency
			for sentence in f:
				sentence = normalize_sentence(sentence)

				sentence = sentence.split()

				for word in sentence:
					if word in word_freq_source:
						word_freq_source[word] += 1
					else:
						word_freq_source[word] = 1

	with open(DATADIR + source, 'rb') as f:

		lookup_length = len(ix2word_source)
		#2nd pass for lookup dictionaries
		for sentence in f:
			sentence = normalize_sentence(sentence)

			# splitting into words
			sentence = sentence.split()

			# adding words to lookup dict
			for i in range(len(sentence)):

				#replace word by <UNK> if appears less than min_word_occurence times
				if filtering:
					if word_freq_source[sentence[i]] < min_word_occurence:
						sentence[i] = "<UNK>"

				if sentence[i] not in word2ix_source:
					word2ix_source[sentence[i]] = lookup_length
					ix2word_source[str(lookup_length)] = sentence[i]
					lookup_length += 1

			# convert sentence to list of word indices
			sentence = [word2ix_source[word] for word in sentence]

			#adding to pairs 
			pairs.append({})
			pairs[-1]['source'] = sentence

	# target language
	print("Processing target language...")

	with open(DATADIR + target, 'rb') as f:

		if filtering:
			#1st pass for word frequency
			for sentence in f:
				sentence = normalize_sentence(sentence)

				sentence = sentence.split()

				for word in sentence:
					if word in word_freq_target:
						word_freq_target[word] += 1
					else:
						word_freq_target[word] = 1

	with open(DATADIR + target, 'rb') as f:

		lookup_length = len(ix2word_target)
		j = 0

		#2nd pass for lookup dictionaries
		for sentence in f:
			sentence = normalize_sentence(sentence)

			# splitting into words
			sentence = sentence.split()

			# adding words to lookup dict
			for i in range(len(sentence)):

				#replace word by <UNK> if appears less than min_word_occurence times
				if filtering:
					if word_freq_target[sentence[i]] < min_word_occurence:
						sentence[i] = "<UNK>"

				if sentence[i] not in word2ix_target:
					word2ix_target[sentence[i]] = lookup_length
					ix2word_target[str(lookup_length)] = sentence[i]
					lookup_length += 1

			# convert sentence to list of word indices
			sentence = [word2ix_target[word] for word in sentence]

			#adding to pairs 
			pairs[j]['target'] = sentence
			j += 1

	if filtering:
		new_pairs = []

		for pair in pairs:
			if len(pair['source']) <= max_seq_length and len(pair['target']) <= max_seq_length:
				new_pairs.append(pair)

	# save lookup dictionaries
	with open(ix2word_source_file, 'w') as f:
		json.dump(ix2word_source, f)
	with open(word2ix_source_file, 'w') as f:
		json.dump(word2ix_source, f)
	with open(ix2word_target_file, 'w') as f:
		json.dump(ix2word_target, f)
	with open(word2ix_target_file, 'w') as f:
		json.dump(word2ix_target, f)

	# save pairs 
	with open(pairs_file, 'w') as f:
		json.dump(new_pairs, f)

if __name__ == "__main__":

	preprocess_data()