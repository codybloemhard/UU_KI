# mira.py
# -------
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


# Mira implementation
import util

PRINT = True


class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        #self.C = 0.004
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter()  # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys()  # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        bestWeights = None
        bestAccuracy = 0

        for C in Cgrid:
            weights = self.trainWithC(trainingData, trainingLabels, C)
            accuracy = self.evaluateWeights(weights, validationData, validationLabels)
            print "Performance on validation set for C=%f: (%.1f%%)" % (C, 100.0 * accuracy / len(validationLabels))

            if accuracy > bestAccuracy:
                bestWeights = weights
                bestAccuracy = accuracy

        self.weights = bestWeights

    def trainWithC(self, inputs, labels, C):
        weights = self.weights.copy()

        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(inputs)):
                # Gather feature and label data
                f = inputs[i]
                y = labels[i]

                # Calculate the scores
                scores = [f * weights[label] for label in self.legalLabels]

                # Extract best label candidate
                yprime = max(scores)
                yprime_index = scores.index(yprime)

                # Calculate Tau
                tauprime = ((weights[yprime_index] - weights[y]) * f + 1.) / float(2. * (f * f))
                tau = min(C, tauprime)

                # Correct the weights
                if yprime != y:
                    # Apply tau
                    ftau = f.copy()
                    for key in ftau.keys():
                        ftau[key] *= tau

                    # Correct the weights
                    weights[yprime_index] -= ftau
                    weights[y] += ftau

        return weights

    def evaluateWeights(self, weights, inputs, labels):
        # Swap out weights temporarily
        tmp_weights = self.weights
        self.weights = weights

        # Evaluate
        predictions = self.classify(inputs)
        accuracyCount = [predictions[i] == labels[i] for i in range(len(labels))].count(True)

        # Swap weigths back in
        self.weights = tmp_weights

        return accuracyCount

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []

        for feat in self.features:
            featuresOdds.append((self.conditionalProb[feat, label1]/self.conditionalProb[feat, label2], feat))
        featuresOdds.sort()
        featuresOdds = [feat for val, feat in featuresOdds[-100:]]

        return featuresOdds

    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        # Gather feature weights for a label
        w = self.weights[label]

        # Sort them by highest first and return array with their indices
        top_features = list(reversed(sorted(w.keys(), key=lambda k: w[k])))

        # return 100 highest features
        return top_features[:100]