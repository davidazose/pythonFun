# Name: ...
# CodeFellows Python F2: SEA-C42
# Homework 14: Election prediction

import csv
import os
import time
import math

def read_csv(path):
    """
    Reads the CSV file at path, and returns a list of rows. Each row is a
    dictionary that maps a column name to a value in that column, as a string.
    """
    output = []
    for row in csv.DictReader(open(path)):
        output.append(row)
    return output


################################################################################
# Problem 1: State edges
################################################################################

def row_to_edge(row):
    """
    Given an *ElectionDataRow* or *PollDataRow*, returns the
    Democratic *Edge* in that *State*.
    """
    return float(row["Dem"]) - float(row["Rep"])

def state_edges(election_result_rows):
    """
    Given a list of *ElectionDataRow*s, returns *StateEdge*s.
    The input list has no duplicate *States*;
    that is, each *State* is represented at most once in the input list.
    """
    output = {}
    for item in election_result_rows:
        output[item['State']] = row_to_edge(item);
    return output

################################################################################
# Problem 2: Find the most recent poll row
################################################################################

def earlier_date(date1, date2):
    """
    Given two dates as strings (formatted like "Oct 06 2012"), returns True if
    date1 is before date2.
    """
    return (time.strptime(date1, "%b %d %Y") < time.strptime(date2, "%b %d %Y"))

def most_recent_poll_row(poll_rows, pollster, state):
    """
    Given a list of *PollDataRow*s, returns the most recent row with the
    specified *Pollster* and *State*. If no such row exists, returns None.
    """
    length = len(poll_rows)
    rowIndex = -1
    for i in range(0, length):
        if(poll_rows[i]["Pollster"] == pollster and poll_rows[i]["State"] == state and
            (rowIndex == -1 or earlier_date(poll_rows[rowIndex]["Date"], poll_rows[i]["Date"]))):
            rowIndex = i

    if rowIndex == -1:
        return None;
    else:
        return poll_rows[rowIndex]


################################################################################
# Problem 3: Pollster predictions
################################################################################

def unique_column_values(rows, column_name):
    """
    Given a list of rows and the name of a column (a string),
    returns a set containing all values in that column.
    """
    output = set()
    for row in rows:
        output.add(row[column_name])
    return output



def pollster_predictions(poll_rows):
    """
    Given a list of *PollDataRow*s, returns *PollsterPredictions*.
    For a given pollster, uses only the most recent poll for a state.
    """
    
    output = {}
    pollsterSet = unique_column_values(poll_rows, "Pollster")
    stateSet = unique_column_values(poll_rows, "State")

    for pollster in pollsterSet:
        recentList = []
        for state in stateSet:
            recent = most_recent_poll_row(poll_rows, pollster, state)
            if recent != None:
                recentList.append(recent)
        
        if len(recentList) > 0:
            output[pollster] = state_edges(recentList)

    return output

################################################################################
# Problem 4: Pollster errors
################################################################################

def average_error(state_edges_predicted, state_edges_actual):
    """
    Given predicted *StateEdges* and actual *StateEdges*, returns
    the average error of the prediction.
    """
    
    items = 0;
    delta = 0;
    for key, value in state_edges_actual.items():
        if(key in state_edges_predicted):
            diff = math.fabs(value - state_edges_predicted[key])
            delta += diff
            items += 1

    if(items > 0):
        return delta / items;
    else:
        return 0;


def pollster_errors(pollster_predictions, state_edges_actual):
    """
    Given *PollsterPredictions* and actual *StateEdges*,
    retuns *PollsterErrors*.
    """
    
    output = {}
    for key, value in pollster_predictions.items():
        output[key] = average_error(value, state_edges_actual)
    return output


################################################################################
# Problem 5: Pivot a nested dictionary
################################################################################

def pivot_nested_dict(nested_dict):
    """
    Pivots a nested dictionary, producing a different nested dictionary
    containing the same values.
    The input is a dictionary d1 that maps from keys k1 to dictionaries d2,
    where d2 maps from keys k2 to values v.
    The output is a dictionary d3 that maps from keys k2 to dictionaries d4,
    where d4 maps from keys k1 to values v.
    For example:
      input = { "a" : { "x": 1, "y": 2 },
                "b" : { "x": 3, "z": 4 } }
      output = {'y': {'a': 2},
                'x': {'a': 1, 'b': 3},
                'z': {'b': 4} }
    """
    output = {}
    for k1, d2 in nested_dict.items():
        for k2, v in d2.items():
            if(k2 not in output):
                output[k2] = {k1: v}
            else:
                output[k2][k1] = v
    return output


################################################################################
# Problem 6: Average the edges in a single state
################################################################################

def average_error_to_weight(error):
    """
    Given the average error of a pollster, returns that pollster's weight.
    The error must be a positive number.
    """
    return error ** (-2)

# The default average error of a pollster who did no polling in the
# previous election.
DEFAULT_AVERAGE_ERROR = 5.0

def pollster_to_weight(pollster, pollster_errors):
    """"
    Given a *Pollster* and a *PollsterErrors*,
    return the given pollster's weight.
    """
    if pollster not in pollster_errors:
        weight = average_error_to_weight(DEFAULT_AVERAGE_ERROR)
    else:
        weight = average_error_to_weight(pollster_errors[pollster])
    return weight


def weighted_average(items, weights):
    """
    Returns the weighted average of a list of items.

    Arguments:
    items is a list of numbers.
    weights is a list of numbers, whose sum is nonzero.

    Each weight in weights corresponds to the item in items at the same index.
    items and weights must be the same length.
    """
    assert len(items) > 0
    assert len(items) == len(weights)
    
    sum = 0
    count = 0
    length = len(items)
    for i in range(0, length):
        sum += items[i] * weights[i]
        count += weights[i]
    return sum / count


def average_edge(pollster_edges, pollster_errors):
    """
    Given *PollsterEdges* and *PollsterErrors*, returns the average
    of these *Edge*s weighted by their respective *PollsterErrors*.
    """
    items = []
    weights = []
    for k,v in pollster_edges.items():
        items.append(v)
        weight = pollster_to_weight(k, pollster_errors)
        weights.append(weight)
    return weighted_average(items, weights)

# ################################################################################
# # Problem 7: Predict the 2012 election
# ################################################################################

# def predict_state_edges(pollster_predictions, pollster_errors):
#     """
#     Given *PollsterPredictions* from a current election and
#     *PollsterErrors* from a past election,
#     returns the predicted *StateEdges* of the current election.
#     """
#     #TODO: Implement this function
#     pass


# ################################################################################
# # Electoral College, Main Function, etc.
# ################################################################################

# def electoral_college_outcome(ec_rows, state_edges):
#     """
#     Given electoral college rows and state edges, returns the outcome of
#     the Electoral College, as a map from "Dem" or "Rep" to a number of
#     electoral votes won.  If a state has an edge of exactly 0.0, its votes
#     are evenly divided between both parties.
#     """
#     ec_votes = {}               # maps from state to number of electoral votes
#     for row in ec_rows:
#         ec_votes[row["State"]] = float(row["Electors"])

#     outcome = {"Dem": 0, "Rep": 0}
#     for state in state_edges:
#         votes = ec_votes[state]
#         if state_edges[state] > 0:
#             outcome["Dem"] += votes
#         elif state_edges[state] < 0:
#             outcome["Rep"] += votes
#         else:
#             outcome["Dem"] += votes/2.0
#             outcome["Rep"] += votes/2.0
#     return outcome


# def print_dict(dictionary):
#     """
#     Given a dictionary, prints its contents in sorted order by key.
#     Rounds float values to 8 decimal places.
#     """
#     for key in sorted(dictionary.keys()):
#         value = dictionary[key]
#         if type(value) == float:
#             value = round(value, 8)
#         print(key, value)


# def main():
#     """
#     Main function, which is executed when election.py is run as a Python script.
#     """
#     # Read state edges from the 2008 election
#     edges_2008 = state_edges(read_csv("data/2008-results.csv"))

#     # Read pollster predictions from the 2008 and 2012 election
#     polls_2008 = pollster_predictions(read_csv("data/2008-polls.csv"))
#     polls_2012 = pollster_predictions(read_csv("data/2012-polls.csv"))

#     # Compute pollster errors for the 2008 election
#     error_2008 = pollster_errors(polls_2008, edges_2008)

#     # Predict the 2012 state edges
#     prediction_2012 = predict_state_edges(polls_2012, error_2008)

#     # Obtain the 2012 Electoral College outcome
#     ec_2012 = electoral_college_outcome(read_csv("data/2012-electoral-college.csv"),
#                                         prediction_2012)

#     print("Predicted 2012 election results:")
#     print_dict(prediction_2012)
#     print()

#     print("Predicted 2012 Electoral College outcome:")
#     print_dict(ec_2012)
#     print()


# # If this file, election.py, is run as a Python script (such as by typing
# # "python election.py" at the command shell), then run the main() function.
# if __name__ == "__main__":
#     main()


# ###
# ### Collaboration
# ###

# # ... Write your answer here, as a comment (on lines starting with "#").
