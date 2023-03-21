from task import Task


class Volunteer:
    def __init__(self, name: str):
        self._name = name
        self.interested_tasks: list[Task] = []

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)

    @property
    def name(self):
        return self._name

    def add_interested_task(self, task: Task):
        self.interested_tasks.append(task)

    def remove_interested_task(self, task: Task):
        self.interested_tasks.remove(task)

    def is_interested(self, task: Task) -> bool:
        return task in self.interested_tasks

    def get_task_desirability_score(self, task: Task) -> float:
        """
        Returns a float representing how desirable the given task is to this
        volunteer.
        """
        desire = 0
        try:
            task_index = self.interested_tasks.index(task)
            desire = 1 / (task_index + 1)
        except ValueError:
            pass

        return desire
