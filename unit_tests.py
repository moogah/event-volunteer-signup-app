import unittest
from unittest.mock import MagicMock
from assignment_server import AssignmentServer
from volunteer import Volunteer


class TestAssignmentServer(unittest.TestCase):

    def test_get_interested_volunteers__returns_empty_array(self):
        """
        check that we get an empty array when nothing is initialized.
        """
        server = AssignmentServer()
        task = 'test_task'

        self.assertEqual(server.get_interested_volunteers(task), [])

    def test_get_interested_volunteers__handles_none(self):
        """
        check that the function handles None in a predictable way
        """
        server = AssignmentServer()
        self.assertEqual(server.get_interested_volunteers(None), [])

    def test_get_interested_volunteers__calls_volunteer_is_interested(self):
        """
        check that we call the correct external method
        """
        server = AssignmentServer()
        task = 'test_task'
        volunteer = MagicMock()

        server.volunteers = [volunteer]

        # mock is_interested so we can check that it's called exactly how we expect.
        volunteer.is_interested = MagicMock()

        _ = server.get_interested_volunteers(task)

        volunteer.is_interested.assert_called_with(task)

    def test_get_interested_volunteers__returns_interested_volunteers(self):
        """
        check that we return the correct volunteer
        """
        server = AssignmentServer()
        volunteer = MagicMock()
        volunteer.is_interested = MagicMock(return_value=True)

        server.volunteers = [volunteer]

        # This test case is not about the logic of "task in volunteer.interested_tasks",
        # only that get_interested_volunteers processes the result of is_interested correctly
        interested_volunteers = server.get_interested_volunteers(None)

        self.assertEqual(interested_volunteers, [volunteer])

    def test_get_interested_volunteers__doesnt_return_uninterested_volunteers(self):
        """
        check that we don't return uninterested volunteers
        """
        server = AssignmentServer()
        volunteer = MagicMock()
        volunteer.is_interested = MagicMock(return_value=False)

        server.volunteers = [volunteer]

        interested_volunteers = server.get_interested_volunteers(None)

        self.assertEqual(interested_volunteers, [])

    def test_get_interested_volunteers__only_returns_interested_volunteers(self):
        """
        check that we only return interested volunteers
        """
        server = AssignmentServer()
        interested_volunteer = MagicMock()
        uninterested_volunteer = MagicMock()
        interested_volunteer.is_interested = MagicMock(return_value=True)
        uninterested_volunteer.is_interested = MagicMock(return_value=False)

        server.volunteers = [interested_volunteer, uninterested_volunteer]

        interested_volunteers = server.get_interested_volunteers(None)

        self.assertEqual(interested_volunteers, [interested_volunteer])

    def test_get_tasks_by_desirability__returns_empty_array(self):
        """
        check that we return [] by default
        """
        server = AssignmentServer()
        self.assertEqual(server.get_tasks_by_desirability(), [])

    def test_get_tasks_by_desirability__orders_tasks(self):
        """
        check that we order tasks correctly
        """
        server = AssignmentServer()

        volunteer1 = MagicMock()
        volunteer1.get_task_desirability_score = MagicMock()
        # desirability approaches zero for more desireable tasks
        # not immediatly intuitive, but helpful for the heap implementation
        # since python's heap is a minHeap where smaller items are at the top
        volunteer1.get_task_desirability_score.side_effect = [
            0.5,
            0.3,
            0.25
        ]

        volunteer2 = MagicMock()
        volunteer2.get_task_desirability_score = MagicMock()
        volunteer2.get_task_desirability_score.side_effect = [
            0.3,
            0.2,
            0.0
        ]

        volunteer3 = MagicMock()
        volunteer3.get_task_desirability_score = MagicMock()
        volunteer3.get_task_desirability_score.side_effect = [
            0.5,
            0.0,
            0.0
        ]

        server.tasks = {
            1: MagicMock(id=1, people_facing=False),
            2: MagicMock(id=2, people_facing=False),
            3: MagicMock(id=3, people_facing=False)
        }

        server.volunteers = [
            volunteer1,
            volunteer2,
            volunteer3
        ]

        expected_result = [(1.3, 1), (1.8, 2), (2.05, 3)]
        #                        ^ task 1  ^ task 2   ^ task 3

        self.assertEqual(server.get_tasks_by_desirability(), expected_result)

    def test_get_tasks_by_desirability__orders_public_tasks_first(self):
        """
        check that public facing tasks are ordered first
        """
        server = AssignmentServer()

        volunteer1 = MagicMock()
        volunteer1.get_task_desirability_score = MagicMock()
        volunteer1.get_task_desirability_score.side_effect = [
            0.5,
            0.3,
            0.25
        ]

        volunteer2 = MagicMock()
        volunteer2.get_task_desirability_score = MagicMock()
        volunteer2.get_task_desirability_score.side_effect = [
            0.3,
            0.2,
            0.0
        ]

        volunteer3 = MagicMock()
        volunteer3.get_task_desirability_score = MagicMock()
        volunteer3.get_task_desirability_score.side_effect = [
            0.5,
            0.0,
            0.0
        ]

        server.tasks = {
            1: MagicMock(id=1, people_facing=False),
            2: MagicMock(id=2, people_facing=False),
            # public facing task should show up first in the results
            3: MagicMock(id=3, people_facing=True)
        }

        server.volunteers = [
            volunteer1,
            volunteer2,
            volunteer3
        ]

        expected_result = [(2.05, 3), (1.3, 1), (1.8, 2)]
        #                         ^ task 3  ^ task 2   ^ task 2

        self.assertEqual(server.get_tasks_by_desirability(), expected_result)


class TestVolunteer(unittest.TestCase):

    def test_get_desireability_score__returns_zero_by_default(self):
        """
        check that get_task_desirability_score returns 0
        """
        volunteer = Volunteer(name='test_volunteer')

        self.assertEqual(volunteer.get_task_desirability_score(None), 0)

    def test_get_desireability_score__calculates_score_by_index(self):
        """
        check that the score calculation is correct
        """
        volunteer = Volunteer(name='test_volunteer')

        # @TODO is there a better way to do this?
        # list.index is read-only so we can't mock it directly
        volunteer.interested_tasks = MagicMock()
        volunteer.interested_tasks.index = MagicMock(return_value=1)

        self.assertEqual(volunteer.get_task_desirability_score(None), 0.5)

    @unittest.skip("Consider if checking the handling of ValueError is useful here")
    def test_get_desireability_score__handles_value_error(self):
        pass


if __name__ == '__main__':
    unittest.main()
