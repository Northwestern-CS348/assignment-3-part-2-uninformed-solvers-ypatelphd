from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # Expand children, make move, update game state

        # First check to see if this is the winning state. If so, return true and drop out
#        print("starting kb:")
#        print(self.gm.kb)
#        print("current state:")
#        print(self.currentState.state)
#        print("victory condition:")
#        print(self.victoryCondition)
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            # Not a winning state, so get all the permissible moves
            moves = self.gm.getMovables()

#            print("Possible moves:")
#            print(moves)
#
            # Check to see if there are permissable moves, or if we've reached a terminal node
            if moves:
                # Loop through the moves, make a child state for each move, link to parent
                for move in moves:
                    # First make the move
                    self.gm.makeMove(move)

                    # Create new GameState for each child

                    # First we'll create a GameState with no depth or requiredMovable to see if we've already visited this state
                    # If we haven't proceed with adding the child, otherwise skip. This prevents infinite loops
                    child = GameState(self.gm.getGameState(), 0, None)

 #                   print("here's visited:")
 #                   print(self.visited)
 #                   for i in self.visited.keys():
 #                       print(i.state)
 #                   print("here's the child:")
 #                   print(child)
 #                   print(child.state)
 #                   print("checking...")
 #                   print(child not in self.visited or not self.visited[child])
 #                   print("checked...")
#
                    if child not in self.visited or not self.visited[child]:
#                    if (self.currentState.depth == 0) or (child.state != self.currentState.parent.state):
                        self.visited[child] = False
                        child.depth = self.currentState.depth + 1
                        child.requiredMovable = move
                        child.parent = self.currentState
                        self.currentState.children.append(child)

                    # Reverse the move to get back to current state
                    self.gm.reverseMove(move)

            # At this point, all children of the current state have been expanded

            # If there are no children left to visit, keep moving backwards until there are (or you reach the top)
            while (self.currentState.nextChildToVisit >= len(self.currentState.children)) and (self.currentState.depth > 0):
                # Update the game state to move back one move
#                print("################# backing up move:")
                self.gm.reverseMove(self.currentState.requiredMovable)

                # Update the current state to point to the child we're on
                self.currentState = self.currentState.parent

            # At this point, either I'm back up to the top of the tree, or I've got a sibling I can visit

            # If there are remaining children to visit, go to the next child
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                # Update the game state to reflect the move
#                print("########## MAKING MOVE ############")
                self.gm.makeMove(self.currentState.children[self.currentState.nextChildToVisit].requiredMovable)

                # Update the current state to point to the child we're on; mark visited
                self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.parent.nextChildToVisit += 1

                # Since visited only stores which states we've been in (regardless of level or move), we need a "clean" state to set here
#                self.visited[self.currentState] = True
                self.visited[GameState(self.gm.getGameState(), 0, None)] = True

                # Check to see if we're at a solution
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            else:
                # There are no children left to visit, so I must be back to the top of the tree, so return false
#                print("ending kb:")
#                print(self.gm.kb)
                return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            # If we're at the victory condition, return true
            self.visited[self.currentState] = True
            return True
        elif not self.currentState.children:
            # Not a winning state, so get all the permissible moves
            moves = self.gm.getMovables()

            # Check to see if there are permissable moves, or if we've reached a terminal node
            if moves:
                # Loop through the moves, make a child state for each move, link to parent
                for move in moves:
                    # First make the move
                    self.gm.makeMove(move)

                    # Create new GameState for each child
                    child = GameState(self.gm.getGameState(), 0, None)

                    if not self.visited.get(child, False):
                        self.visited[child] = False
                        child.depth = self.currentState.depth + 1
                        child.requiredMovable = move
                        child.parent = self.currentState
                        self.currentState.children.append(child)

                    # Reverse the move to get back to current state
                    self.gm.reverseMove(move)

            # At this point, all children of the current state have been expanded so call recursive procedure
            return self.recursiveHelper()

    def recursiveHelper(self):
        # First check to see if this node has any siblings, if so, visit them
        if self.currentState.parent and self.currentState.parent.children.index(self.currentState) < len(self.currentState.parent.children)-1:
            idx = self.currentState.parent.children.index(self.currentState)
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.gm.makeMove(self.currentState.children[idx+1].requiredMovable)
            self.currentState = self.currentState.children[idx+1]
            if not self.visited.get(self.currentState):
                self.visited[self.currentState] = True

                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            else:
                return self.recursiveHelper()
        else:
            # I've got no siblings left so move up
            while self.currentState.parent and (self.currentState.parent.children.index(self.currentState) == len(self.currentState.parent.children)-1):
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

            # At this point either the current node is the root, or it has a sibling
            if self.currentState.parent:
                return self.recursiveHelper()
            if not self.currentState.parent:
                # We're at the root node, so we need to come down
                while self.visited.get(self.currentState, False) and self.currentState.children:
                    self.gm.makeMove(self.currentState.children[0].requiredMovable)
                    self.currentState = self.currentState.children[0]
#                    print("Just set a left node!")
#                    print(self.currentState)
#                    print(self.visited.get(self.currentState, False))
                if self.visited.get(self.currentState, False):
                    # You've been visited before, but have no children, so call SolveOneStep to proceed
                    return self.solveOneStep()
                else:
                    # You haven't been visited and this is a new node, so test and exit
#                    print("Found new left child!")
                    self.visited[self.currentState] = True

                    if self.currentState.state == self.victoryCondition:
                        return True
                    else:
                        return False

