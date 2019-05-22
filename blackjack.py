"""
Black Jack Card Game
Garrett Sloup
11/09/2018
Built and developed in conjunction with Complete Python Bootcamp: Go from zero to hero in Python 3

NOTE:
*Areas for improvement*
	1) make chips a global variable to keep running tab of chips between hands/games
	2) add more basic functionality to the game(e.g. split, double down, display total hand value to player, pay blackjacks 3/2)
	3) add more complex functionality (e.g. insurance option if dealer's card shows an ace, basic strategy hints based off current cards)
	4) basic GUI for improving ease of use-- display card pictures, and use buttons in lieu of having player type answers.
"""
import random

# Global Variables for card data
suits = ('Spades','Diamonds', 'Clubs', 'Hearts')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 
		'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Will be used as a default global variable to be broken out of the game's while-loop
playing = True


##############################################################################
# CLASSES 

class Card():
	"""Used to generate all card suits and ranks in the deck via a nested for-loop when the Deck class is ran """
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	def __str__(self):
		return self.rank + " of " + self.suit

class Deck():
	""" Generates a full deck of cards(excluding Jokers) that can be shuffled and dealt a card off the top """
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))
	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + card.__str__()
		return "The deck has: " + deck_comp
	def shuffle(self):
		random.shuffle(self.deck)
	def deal(self):
		single_card = self.deck.pop()
		return single_card

class Hand():
	""" Instance of a hand will be generated for both the player and dealer, 
	that can have cards added (when hit) and also take the value of aces into account"""
	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0
	
	def add_card(self,card):
		# This card is passed in from Deck.deal() --> single Card(suit,rank)
		self.cards.append(card)

		# Sums total value from global values dictionary and uses rank as the key
		self.value += values[card.rank]

		# Tracks if aces are available incase the value exceeds 21 and the ace can go from 11 -> 1
		if card.rank == "Ace":
			self.aces += 1

	def adjust_for_ace(self):
		#if total value > 21 and I still have an ace available, then change my ace to be a 1 instead of 11.
		while self.value > 21 and self.aces > 0:
			self.value -= 10
			self.aces -= 1

class Chips():
	""" Player will be given 100 chips unless otherwise specified and will add/subtract chips based off the 
	amount bet and whether the hand was won"""
	def __init__(self, total= 100):
		self.total = total
		self.bet = 0
	def win_bet(self):
		self.total += self.bet
	def lose_bet(self):
		self.total -= self.bet

###################################################################################################
# FUNCTIONS

def take_bet(chips):
	"""Will prompt player to bet a certain number of chips between 1 and their total chip count."""

	while True:
		try:
			chips.bet = int(input("How many chips would you like to bet?"))
		except:
			print("Sorry, please enter a number!")

		#This corrects for bets exceeding chip total or negative bets
		if chips.bet > chips.total or chips.bet <= 0:
			print("Please enter a number between 1 and {}".format(chips.total))
		else:
			break

def hit(deck,hand):
	""" Function will add a card to player's hand and adjust for any possible aces."""
	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def hit_or_stand(deck,hand):
	""" Function prompts player to "hit" or "stand". """
	global playing  # Global variable to later break out of while-loop

	while True:
		x = input('Hit or stand? Enter h or s ')

		if x[0].lower() == 'h':
			hit(deck,hand)
		elif x[0].lower() == 's':
			print('Player Stands, Dealer\'s Turn')
			playing = False # will stop the while loop once the 'break' is reached
		else:
			print("Sorry, I didn't understand your answer. Please enter h or s only!")
			continue  # will restart the while loop
		break

def show_some(player,dealer):
	""" When called, this function will show one of the dealer's cards (2nd) and all of the player's cards. """
	print("-----------------------------")
	print("DEALER'S HAND:")
	print("One card is hidden!")
	print(dealer.cards[1])
	print('\n')
	print("PLAYER'S HAND:")
	for card in player.cards:
		print(card)
        
def show_all(player,dealer):
	""" When called, this function will show all of the dealer's and player's cards. """
	print("-----------------------------")
	print("DEALER'S HAND:")
	for card in dealer.cards:
		print(card)
	print('\n')
	print("PLAYER'S HAND:")
	for card in player.cards:
		print(card)

# DIFFERENT END OF GAME SCENARIOS

def player_busts(player,dealer,chips):
	print("Player Busts!")
	chips.lose_bet()

def player_wins(player,dealer,chips):
	print("Player Wins!")
	chips.win_bet()

def dealer_busts(player,dealer,chips):
	print("Dealer Busts!")
	chips.win_bet()

def dealer_wins(player,dealer,chips):
	print("Dealer Wins!")
	chips.lose_bet()

def push(player,dealer):
	""" 'chips' isn't a necessary argument since no chips are won or lost """
	print("Dealer and Player Tie-- Push!")

#################################################################################
# Black Jack Game Logic

while True:  # The game set up resides in while-loop.  Will 'break' to end the program.
	# Opening statement
	print("Welcome to Blackjack")

	# Create a deck object and shuffle the cards
	deck = Deck()
	deck.shuffle()

	# Create a hand object for player and dealer, then deals them each 2 cards
	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	# Sets up player's chips
	player_chips = Chips() # Can add an int argument to specify num of chips other than 100

	# Prompts player to bet before cards are seen
	take_bet(player_chips)
	print('\n')

	# Show all player cards and one dealer card
	show_some(player_hand, dealer_hand)

	while playing: # Global variable defined in hit_or_stand()
		# Prompt player to hit or stand. If player stands, 'playing' = False.
		hit_or_stand(deck, player_hand)

		# Reveals the newley dealt card to player or redisplays the same cards if player stands.
		show_some(player_hand, dealer_hand)

		# If player's hand > 21, player busts
		if player_hand.value > 21:
			player_busts(player_hand, dealer_hand, player_chips)
			break # will break current while loop to start a new hand

	# If player doesn't bust, Dealer will hit until >= 17.
	if player_hand.value <= 21:
		while dealer_hand.value < 17:
			hit(deck, dealer_hand)

		# Shows both the player's and dealer's full hands.
		show_all(player_hand, dealer_hand)

		# Different winning scenarios. Will reward or keep player chips.
		if dealer_hand.value > 21:
			dealer_busts(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value > player_hand.value:
			dealer_wins(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value < player_hand.value:
			player_wins(player_hand, dealer_hand, player_chips)
		else:
			push(player_hand, dealer_hand)

	# Display the player's current chip count
	print('\n Player\'s total chips are at: {}'.format(player_chips.total))

	# Ask the player to play again
	while True:
		x = input("Would you like to play again? y/n \n")
		if x[0].lower() == 'y':
			playing = True
			break # will break out of current while-loop and start back at the first while-loop
		elif x[0].lower() == 'n':
			print("Thanks for playing!")
			playing = False
			break # Will break out of the current while-loop.
		else:
			print("Sorry, please type 'y' to play again or 'n' to stop playing.")
			continue # Will go back to top of current while loop to get a correct response

	# Will break out of the game's while-loop to end the entire program
	if playing == False:
		break

