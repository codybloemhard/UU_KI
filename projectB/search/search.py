# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def constructPath(road, start, end):
    # construct path to goal
    path = []
    piter = end  # we find it backwards, so start at the end
    while (piter != start):  # as long as we havent found the start yet
        prev = road[piter]  # find the backtrack info in road
        path.append(prev[1])  # append the direction we had to take to get to this node
        piter = prev[0]  # new target is the position we came from to get to this node
    path.reverse()  # reverse it
    return path  # done


def recordEdge(road, node):
    road[node[0]] = (node[1], node[2])


def depthFirstSearch(problem):
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    from game import Directions
    from util import Stack

    root = problem.getStartState()  # starting node
    visited = set()  # positions already visited
    road = {}  # dictionary: pos -> (from pos, with dir)
    end = root  # here the found goal will be stored as pos
    stack = Stack()  # stack used to do DFS, (pos, from pos, with dir)
    stack.push((root, root, Directions.STOP))  # push the root to start

    while (not stack.isEmpty()):
        node = stack.pop()  # get a node
        if (node[0] in visited): continue  # if already seen, go to next node
        visited.add(node[0])  # mark as seen
        recordEdge(road, node)  # record where we came from with which direction
        if (problem.isGoalState(node[0])):  # if this node is the goal
            end = node[0]  # save it
            break  # and stop the loop
        succs = problem.getSuccessors(node[0])  # find all legal moves
        for s in succs:  # forall
            stack.push((s[0], node[0], s[1]))
            # above: push it: (new node pos, node-we came form our current node, dir we took a step in)
    return constructPath(road, root, end)
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    from game import Directions
    from util import Queue

    root = problem.getStartState()  # starting node
    visited = set()  # positions already visited
    road = {}  # dictionary: pos -> (from pos, with dir)
    end = root  # here the found goal will be stored as pos
    queue = Queue()
    queue.push((root, root, Directions.STOP))

    while (not queue.isEmpty()):
        node = queue.pop()  # get a node
        if (node[0] in visited): continue  # if already seen, go to next node
        visited.add(node[0])  # mark as seen
        recordEdge(road, node)  # record where we came from with which direction
        if (problem.isGoalState(node[0])):  # if this node is the goal
            end = node[0]  # save it
            break  # and stop the loop
        succs = problem.getSuccessors(node[0])  # find all legal moves
        for s in succs:  # forall
            queue.push((s[0], node[0], s[1]))
            # above: push it: (new node pos, node-we came form our current node, dir we took a step in)
    return constructPath(road, root, end)
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue
    from game import Directions

    class ANode:
        def __init__(self, state, previous_state, direction, cost=0):
            self.state = state
            self.previous_state = previous_state
            self.direction = direction
            self.cost = cost

    open = PriorityQueue()
    closed = set()
    road = {}

    start_state = problem.getStartState()

    open.push(ANode(start_state, start_state, Directions.STOP), 0)
    while not open.isEmpty():
        current = open.pop()

        # Check whether current node is already closed
        if current.state in closed: continue
        closed.add(current.state)
        recordEdge(road, (current.state, current.previous_state, current.direction))

        # Check whether we are at the goal
        if problem.isGoalState(current.state): return constructPath(road, start_state, current.state)

        # Calculate the cost and add to queue
        for successor in problem.getSuccessors(current.state):
            neighbor = ANode(successor[0], current.state, successor[1], 0)
            neighbor.cost = current.cost + successor[2]  # c(s') = c(s) + C(s, a, s')

            open.push(neighbor, neighbor.cost)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    from game import Directions

    class ANode:
        def __init__(self, state, previous_state, direction, h=0):
            self.state = state
            self.previous_state = previous_state
            self.direction = direction
            self.h = h
            self.g = 0

    start_state = problem.getStartState()
    open = PriorityQueue()
    closed = set()
    road = {}

    open.push(ANode(start_state, start_state, Directions.STOP), 0)
    while not open.isEmpty():
        current = open.pop()

        # Check whether current node is already closed
        if current.state in closed: continue
        closed.add(current.state)
        recordEdge(road, (current.state, current.previous_state, current.direction))

        # Check whether we are at the goal
        if problem.isGoalState(current.state): return constructPath(road, start_state, current.state)

        # Calculate the heuristic + g score for each neighbour node
        for successor in problem.getSuccessors(current.state):
            neighbor = ANode(successor[0], current.state, successor[1])
            neighbor.g = current.g + successor[2]  # g(s') = g(s) + cost(s, a, s')
            neighbor.f = neighbor.g + heuristic(neighbor.state, problem)  # f(s') = g(s') + h(s')

            open.push(neighbor, neighbor.f)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
