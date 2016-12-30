from scipy.integrate import quad
import numpy as np
from prettytable import PrettyTable


def integral_solution(interval_bounds, family):
    answers = []

    for function in family:
        answers.append(quad(lambda x: eval(function), interval_bounds[0], interval_bounds[1])[0])

    return answers


def midpoint_rule(interval_bounds, partitions, family):
    intervals = list()  # array of all dx's
    dx = ((interval_bounds[1] - interval_bounds[0]) / partitions)
    step = interval_bounds[0]

    while step <= interval_bounds[1]:
        intervals.append(step)
        step += dx

    answers = [0.0] * len(family)
    i = 0
    while i < len(intervals) - 1:
        x = ((intervals[i] + intervals[i+1]) / 2.0)  # evaluate each with x
        for j in range(0, len(family)):
            answers[j] += 2*(eval(family[j]))
        i += 1
    return answers


def trapezoidal_rule(interval_bounds, partitions, family):
    x = list()  # array of all dx's
    dx = ((interval_bounds[1] - interval_bounds[0]) / partitions)
    step = interval_bounds[0]

    while step <= interval_bounds[1]:
        x.append(step)
        step += dx

    x = np.array(x)

    answers = []
    for function in family:
        if function.isdigit():
            answers.append(np.trapz(int(function) + (0*x), x))  # check if constant
        else:
            answers.append(np.trapz(eval(function), x))
    return answers


def find_weight(midpoint_rule_value, trapezoidal_rule_value, integral_value, family):
    answers = [0] * len(family)
    i = 0
    while i <= len(answers) - 1:
        if trapezoidal_rule_value[i] - midpoint_rule_value[i] == 0:
            answers[i] = 0
        else:
            answers[i] = (trapezoidal_rule_value[i] - integral_value[i]) / \
                         (trapezoidal_rule_value[i] - midpoint_rule_value[i])
        i += 1

    return answers


def table(family, midpoint_value, trapezoidal_value, integral_value, weights):
    table = PrettyTable()
    table.add_column("Functions", family)
    table.add_column("Midpoint Values", midpoint_value)
    table.add_column("Trapezoidal Values", trapezoidal_value)
    table.add_column("Integral Values", integral_value)
    table.add_column("Scalar Constants", weights)

    return table

def main():
    family = []
    print("Warning: Use ** for exponents instead of ^")
    while True:
        function = input("Please enter your next function or press q to finish: ")
        if function == "q" or function == "Q":
            break
        else:
            family.append(function)
    partitions = int(input("How many partitions? "))
    start = int(input("Interval start? "))
    end = int(input("Interval end? "))
    interval_bounds = [start, end]

    integral_value = integral_solution(interval_bounds, family)
    midpoint_value = midpoint_rule(interval_bounds, partitions, family)
    trapezoidal_value = trapezoidal_rule(interval_bounds, partitions*2, family)
    weights = find_weight(midpoint_value, trapezoidal_value, integral_value, family)
    print(table(family, midpoint_value, trapezoidal_value, integral_value, weights))

if __name__ == main():
    main()
