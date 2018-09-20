import torch
from torch import nn
import torch.nn.functional as F
from torch import optim
from torch.autograd import Variable

import json
import matplotlib.pyplot as plt
from random import shuffle
import itertools

from seq2seq import Seq2Seq

use_cuda = torch.cuda.is_available()

batch_size = 64


DATADIR = 'data/'

# saved model names
saved_model = 'seq2seq_saved.pt'

#load dataset
pairs_file = 'pairs_en_fr.json'
with open(pairs_file) as f:
	pairs = json.load(f)
shuffle(pairs)

def generate_pairs_batch():







def train(model, n_updates = 10000, print_every=100, learning_rate=learning_rate):

	if use_cuda:
		model = model.cuda()

	criterion = nn.CrossEntropyLoss()
	optimizer = optim.Adam(model.parameters(), lr=learning_rate, momentum)

	for update in range(n_updates):

		
		inputs, targets = generate_pairs_batch()

		inputs, targets = Variable(inputs), Variable(targets)
		if use_cuda:
			inputs, targets = inputs.cuda(), targets.cuda()


def show_attention():
	pass

if __name__ == "__main__":

	model = Seq2Seq()

	#loading saved model
	model.load_state_dict(torch.load(saved_model))

	train(model)