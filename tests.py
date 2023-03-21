from __future__ import annotations
from assignment_server import AssignmentServer
from task import Task
from volunteer import Volunteer
from util import get_volunteer_satisfaction_score

"""
A set of simple tests that you can use to help verify that your code is working
correctly.

These tests are not exhaustive and do not guarantee that your solutions are
fully correct. If you have time, add some tests of your own to help verify your
solutions.
"""


def run_tests(server: AssignmentServer):
    """Runs all of the tests."""
    print("\n~~~~~~~~~~~~~~~~~\n| Running Tests |\n~~~~~~~~~~~~~~~~~")

    # If you have time, add some tests of your own to help verify your solutions.

    # Task 1 tests
    print("\n~~~ Task 1 - INTEREST ROSTER ~~~\n")
    test_interest_roster(server)
    test_task_desirability_score()

    # Task 2 tests
    print("\n~~~ Task 2 - TASKS BY DESIRABILITY ~~~\n")
    test_tasks_by_desirability(server)

    # Task 3 tests
    print("\n~~~ Task 3 - IMPROVED TASK ASSIGNMENTS ~~~\n")
    test_improved_task_assignment(server)


def test_interest_roster(server: AssignmentServer):
    """
    Tests get_interested_volunteers() based on the data in volunteers.csv.
    """
    print("\n*** Task Interest Roster ***\n")
    for task in server.tasks.values():
        print(
            task,
            "(",
            len(server.get_interested_volunteers(task)),
            "):",
            server.get_interested_volunteers(task),
        )


def test_task_desirability_score():
    """
    Tests get_task_desirability_score() with two tasks that the volunteer is
    interested in, and one task that the candidate is not interested in.
    """
    print("\n*** Task Desirability Score ***\n")
    volunteer = Volunteer("Test Volunteer")
    taskA = Task(1, "A", False, "")
    taskB = Task(2, "B", False, "")
    taskC = Task(3, "C", False, "")

    volunteer.interested_tasks = [taskA, taskB]

    tasks_to_expected_scores = {taskA: 1, taskB: 0.5, taskC: 0}

    for task, expected_score in tasks_to_expected_scores.items():
        score = volunteer.get_task_desirability_score(task)
        if score == expected_score:
            emoji = "✅"
        else:
            emoji = "❌"
        print("Task {} Desirability: {} {}".format(task.name, score, emoji))


def test_tasks_by_desirability(server: AssignmentServer):
    """
    Tests get_tasks_by_desirability() based on the data in volunteers.csv.
    The volunteer satisfaction score should be 12.
    """
    sorted_tasks = server.get_tasks_by_desirability()
    if len(sorted_tasks) > 0:
        print("\n*** Tasks Stats ***\n")
        print("Most popular task:", sorted_tasks[0])
        print("Least popular task:", sorted_tasks[len(sorted_tasks) - 1])

    server.assign_tasks()
    print("\n*** Task Assignments ***\n")
    display_assignments(server.assignments)

    print(
        "Volunteer Satisfaction Score:",
        get_volunteer_satisfaction_score(
            server.assignments, server.volunteers, len(server.tasks)
        ),
    )


def test_improved_task_assignment(server: AssignmentServer):
    """
    Tests assign_tasks_improved() based on the data in volunteers.csv.
    """
    server.assignments.clear()
    server.assign_tasks_improved()
    print("\n*** Improved Task Assignments ***\n")
    display_assignments(server.assignments)

    print(
        "Improved Volunteer Satisfaction Score:",
        get_volunteer_satisfaction_score(
            server.assignments, server.volunteers, len(server.tasks)
        ),
    )


def display_assignments(assignments: dict[Volunteer, list[Task]]):
    for volunteer in assignments.keys():
        print("Tasks assigned to", volunteer)
        for task in assignments[volunteer]:
            print("\t", task)
        print("\n")
