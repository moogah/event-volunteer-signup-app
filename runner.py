from assignment_server import AssignmentServer
from tests import run_tests


class Runner:
    def run(self):
        self.print_intro("Assignment Server")

        # Initialize AssignmentServer instance.
        server = AssignmentServer()
        server.import_tasks_from_csv("tasks.csv")
        server.import_volunteers_from_csv("volunteers.csv")

        run_tests(server)

    def print_intro(self, codebase_title: str):
        """Prints a brief intro to the codebase."""
        print("\nWelcome to the " + codebase_title + " codebase!")
        print("Start by reading through the README file for your instructions,")
        print("then familiarize yourself with the rest of the files in the codebase.")
        print("When you're ready, start tackling the TODOs in the codebase.\n")


if __name__ == "__main__":
    Runner().run()
