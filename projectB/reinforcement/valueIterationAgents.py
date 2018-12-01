# valueIterationAgents.py
# -----------------------
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


from itertools import starmap

import mdp
import util
from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    mdp = None  # type: mdp.MarkovDecisionProcess

    """
        * Please read learningAgents.py before reading this.*`

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.

        Some useful mdp methods you will use:
        mdp.getStates()
        mdp.getPossibleActions(state)
        mdp.getTransitionStatesAndProbs(state, action)
        mdp.getReward(state, action, nextState)
        mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        self.iterateValues(self.iterations)

    def iterateValues(self, max_k):
        """
        Iterates values for k steps
        :param max_k:
        :return:
        """
        for k in range(max_k):
            self.iterateValuesStep()

    def iterateValuesStep(self):
        """
        Does one step of value iteration
        :return:
        """
        new_values = self.values.copy()

        # Update each step if its not a terminal one
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state): continue
            new_values[state] = self.computeValue(state)

        self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
        :type state: Union[str, Tuple[int, int]]
        Compute the Q-value of action in state from the
        value function stored in self.values.
        """

        # Calculates the part of the equation that is within the sum
        def partial_q(_s, t):
            r = self.mdp.getReward(state, action, _s)
            v = self.getValue(_s)
            g = self.discount

            return t * (r + g * v)

        TSP = self.mdp.getTransitionStatesAndProbs(state, action)
        partial_Qs = list(starmap(partial_q, TSP))  # All the partial results that are inside the sum
        Q = sum(partial_Qs)

        return Q

    def computeValue(self, state):
        """
        Computes the k+1 value for given state

        If no actions are available, returns current value.
        :param state:
        :return:
        """
        A = self.mdp.getPossibleActions(state)
        if len(A) == 0: return self.getValue(state)

        # QValue represents rating values from actions. See slides
        return max(self.getQValue(state, a) for a in A)

    def computeActionFromValues(self, state):
        """
        :type state: Union[str, Tuple[int, int]]

        The policy is the best action in the given state
        according to the values currently stored in self.values.

        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        # Does the same a compute value but takes max action instead of max qvalue

        A = self.mdp.getPossibleActions(state)
        if len(A) == 0: return None

        # Homebrewn argmax
        return max(A, key=lambda a: self.getQValue(state, a))

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
