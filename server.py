"""Enviar e Receber Mensagens Criptografadas"""

from random import sample
from json import dumps
from datetime import datetime
from secrets import ALPHABET, AUTH_TOKEN, ACCOUNT_SID, MY_PHONE_NUMBER, MY_TWILIO_PHONE
from twilio.rest import Client

class Messages(object):
	"""docstring for Messages"""
	def __init__(self):
		super(Messages, self).__init__()
		self.numbers = list(range(25, 99))
		self.alphabet = ALPHABET # codificacao de alfabeto a criterio do desenvolvedor
		self.AUTH_TOKEN = AUTH_TOKEN
		self.ACCOUNT_SID = ACCOUNT_SID
		self.MY_PHONE_NUMBER = MY_PHONE_NUMBER
		self.MY_TWILIO_PHONE = MY_TWILIO_PHONE

	def connect_twilio(self, body):

		client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)

		message = client.messages.create(
			body = body,
			from_ = self.MY_TWILIO_PHONE,
			to = self.MY_PHONE_NUMBER
		)

		return message.sid

	def send_message_crypto(self, text: str):

		if len(text) > 180:

			return {'message': 'Excede o número de caracteres'}

		token = sample(self.numbers, 2)

		token = int(''.join([str(i) for i in token]))

		error = sample(self.numbers, 1)[0]

		full_text = []

		for word in text.lower():

			try:

				word = ''.join([str(self.alphabet.get(i)*token*error) for i in word][0])

				full_text.append(word)

			except TypeError:

				print('Caractere é um número ou acentuação, portanto será removido.')

		data = {
			'token': str(token) + str(error),
			'timestamp': int(datetime.now().timestamp()),
			'message': ' '.join(full_text)
		}

		return self.connect_twilio(body = dumps(data, indent = 2))

	def receive_message_crypto(self, data: dict):

		text = data['message'].split(' ')

		token = data['token'][0:4]

		error = data['token'][-2:]

		print(token, error)

		reversed_alphabet = dict(map(reversed, self.alphabet.items()))

		text = ''.join([reversed_alphabet.get(int(i)/int(token)/int(error)) for i in text])

		return text

if __name__ == '__main__':

	x = Messages()

	message = str(input('Mensagem: '))

	y = x.send_message_crypto(message)

	print(y)
