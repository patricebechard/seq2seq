import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable

class Seq2Seq(nn.Module):

	def __init__(self, input_size, output_size, embedding_size=256, hidden_size=256, 
				 num_layers=3, bidirectional=False, attention=False, rnn_type='gru'):

		self.encoder = Encoder(input_size=input_size, embedding_size=embedding_size,
							   hidden_size=hidden_size, num_layers=num_layers,
							   bidirectional=bidirectional, encoder_type=rnn_type)
		self.decoder = Decoder(embedding_size=embedding_size, hidden_size=hidden_size,
							   output_size=output_size, attention=attention,
							   decoder_type=rnn_type)

	def forward(self, inputs, targets=None, teacher_forcing=False):

		# hidden at t=0 is a learned bias parameter
		self.encoder.hidden = self._init_hidden()

		for word in inputs:
			out = self.encoder(word)

		self.decoder.hidden = self.encoder.hidden

		if teacher_forcing:
			# we feed target to decoder

			if targets is None:
				raise Exception("Has to feed target to model when using teacher forcing")

			for word in targets:
				out = self.encoder(word)

		else:

			# feeding bos as first input and feeding previous outputs as inputs after

			




		return x

class Encoder(nn.Module):

	def __init__(self, input_size, embedding_size, hidden_size, num_layers,
				 bidirectional=False, encoder_type='gru'):
		"""
		Parameters
		----------
		input_size : int
			size of vocabulary for input sequence
		embedding_size : int
			size of embedding
		hidden_size : int
			size of hidden state and cell state (if applicable)
		num_layers : int
			number of hidden layers of encoder
		bidirectional : boolean
			whether or not the encoder is a bidirectional rnn or not
		encoder_type : string
			type of rnn used as encoder. Can take values in ['normal', 'lstm', 'gru']
		"""

		self.input_size = input_size
		self.embedding_size = embedding_size
		self.hidden_size = hidden_size
		self.num_layers = num_layers
		self.is_bidirectional = bidirectional
		self.encoder_type = encoder_type

		self.hidden0 = nn.Parameter(torch.randn(num_layers, 1, hidden_size) * 0.05)

		self.embedding = nn.Embedding(num_embedding=input_size,
			                          embedding_dim=embedding_size)

		self.encoder_rnn = nn.GRU(input_size=embedding_size,
			                       hidden_size=hidden_size,
			                       num_layers=num_layers,
			                       bidirectional=bidirectional)

	def forward(self, x):

		x = self.embedding(x)
		x, self.hidden = self.encoder_rnn(x, self.hidden)

		return x

	def _init_hidden(self):

		hidden = self.hidden0.clone().repeat(1, self.batch_size, 1)
		if use_cuda:
			hidden = hidden.cuda()

		return hidden

class Decoder(nn.Module):

	def __init__(self, embedding_size, hidden_size, output_size, num_layers, 
				 decoder_type='gru', attention=False):
		"""
		Parameters
		----------
		embedding_size : int
			size of embedding
		hidden_size : int
			size of hidden state and cell state (if applicable)
		num_layers : int
			number of hidden layers of decoder
		decoder_type : string
			type of rnn used as decoder. Can take values in ['normal', 'lstm', 'gru']
		"""

		self.embedding_size = embedding_size
		self.hidden_size = hidden_size
		self.output_size = output_size
		self.num_layers = num_layers
		self.decoder_type = decoder_type
		self.with_attention = attention

		self.embedding = nn.Embedding(num_embedding=output_size, 
									  embedding_dim=embedding_size)

		self.attention = nn.Linear(in_features=hidden_size, out_features=hidden_size)
		self.decoder_rnn = nn.LSTM(input_size=output_size,
			                       hidden_size=hidden_size,
			                       num_layers=num_layers)

		self.fc = nn.Linear(in_features=hidden_size, out_features=output_size)

	def forward(self, x):

		x = self.embedding(x)

		x, self.hidden = self.decoder_rnn(x, self.hidden)

		x = self.fc(x)
if __name__ == "__main__":

	model = Seq2Seq(input_size, )

	