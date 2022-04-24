import socket
import string

import networkx as nx

import matplotlib.pyplot as plt

# Concept inventory
# 1-useful to have a function sendMessage that sends a number and returns response by the server.
# 2-
if __name__ == "__main__":
    MAX_MSG_SIZE = 16
    unExplored = None
    finalState = 'Z'
    initialState = 'A'
    allDirections = '123'
    serverDetails = ('20.211.33.233', 65432)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(serverDetails)
    except socket.error:
        print("unable to estalbish connection with server")
        exit(1)

    def receiveInitialState():
        """
        recieve until msg 'initialState' message
        """
        msg = ''
        while initialState not in msg:
            msg = sock.recv(MAX_MSG_SIZE).decode("utf-8").strip()
        print(f'{initialState} recieved')

    def sendMessage(msg: str) -> str:
        """
        input: msg to send to server
        output: response from server
        """

        sock.sendall(bytes(f"{msg}\n", 'utf-8'))
        print(f"{msg} sent")
        rsvMsg = sock.recv(MAX_MSG_SIZE).decode("utf-8").strip()
        print(f"{rsvMsg} recieved")
        return rsvMsg

    def findClosestPathToFinalState(pathSofarNumeric, pathSofarString):
        """
        uses explored dictionary to return shortest path to unexplored state; if no such path found, returns closest path to exit.
        """
        currentCharToExplore = pathSofarString[-1]
        for dir in allDirections:
            if explored[currentCharToExplore][dir] == finalState:
                return pathSofarNumeric+dir

        allPaths = []
        for dir in allDirections:
            nextCandidateCharacter = explored[currentCharToExplore][dir]

            if nextCandidateCharacter not in pathSofarString:  # avoid loops
                candidatePathOut = findClosestPathToFinalState(pathSofarNumeric+dir,
                                                               pathSofarString+nextCandidateCharacter)
                if candidatePathOut:
                    allPaths.append(candidatePathOut)
        if allPaths:
            return sorted(allPaths, key=len)[0]
        return None

    def findClosestPathToUnexplored(pathSofarNumeric: str, pathSofarString: str) -> str:
        """
        uses explored dictionary to return shortest path to unexplored state
        """
        currentCharToExplore = pathSofarString[-1]
        for dir in allDirections:
            if explored[currentCharToExplore][dir] == unExplored:
                return pathSofarNumeric+dir

        allPaths = []
        for dir in allDirections:
            nextCandidateCharacter = explored[currentCharToExplore][dir]
            if nextCandidateCharacter not in pathSofarString and nextCandidateCharacter != finalState:  # avoid loops
                allPaths.append(
                    findClosestPathToUnexplored(pathSofarNumeric+dir,
                                                pathSofarString+nextCandidateCharacter))
        if not allPaths:
            # special case when exploration cannot find a new state from current place, need to find the closest exit
            return findClosestPathToFinalState(pathSofarNumeric, pathSofarString)

        # There are paths that don't lead to exit
        validPaths = list(filter(lambda path: path is not None, allPaths))
        if validPaths:
            return sorted(validPaths, key=len)[0]
        return None

    def exploreationOver() -> bool:
        for char in explored.keys():
            allExploredForThisKey = all(
                explored[char][dir] is not None for dir in allDirections)
            if not allExploredForThisKey:
                return False
        return True
    explored = {state: {direction: None for direction in allDirections}
                for state in string.ascii_uppercase if state != finalState}

    receiveInitialState()
    currentCharToExplore = initialState
    while not exploreationOver():
        shortestPathToUnexploredNumric = findClosestPathToUnexplored(
            '', currentCharToExplore)

        for directionToExplore in shortestPathToUnexploredNumric[:-1]:
            sendMessage(directionToExplore)
            currentCharToExplore = explored[currentCharToExplore][directionToExplore]
        newDirToExplore = shortestPathToUnexploredNumric[-1]
        newExploredChar = sendMessage(newDirToExplore)
        print(f"{currentCharToExplore}->{newDirToExplore}->{newExploredChar}")
        explored[currentCharToExplore][newDirToExplore] = newExploredChar
        currentCharToExplore = newExploredChar
        if currentCharToExplore == finalState:
            receiveInitialState()
            currentCharToExplore = initialState
    explored["Z"] = {'-': "A"}
    print(explored)
    sock.close()

    graphObject = nx.DiGraph()
    for node, outgoingEdge in explored.items():
        for direction, targetState in outgoingEdge.items():
            graphObject.add_edge(node, targetState)
            nx.set_edge_attributes(
                graphObject, {(node, targetState): {"d": direction}})
    nx.draw_networkx(graphObject, with_labels=True)

    plt.savefig("graphRepresentation.png")
