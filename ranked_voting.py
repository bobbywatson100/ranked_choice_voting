from pprint import pprint
import math

#Constants
GAMES_LIST_HEADER = "[games]"
VOTES_LIST_HEADER = "[votes]"


#Global variables
gamesDict = {}
votesDict = {}
voteTally = {}
totalVotes = {}

def addGameToGamesDict(textLine):

    # Split the text line at the tab character
    elements = textLine.split('\t')

    # Use the abbreviation as the key if there are at least two elements in the array
    if len(elements) == 2:
        gamesDict[elements[0]] = elements[1]
        # Also add an entry in the totalVotes dictionary, and set the value (number of votes) to 0
        totalVotes[elements[0]] = 0



def addVotesToVotesDict(textLine):
    
    # Split the text line at the tab character - format should be voter name \t games (CSV)
    elements = textLine.split('\t')

    # Use the abbreviation as the key if there are at least two elements in the array
    if len(elements) == 2:
        # Remove all spaces
        elements[1] = elements[1].replace(' ','')
        votes = elements[1].split(',')
        
        # Add votes to the votes dictionary
        votesDict[elements[0]] = votes

        # Add the votes to the total votes
        for vote in votes:
            totalVotes[vote] += 1



def tallyVotes():
    for vote in votesDict:

        # Ignore lines where all votes have already been removed
        if len(votesDict[vote]) == 0:
            continue

        # Increment the counter for the number of first and second places for each game
        firstGame = votesDict[vote][0]
        voteTally[firstGame][0]+=1
        # If there is a second place, count it
        secondGame = ""
        if len(votesDict[vote]) > 1:
            secondGame = votesDict[vote][1]
            voteTally[secondGame][1]+=1


def checkForWinner(numberOfVoters):
    global voteTally
    global votesDict

    # Determine number of votes required to win (should be at least 50% + 1)
    votesToWin = 0
    if numberOfVoters % 2 == 1:
        votesToWin = math.ceil(numberOfVoters / 2)
    else: 
        votesToWin =  (numberOfVoters / 2) + 1

    winner = ""

    # Check if a game has the number of votes required to win
    for game in voteTally:
        if voteTally[game][0] >= votesToWin:
            winner = game
            break

    return winner


def resetVoteTally():

    # Re-initialize the votesTally dictionary
    global voteTally 
    voteTally = {}
    for game in gamesDict:
        voteTally[game] = [0, 0]


def purgeLowVotes():

    lowestVote = 0
    highestSecond = 0

    # Find lowest non-zero value (and keep track of the one with the highest number of second places)
    for game in voteTally:
        if voteTally[game][0] != 0 and (lowestVote == 0 or lowestVote > voteTally[game][0]):
            lowestVote = voteTally[game][0]
            highestSecond = voteTally[game][1]
        else:
            if voteTally[game][0] == lowestVote and voteTally[game][1] > highestSecond:
                highestSecond = voteTally[game][1]

    # Find all games that have the lowest number of votes
    gamesToRemove = []
    potentialRemovals = []
    for game in voteTally:

        # If the number of first place and second place matches the numbers determined above, keep it as a potential
        if voteTally[game][0] == lowestVote and voteTally[game][1] == highestSecond:
            potentialRemovals.append(game)
        else:
            if voteTally[game][0] == 0 or voteTally[game][0] == lowestVote:
                gamesToRemove.append(game)

    # If no game was selected to be removed, use all the potentials
    if len(gamesToRemove) == 0:
        gamesToRemove = potentialRemovals

    # Remove games from game dictionary
    for game in gamesToRemove:
            del gamesDict[game]

# Remove votes with low number of votes from the votes
    for vote in votesDict:
        for game in gamesToRemove:
            if game in votesDict[vote]:
                votesDict[vote].remove(game)




# Start of main program
print("======================= START OF PROCESSING ========================")

# Open data file and read all of its content
file1 = open('data.txt', 'r') 
Lines = file1.readlines() 
  
inGamesList = False
inVotesList = False
numberOfVoters = 0

# Strips the newline character 
for line in Lines: 

# If either of the header lines is encountered, set the appropriate status flag
    if line.strip() == GAMES_LIST_HEADER:
        inGamesList = True
        continue
    elif line.strip() == VOTES_LIST_HEADER:
        inVotesList = True
        inGamesList = False
        continue
    # Ignore blank lines
    elif line.strip() == '':
        continue
    
    if inGamesList:
        addGameToGamesDict(line.strip())
    elif inVotesList:
        numberOfVoters+=1
        addVotesToVotesDict(line.strip())

# Print total number of votes per game
print("Total votes:")
pprint(totalVotes)

# Declare the winner variable and initialize the votesTally dictionary
winner = ""
resetVoteTally()

# Tally the votes
for x in range(1,10):
    print("==================> Iteration ", x)

    tallyVotes()

# Look at the results and see if there is a winner
    winner = checkForWinner(numberOfVoters)

    pprint(voteTally)

# If a winner has been found, exit the loop
    if winner != "":
        print("Winner: ", winner)
        break

# If there is no winner, remove losers from the votes
    purgeLowVotes()

# Reset the tally
    resetVoteTally()