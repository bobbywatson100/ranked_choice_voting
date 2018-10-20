import json
from pprint import pprint

# This function initializes an array with all games that have votes
def initGamesDict(choices):

    gamesDict = { }

    for choice in choices:
        if choice not in gamesDict:
            gamesDict[choice] = 0

    return gamesDict

# This function removes games with the lowest number of votes from the games dictionary and
#    from all players' choices
def disqualifyGames(gamesDict, votes, numVotes):
    gamesToRemove = []

# Remove games with the least number of votes fromt the master game dictionary
    for game in gamesDict:
        if gamesDict[game] == numVotes:
            print("Removing ", game, " with ", numVotes, " votes")
            gamesToRemove.append(game)

    for gameToRemove in gamesToRemove:
        del gamesDict[gameToRemove]

# Remove all games with the lowest number of votes from all choices lists
    for vote in votes:
        for game in gamesToRemove:
            if game in vote["choices"]:
                vote["choices"].remove(game)

def votingRound(gamesDict, votes):
    majorityThreshold = len(votes)//2 + 1
    gameHasMajority = None
    leastVotes = None

# Count how many times games are ranked as the highest
    for vote in votes:
        choices = vote["choices"]
        if choices[0] != None:
            gamesDict[choices[0]] = gamesDict[choices[0]] + 1

# Check if the current game has the majority of votes
    for game in gamesDict:
        if gamesDict[game] >= majorityThreshold:
            gameHasMajority = game
            break
        else:
# Determine if the current game has the lowest number of votes so far
            if leastVotes == None or gamesDict[game] < leastVotes:
                leastVotes = gamesDict[game]

# If no game has the majority, remove the least voted for game from all votes
    if gameHasMajority == None:
#        for vote in votes:
#            choices = vote["choices"]
#            if leastVotedGame in choices:
#                choices.remove(leastVotedGame)
# And also remove the least voted game from the list of gamesDict

#        del gamesDict[leastVotedGame]
        disqualifyGames(gamesDict, votes, leastVotes)
        return None
    else:
        return gameHasMajority

print("======================= START OF PROCESSING ========================")

with open("votes.json") as f:
    data = json.load(f)

gamesDict = initGamesDict(data["choices"]);


for x in range(1,4):

    print("======= Iteration", x, " ===========")

    votingResult = votingRound(gamesDict, data["votes"])

    print("Results for iteration ", x)
    pprint(gamesDict)

# If a winner has been found, show it an exit
    if votingResult:
        print(votingResult, " won!")
        break
    else:
        print("No winner found in iteration", x)

print("======================== END OF PROCESSING =========================")
