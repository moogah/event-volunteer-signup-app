# Changelog

get_interested_volunteers and get_tasks_by_desireability in `assignment_server.py` have implementations
get_task_desirability_score in `volunteer.py` has an implementation
`unit_test.py` contains tests for all 3 of the above
`run_volunteer.sh` has been modified to run the unit tests, and to fail loudly if they do not pass.

# Getting Started

run `sh run_volunteer.sh` to execute both unit tests and a sort of functional test suite.

# Testing

I have strong opinions about testing and the included "test" file caused a lot of cognitive dissonance, particularly for a Python project where [unittest](https://docs.python.org/3/library/unittest.html) is a built in library.  If I was sent a PR containing this code I'd want to have a chat with the authors so that I could understand:

- Why choose this approach over the others available?
- What is the plan for supporting additonal user stories and more complex user stories?

If there were good justifications for all the above, I'd likely still push hard to have the result of the "test" script produce an error code greater than 0 if any conditions were not met.  I actually lost the implementation to get_interested_volunteers() at some point and didn't notice even though I was running the included test file regularly.

## Implementing unittest

The included `unit_tests.py` demonstrates what I would consider good testing practice.  Using mocks to narrow the scope of a test to a very small bit of functionality and then creating many well-named test cases.

# Follow up items

The structure of the heap will likely need further refinement, the current notion being that instead of just task_id as the datapoint we will also save a list of volunteers who are interested in that task.

``` python
# (desireability_score, {task_id: [volunteer_ids]})
heap = [
(0.1, {1: [1,2,3]})
]
```

This can be then used to assign tasks to volunteers in a first-pass.
