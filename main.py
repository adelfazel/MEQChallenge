import socket
import string
from functools import cmp_to_key
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

    def findClosestPathToFinalState(pathSofarString:str,pathSofarNumeric:str='')->str:
        """
        uses explored tree to return shortest path to exit
        """
        currentCharToExplore = pathSofarString[-1]
        for direction in allDirections:
            if explored[currentCharToExplore][direction] == finalState:
                return pathSofarNumeric+direction
        allPaths = []
        for dir in allDirections:
            nextCandidateCharacter = explored[currentCharToExplore][dir]
            if nextCandidateCharacter not in pathSofarString:  # avoid loops
                candidatePathOut = findClosestPathToFinalState(pathSofarString+nextCandidateCharacter,
                                   pathSofarNumeric+dir)
                if candidatePathOut:
                    allPaths.append(candidatePathOut)
        if allPaths:
            return sorted(allPaths, key=len)[0]
        return None

    def findClosestPathToUnexplored(pathSofarString: str, pathSofarNumeric : str='' ) -> str:
        """
        uses explored dictionary to return shortest path to unexplored state
        """
        currentCharToExplore = pathSofarString[-1]
        for direction in allDirections:
            if explored[currentCharToExplore][direction] == unExplored:
                return pathSofarNumeric+direction

        allPaths = []
        for direction in allDirections:
            nextCandidateCharacter = explored[currentCharToExplore][direction]
            if nextCandidateCharacter not in pathSofarString and nextCandidateCharacter != finalState:  # avoid loops
                allPaths.append(
                    findClosestPathToUnexplored(pathSofarString+nextCandidateCharacter, pathSofarNumeric+direction))
        if currentCharToExplore=='A':
            print(allPaths)


        # There are paths that don't lead to exit
        validPaths = list(filter(lambda path: path is not None, allPaths))
        if validPaths:
            return sorted(validPaths, key=len)[0]
        return None

    def exploreationOver() -> bool:
        """
        Returns True if all directions for all nodes are cool
        """

        for char in explored.keys():
            allExploredForThisKey = all(
                explored[char][direction] is not unExplored for direction in allDirections)
            if not allExploredForThisKey:
                return False
        return True
    explored = {state: {direction: unExplored for direction in allDirections}
                for state in string.ascii_uppercase if state != finalState}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(serverDetails)

        receiveInitialState()
        currentCharToExplore = initialState

        while not exploreationOver():
            print(f"currently we are exploring {currentCharToExplore}")
            shortestPathToUnexploredNumeric = findClosestPathToUnexplored(currentCharToExplore)
            if not shortestPathToUnexploredNumeric:
                shortestPathToUnexploredNumeric = findClosestPathToFinalState(currentCharToExplore)
            assert shortestPathToUnexploredNumeric!=None
            for directionToExplore in shortestPathToUnexploredNumeric[:-1]:
                sendMessage(directionToExplore)
                currentCharToExplore = explored[currentCharToExplore][directionToExplore]
            newDirToExplore = shortestPathToUnexploredNumeric[-1]
            newExploredChar = sendMessage(newDirToExplore)
            print(f"just explored {currentCharToExplore}->{newDirToExplore}->{newExploredChar}")
            explored[currentCharToExplore][newDirToExplore] = newExploredChar
            currentCharToExplore = newExploredChar
            if currentCharToExplore == finalState:
                receiveInitialState()
                currentCharToExplore = initialState
            print(f"Current tree:{explored}")
        explored["Z"] = {'-': "A"}
        print(f"full tree:{explored}")
    except socket.error:
        print("unable to establish connection with server")
        exit(1)
    except AssertionError:
        print("no path to victory!")
    finally:
        sock.close()

    graphObject = nx.DiGraph()
    for node, outgoingEdge in explored.items():
        for direction, targetState in outgoingEdge.items():
            graphObject.add_edge(node, targetState)
            nx.set_edge_attributes(
                graphObject, {(node, targetState): {"d": direction}})
    nx.draw_networkx(graphObject, with_labels=True)

    plt.savefig("graphRepresentation.png")
