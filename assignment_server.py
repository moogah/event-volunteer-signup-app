from __future__ import annotations
from util import load_volunteers, load_tasks
from task import Task
from volunteer import Volunteer
import heapq


class AssignmentServer:
    def __init__(self):
        self.assignments: dict[Volunteer, list[Task]] = {}
        self.tasks: dict[int, Task] = {}
        self.volunteers: list[Volunteer] = []
        self.tasks_by_desirability: list[dict] = []
        self.priority_tasks_by_desirability: list[dict] = []

    def import_tasks_from_csv(self, csv_filename: str):
        self.tasks = load_tasks(csv_filename)

    def import_volunteers_from_csv(self, csv_filename: str):
        self.volunteers.extend(load_volunteers(csv_filename, self.tasks))

    def get_interested_volunteers(self, task: Task) -> list[Volunteer]:
        """
        Returns a List of the Volunteers who have indicated interest in the
        given task.
        """

        interested_volunteers = []

        for volunteer in self.volunteers:
            if volunteer.is_interested(task):
                interested_volunteers.append(volunteer)

        return interested_volunteers

    def get_tasks_by_desirability(self) -> list[Task]:
        """
        Returns a List of Tasks sorted by desirability.

        Pushing tasks onto a heap feels like a good approach here, since this data structure would also then be useful during assignment
        """

        desire_sum = 0

        for id, task in self.tasks.items():
            for volunteer in self.volunteers:
                desire_sum += volunteer.get_task_desirability_score(task)

            if task.people_facing:
                heapq.heappush(self.priority_tasks_by_desirability,
                               (desire_sum, task.id))
            else:
                heapq.heappush(self.tasks_by_desirability,
                               (desire_sum, task.id))

        return self.priority_tasks_by_desirability + self.tasks_by_desirability

    def assign_tasks(self):
        """
        Assigns Tasks to Volunteers by inserting them into the assignment map,
        in order of desirability. Tasks are assigned to the first Volunteer with
        interest. If there are no interested Volunteers, they are assigned to the
        first available Volunteer.
        """
        for task in self.get_tasks_by_desirability():
            interested_volunteers = self.get_interested_volunteers(task)

            if len(interested_volunteers) > 0:
                self.assign_task(task, interested_volunteers[0])
            elif len(self.volunteers) > 0:
                self.assign_task(task, self.volunteers[0])

    def assign_task(self, task: Task, volunteer: Volunteer):
        """
        Adds the given Task to the specified Volunteer's Set of assigned Tasks.
        """
        if volunteer not in self.assignments:
            self.assignments[volunteer] = set()
        self.assignments[volunteer].add(task)

    def assign_tasks_improved(self):
        """
        Assigns Tasks to Volunteers based on their interests.
        """

        # TODO: Implement this method. See the README for more details.

        pass
