class Employee:
    """Generic employee class.

    For this module, we're going to remove the inheritance hierarchy
    in `abstract_class` and make all employees have a `direct_reports`
    attribute.

    Notice that if we continue adding employees in the `direct_reports`
    attribute, those same employees have a `direct_reports` attribute
    as well.

    The tree-like structure of this class resembles the Composite design
    pattern, and you can find it on Wikipedia:

    https://en.wikipedia.org/wiki/Composite_pattern
    """

    def __init__(self, name, title, direct_reports):
        self.name = name
        self.title = title
        self.direct_reports = direct_reports

    def __repr__(self):
        return f"<Employee name={self.name}>"


class IterationError(RuntimeError):
    """Any error that comes while iterating through objects.

    Notice that this class inherits from `RuntimeError`. That way dependent
    functions can handle this exception using either the package hierarchy
    or the native hierarchy.
    """


class EmployeeIterator:
    """Employee iterator.

    An iterator class is composed of three methods:

    - A constructor which defines data structures
    - An iterator returns the instance itself
    - A retriever which gets the next element

    We do this by providing what are called magic methods. Other people
    call them d-under methods because they have double-underscores.

    An iterator class resembles the Iterator design pattern, and you
    can find it on Wikipedia:

    https://en.wikipedia.org/wiki/Iterator_pattern

    Design patterns are battle-tested ways of structuring code to handle
    common problems encountered while writing software in a team setting.
    Here's a Wikipedia link for more design patterns:

    https://en.wikipedia.org/wiki/Design_Patterns
    """

    def __init__(self, employee):
        """Constructor logic."""
        self.employees_to_visit = [employee]
        self.employees_visited = set()

    def __iter__(self):
        """Iterator is self by convention."""
        return self

    def __next__(self):
        """Return the next employee available.

        The logic may seem complex, but it's actually a common algorithm
        used in traversing a relationship graph. It is called depth-first
        search and you can find it on Wikipedia:

        https://en.wikipedia.org/wiki/Depth-first_search
        """
        if not self.employees_to_visit:
            raise StopIteration
        employee = self.employees_to_visit.pop()
        if employee.name in self.employees_visited:
            raise IterationError("Cyclic loop detected")
        self.employees_visited.add(employee.name)
        for report in employee.direct_reports:
            self.employees_to_visit.append(report)
        return employee


def employee_generator(top_employee):
    """Employee generator.

    It is essentially the same logic as above except constructed as a
    generator function. Notice that the generator code is in a single
    place, whereas the iterator code is in multiple places. Also notice
    that we are using the `yield` keyword in the generator code.

    It is a matter of preference and context that we choose one approach
    over the other. If we want something simple, go with the generator.
    Otherwise, go with the iterator to fulfill more demanding requirements.
    In this case, examples of such requirements are tasks like encrypting
    the employee's username, running statistics on iterated employees or
    excluding the reports under a particular set of managers.

    For more on the subject of using a function versus a class, check
    out this post from Microsoft Developer Blogs:

    https://devblogs.microsoft.com/python/idiomatic-python-functions-versus-classes/
    """
    to_visit = [top_employee]
    visited = set()
    while len(to_visit) > 0:
        employee = to_visit.pop()
        if employee.name in visited:
            raise IterationError("Cyclic loop detected")
        visited.add(employee.name)
        for report in employee.direct_reports:
            to_visit.append(report)
        yield employee


def main():
    # Manager with two direct reports
    manager = Employee("Max Doe", "Engineering Manager", [
        Employee("John Doe", "Software Engineer", []),
        Employee("Jane Doe", "Software Engineer", [])
    ])

    # We should provide the same three employees in the same order regardless
    # of whether we use the iterator class or the generator function
    employees = [emp for emp in EmployeeIterator(manager)]
    assert employees == [emp for emp in employee_generator(manager)]
    assert len(employees) == 3

    # Make sure that the employees are who we expect them to be
    assert all(isinstance(emp, Employee) for emp in employees)
    print(employees)

    # This is not a good day for this company
    hacker = Employee("Unknown", "Hacker", [])
    hacker.direct_reports.append(hacker)

    for iter_fn in (EmployeeIterator, employee_generator):
        try:
            list(iter_fn(hacker))
        except IterationError as e:
            print(e)


if __name__ == "__main__":
    main()
