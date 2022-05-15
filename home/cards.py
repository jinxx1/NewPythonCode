import collections

Card = collections.namedtuple('card', ['rank', 'suit'])


class FrenchDeck:
	ranks = [str(n) for n in range(2, 11)] + list('JQKA')
	suits = ['spades', 'diamonds', 'clubs', 'hearts']
	# joke_B = 'joke_B'
	# joke_s = 'joke_s'


	def __init__(self):
		self._cards = [Card(rank=rank, suit=suit)
		               for rank in self.ranks
		               for suit in self.suits]

	def __len__(self):
		return len(self._cards)

	def __getitem__(self, position):
		return self._cards[position]


if __name__ == '__main__':
	beerCard = FrenchDeck()
	for i in beerCard:
		print(i)
	print(len(beerCard))
