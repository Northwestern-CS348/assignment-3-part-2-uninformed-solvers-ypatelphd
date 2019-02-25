from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        # Find out what's on each peg
        gameState = self.kb.kb_ask(parse_input("fact: (on ?x ?y)"))

        # Set up a new list to represent each peg
        states = [list(), list(), list()]

        # Loop through the bindings and add the disk number to the appropriate peg numer
        for binding in gameState:
            states[int(binding.bindings_dict["?y"][-1])-1].append(int(binding.bindings_dict["?x"][-1]))

        # Return the sorted lists as tuples
        return tuple((tuple(sorted(states[0])), tuple(sorted(states[1])), tuple(sorted(states[2]))))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

#        print("Making move: {}", movable_statement)
#        print("Before move kb:")
#        print(self.kb)

        # Change which peg the moving disk is on, which disk is now on top of each peg, and what the top is

        # Retract the target peg being empty
        self.kb.kb_retract(parse_input("fact: (empty {})".format(movable_statement.terms[2])))

        # Retract that disk is on starting peg
        self.kb.kb_retract(parse_input("fact: (on {} {})".format(movable_statement.terms[0], movable_statement.terms[1])))

        # Retract that disk is the top of starting peg
        self.kb.kb_retract(parse_input("fact: (top {} {})".format(movable_statement.terms[0], movable_statement.terms[1])))

        # Retract that some other disk is on top of the target peg
        oldPeg = self.kb.kb_ask(parse_input("fact: (top ?x {})".format(movable_statement.terms[2])))
        if oldPeg:
            self.kb.kb_retract(
                parse_input("fact: (top {} {})".format(oldPeg[0].bindings_dict["?x"], movable_statement.terms[2])))

        # Add that disk is on target peg
        self.kb.kb_assert(parse_input("fact: (on {} {})".format(movable_statement.terms[0], movable_statement.terms[2])))

        # Add that disk is the top of target peg
        self.kb.kb_assert(parse_input("fact: (top {} {})".format(movable_statement.terms[0], movable_statement.terms[2])))

        # Assert that either some new disk is on top of starting peg, or starting peg is empty

        # Find out what's left on the old peg
        oldPeg = self.kb.kb_ask(parse_input("fact: (on ?x {})".format(movable_statement.terms[1])))
        if oldPeg:
            # If there are still disks left on the old peg, get the smallest since it must be on top
            oldPegDisks = list()
            for binding in oldPeg:
                oldPegDisks.append(int(binding.bindings_dict["?x"][-1]))

            # Assert that there's a new disk on top of the old peg
            self.kb.kb_assert(parse_input("fact: (top {} {})".format("disk"+str(sorted(oldPegDisks)[0]), movable_statement.terms[1])))

        else:
            # Since no disks were found on the old peg, assert that it's empty
            self.kb.kb_assert(parse_input("fact: (empty {})".format(movable_statement.terms[1])))

#        print("After move kb:")
#        print(self.kb)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        # Find out where everything is
        gameState = self.kb.kb_ask(parse_input("fact: (coordinate ?tile ?pos_x ?pos_y)"))

        # Set up a new list to represent each row
        states = [[None] * 3, [None] * 3, [None] * 3]

        # Loop through the bindings and add the tile number to the appropriate row
        for binding in gameState:
            if binding.bindings_dict["?tile"][0:4] == "tile":
                states[int(binding.bindings_dict["?pos_y"][-1])-1][int(binding.bindings_dict["?pos_x"][-1])-1] =int(binding.bindings_dict["?tile"][-1])
            else:
                states[int(binding.bindings_dict["?pos_y"][-1])-1][int(binding.bindings_dict["?pos_x"][-1])-1] = -1

        # Return the sorted lists as tuples
        return tuple((tuple(states[0]), tuple(states[1]), tuple(states[2])))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # Since the move is permissible, retract the position of the tile and empty, and replace with their new, swapped positions

        # Retract the position of the tile
        self.kb.kb_retract(parse_input("fact: (coordinate {} {} {})".format(movable_statement.terms[0], movable_statement.terms[1], movable_statement.terms[2])))

        # Retract the position of the empty
        self.kb.kb_retract(parse_input("fact: (coordinate empty {} {})".format(movable_statement.terms[3], movable_statement.terms[4])))

        # Assert the new position of the tile
        self.kb.kb_assert(parse_input("fact: (coordinate {} {} {})".format(movable_statement.terms[0], movable_statement.terms[3], movable_statement.terms[4])))

        # Assert the new position of the empty
        self.kb.kb_assert(parse_input("fact: (coordinate empty {} {})".format(movable_statement.terms[1], movable_statement.terms[2])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
