###Title: Use Django MTV Architecture###

Status: Accepted

##Context:##
The system requires a clear structure to separate data, logic, and user interface for better maintainability and scalability.

Alternatives considered:

A monolithic structure without clear separation
Django MTV (Model–Template–View) architecture

The monolithic approach would make the system harder to maintain and scale, while Django MTV provides a structured way to organise the application.

Decision:
We chose Django’s MTV architecture because it separates concerns effectively. Models manage the data, views handle the business logic, and templates manage the user interface.

Code reference:
models.py, views.py, templates/

Consequences:

Improved code organisation
Easier debugging and maintenance
Slight learning curve for beginners
