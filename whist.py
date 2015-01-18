import itertools
import random
import copy
import operator
import colorama
import sys

########
#stage1:
#-------
#for good trump: play lowest card gauranteed to win?
#for bad trump: lowest card with >80% win chance?
#for non-trump: check odds of better card underneath?
#        minimize number of suits; maybe check bridge scoring?
#
#
#######
#stage2:
#--------
#if can trump, use lowest trump
#if opponent goes first, use lowest winning card
#





colorama.init()


def printHandPretty(hand):
    hand = sorted(hand, key=operator.itemgetter(1,0))
    csuit = 'b'
    for card in hand:
        if card[1] != csuit:
            csuit = card[1]
            if csuit == 'D' or csuit == 'H':
                sys.stdout.write( '\n'+colorama.Fore.RED)
            else:
                sys.stdout.write('\n'+colorama.Style.RESET_ALL)
        face = card[0]
        if face == 11:
            face = 'J'
        elif face == 12:
            face = 'Q'
        elif face == 13:
            face = 'K'
        elif face == 14:
            face = 'A'
        elif face ==10:
            face = 'T'
        suit = '_'
        if card[1] =='D':
            suit = unichr(9830).encode('utf-8')
        if card[1] == 'C':
            suit = unichr(9827).encode('utf-8')
        if card[1] == 'S':
            suit = unichr(9824).encode('utf-8')
        if card[1] == 'H':
            suit = unichr(9829).encode('utf-8')
        sys.stdout.write(str(face)+suit+',')
    print colorama.Style.RESET_ALL
    

full_deck = list(itertools.product([2,3,4,5,6,7,8,9,10,11,12,13,14], ['S','C', 'D', 'H']))
deck = copy.deepcopy(full_deck)
possible_opponent_cards = copy.deepcopy(full_deck)
definite_opponent_cards = []
#cards probably still in the deck are (possible_opp_cards - definite_opp_cards)


#might also want to keep track of what opponent definitely has


opponentDifficulty  = raw_input("Hard or easy ai?")
hard = opponentDifficulty.lower() == 'hard'
print hard



#print deck

random.shuffle(deck)
player_hand = []
computer_hand = []
for i in range(13):
    player_hand.append(deck.pop())
    compcard = deck.pop()
    computer_hand.append(compcard)
    possible_opponent_cards.remove(compcard)
    
trumpSuit = deck[0][1]
usuit = '_'
if trumpSuit =='D':
    usuit = unichr(9830).encode('utf-8')
if trumpSuit == 'C':
    usuit = unichr(9827).encode('utf-8')
if trumpSuit == 'S':
    usuit = unichr(9824).encode('utf-8')
if trumpSuit == 'H':
    usuit = unichr(9829).encode('utf-8')

print "TRUMP: " +usuit



#printHandPretty(player_hand)
playerturn = True

playerpoints = 0
comppoints = 0

while len(deck)>0 or comppoints+playerpoints<13 :
    firsthalf = len(deck)>0
    print "\n\n\n\nTRUMP: " +usuit
    print "YOUR HAND:"
    printHandPretty(player_hand)
    if len(deck)>0:
        print "ON DECK:"
        printHandPretty([deck[0]])
    if playerturn:
        toplay = ('a','a')
        while True:
            userentered = raw_input("what card would you like to play?")
            userentered = userentered.upper()
            if len(userentered) == 2:
                value = userentered[0]
                suit = userentered[1]
                if value == 'T':
                    value = 10
                elif value == 'J':
                    value = 11
                elif value == 'Q':
                    value = 12
                elif value == 'K':
                    value = 13
                elif value == 'A':
                    value = 14
                value = int(value)
                if (value, suit) in player_hand:
                    toplay = (value, suit)
                    break
            print "invalid input"
        responseplay = ('a','a')
        if not hard:
            foundlegit = False
            for card in computer_hand:
                if card[1]==toplay[1]:
                    responseplay = card
                    foundlegit = True
                    break
            if not foundlegit:
                responseplay = computer_hand[0]
            print "Computer Chooses:"
            printHandPretty([responseplay])
        else:
            print "TODO"
            exit
        playerwin = True
        if responseplay[1] == toplay[1]:
            if toplay[0] < responseplay[0]:
                playerwin = False
        elif responseplay[1] == trumpSuit:
            playerwin = False
        
        player_hand.remove(toplay)
        if toplay in definite_opponent_cards:
            definite_opponent_cards.remove(toplay)

        if firsthalf:
            top_card = deck.pop(0)
        possible_opponent_cards.remove(toplay)
        computer_hand.remove(responseplay)
        if firsthalf:
            next_card = deck.pop(0)
        if playerwin:
            print "PLAYER WIN"
            if firsthalf:
                definite_opponent_cards.append(top_card)
                player_hand.append(top_card)
                computer_hand.append(next_card)
                possible_opponent_cards.remove(next_card)
            else:
                playerpoints+=1
            playerturn = True
        else:
            print "COMPUTER WIN"
            if firsthalf:
                print "YOU PICKED UP:"
                printHandPretty([next_card])
                player_hand.append(next_card)
                computer_hand.append(top_card)
                possible_opponent_cards.remove(top_card)
            else:
                comppoints+=1
            playerturn = False
    else: #computer goes first
        if hard:
            print "TODO"
            exit
        else:
            toplay = computer_hand[0]
            print "COMPUTER PLAYED:"
            printHandPretty([toplay])
            while True:
                userentered = raw_input("what card would you like to play?")
                userentered = userentered.upper()
                if len(userentered) == 2:
                    value = userentered[0]
                    suit = userentered[1]
                    if value == 'T':
                        value = 10
                    elif value == 'J':
                        value = 11
                    elif value == 'Q':
                        value = 12
                    elif value == 'K':
                        value = 13
                    elif value == 'A':
                        value = 14
                    value = int(value)
                    if (value, suit) in player_hand:
                        if suit == toplay[1] or not any(x[1] == toplay[1] for x in player_hand):
                            responseplay = (value, suit)
                            break
                print "invalid input"
        #begin cp
        playerwin = False
        if responseplay[1] == toplay[1]:
            if toplay[0] < responseplay[0]:
                playerwin = True
        elif responseplay[1] == trumpSuit:
            playerwin = True

        player_hand.remove(responseplay)
        if responseplay in definite_opponent_cards:
            definite_opponent_cards.remove(responseplay)



        if firsthalf:
            top_card = deck.pop(0)
            next_card = deck.pop(0)
        possible_opponent_cards.remove(responseplay)
        computer_hand.remove(toplay)
        
        if playerwin:
            print "PLAYER WIN"
            if firsthalf:
                definite_opponent_cards.append(top_card)
                player_hand.append(top_card)
                computer_hand.append(next_card)
                possible_opponent_cards.remove(next_card)
            else:
                playerpoints+=1
            playerturn = True
        else:
            print "COMPUTER WIN"
            if firsthalf:
                print "YOU PICKED UP:"
                printHandPretty([next_card])
                player_hand.append(next_card)
                computer_hand.append(top_card)
                possible_opponent_cards.remove(top_card)
            else:
                comppoints+=1
            playerturn = False
        #endcp

                
        
# test if expectation is correct. seems to be working   
#print "\n\n\n EXPECTED PLAYER HAND:"
#printHandPretty(possible_opponent_cards)
#print "ACTUAL:"
#printHandPretty(player_hand)


print "PLAYER:"+str(playerpoints)
print "COMP:"+str(comppoints)
