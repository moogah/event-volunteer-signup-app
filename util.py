from __future__ import annotations
import math
import csv
from volunteer import Volunteer
from task import Task


def get_volunteer_satisfaction_score(
    assignments: dict[Volunteer, list[Task]],
    volunteers: list[Volunteer],
    num_tasks: int,
) -> int:
    """
    Returns an int representing the total satisfaction of the volunteers with the
    current task assignments.

    Each task assigned that the volunteer listed as an interested task earns a
    minimum of 1 point, with tasks listed as a volunteer's first, second, or third
    choice earning 4, 3, and 2 points, respectively.  Each task assigned that the
    volunteer expressed no interest in loses 1 point. Additionally, volunteers lose
    satisfaction points when they are assigned more tasks than they would be if
    tasks were evenly distributed.
    """
    total_satisfaction_score = 0

    if len(assignments) == 0:
        print("No assignments have been made yet.")
        return total_satisfaction_score

    for volunteer in volunteers:
        if volunteer not in assignments:
            continue

        # Calculate a Volunteer's individual satisfaction score.
        volunteer_score = 0
        for task in assignments.get(volunteer):
            if task not in volunteer.interested_tasks:
                volunteer_score -= 1
            else:
                interest_ranking = volunteer.interested_tasks.index(task)
                if interest_ranking < 3:
                    volunteer_score += 4 - interest_ranking
                else:
                    volunteer_score += 1

        # For every Task that a Volunteer has above the number they would
        # have if tasks were evenly distributed, we lose a point. No one
        # wants to feel like they've been asked to do all of the work!
        total_tasks_per_volunteer = math.ceil(num_tasks / len(volunteers))
        number_of_tasks_assigned = len(assignments[volunteer])
        if number_of_tasks_assigned > total_tasks_per_volunteer:
            volunteer_score -= number_of_tasks_assigned - total_tasks_per_volunteer

        total_satisfaction_score += volunteer_score

    return total_satisfaction_score


def load_tasks(csv_filename: str) -> dict[int, Task]:
    tasks = {}
    with open(csv_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        try:
            for parsed_line in csv_reader:
                task_id, name, people_facing, description = parsed_line
                task = Task(int(task_id), name, people_facing == "True", description)
                tasks[int(task_id)] = task
        except csv.Error as e:
            print("Error importing task from", csv_filename, ":\n", e)
    return tasks


def load_volunteers(csv_filename: str, tasks: list[Task]) -> list[Volunteer]:
    volunteers = []
    with open(csv_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        try:
            for parsed_line in csv_reader:
                name, interested_tasks = parsed_line
                volunteer = Volunteer(name)

                # Load in the Volunteer's interested Tasks.
                for task_id_string in interested_tasks.split():
                    volunteer.add_interested_task(tasks.get(int(task_id_string)))
                volunteers.append(volunteer)
        except csv.Error as e:
            print("Error importing volunteer from", csv_filename, ":\n", e)
    return volunteers
