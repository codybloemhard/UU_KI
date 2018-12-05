# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    # Agent seems to not be able to cross bridge if discount is changed
    # Agent seems to be able to go always east if noise is below 0.01695
    # Agent cant cross with only discount change because the reward becomes exponentially less significant where
    # The punishment grows harder than the reward
    # See this graph that illustrates the discount against the q value given a distance and noise
    # and given there are no other rewards. As you can see after around 0.1 there is no solution possible
    # https://www.geogebra.org/geometry/qsqxryjz
    answerDiscount = 0.90
    answerNoise = 0.01695
    return answerDiscount, answerNoise


# https://www.desmos.com/calculator/2tiqecnqga graph
def question3a():
    # https://i.imgur.com/ClInQci.png
    # Red line is the short risky route (this one interests us)
    # Blue line is long risky route
    # Green line is safe long route
    answerDiscount = 0.2
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3b():
    # Very simple. Make living reward huge negative to discover long routes
    # Make noise even bigger to discourage risk.
    answerDiscount = 0.5
    answerNoise = 0.1
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3c():
    # Also quite simple. If there is no risk and the long term reward is tempting enough
    # it will pick the longest path along the bridge
    # https://i.imgur.com/Wfsl1qt.png
    # Red line is the short risky route
    # Blue line is long risky route (this one interests us)
    # Green line is safe long route
    # Purple line is safe short route
    answerDiscount = 0.5
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3d():
    # Simple. Make noise high to discourage risk. Pick right gamma to encourage long term reward
    # https://i.imgur.com/a4r73fT.png
    # Red line is the short risky route
    # Blue line is long risky route
    # Green line is safe long route (this one interests us)
    # Purple line is safe short route
    answerDiscount = 0.5
    answerNoise = 0.25
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3e():
    # Put everything to 0 so all values are set to zero because reward is multiplied by gamma which is always zero
    answerDiscount = 0
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question6():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'


if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis

    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
