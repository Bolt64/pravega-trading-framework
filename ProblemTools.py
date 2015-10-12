from itertools import takewhile
from UserTools import decomment
from logic import Problem

PROBLEM_FILE = "problem_file.dat"

def parseProblemFile(filename, comment="#"):
    problems = []
    for line in decomment(filename, comment):
        name, display_name, answer, base_points, multiplier, *dependencies = line.strip().split(", ")
        problems.append((name, str(Problem(name, display_name, answer, int(base_points), float(multiplier), dependencies))))
    return problems

def display_problems_per_user(user_stats, parsed_problem_file):
    table_to_display = []
    for name, problem_string in parsed_problem_file:
        display_name = Problem.fromString(problem_string).display_name
        row = []
        row.append(display_name)
        #row.append(problem_string)

        if name in user_stats['problems_solved']:
            row.append("Yes")
        else:
            row.append("No")

        if name in user_stats['problems_solved'] and (not name in user_stats['solutions_bought']):
            row.append("Yes")
        else:
            row.append("No")

        if name in user_stats['solutions_bought']:
            row.append("Yes")
        else:
            row.append("No")

        if name in (i[0] for i in user_stats['solutions_sold']):
            row.append("Yes")
        else:
            row.append("No")

        table_to_display.append(row)

    return table_to_display

def categorize_problems(user_stats, parsed_problem_file):
    categories = {"to_solve": [], "to_sell": [], "on_market": []}
    problems = [(name, Problem.fromString(problem_string)) for name, problem_string in parsed_problem_file]
    for name, problem in problems:
        if not name in user_stats['problems_solved']:
            for dependency in problem.dependencies:
                if dependency in user_stats['problems_solved']:
                    categories["to_solve"].append((name, problem))

    return categories
