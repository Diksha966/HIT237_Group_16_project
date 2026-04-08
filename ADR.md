ADR 1 
Title: Use Django MTV Architecture
Status: Accepted
Context:
 For this project, we needed a clear way to organize the application so that the data, logic, and user interface in our project are separated. Since the system involves managing residents, houses, and maintenance requests, having a structured approach is important to keep the project manageable and easy to understand.
Alternatives considered:
 One option was to build the system without a clear structure, with everything handled in a single place. Another option was to follow Django’s Model–View–Template (MVT) architecture.
The first option would make the project harder to maintain and more confusing as it approaches more. The MTV approach provides a clear separation between different parts of the system.
Decision:
 We decided to use Django’s MTV architecture because it helps organize the application effectively. The models in models.py manage the data ( Resident, House, and MaintenanceRequest), the views handle the application logic, and the templates provide the user interface. This makes the system easier to manage and develop.
Code reference:
 models.py (Resident, House, MaintenanceRequest models), views.py, templates/
Consequences:
 This approach makes the code more organized and easier to maintain. This helps team members to work on different parts of the system. However, it may be a bit difficult to connect everything at first.

ADR 2
Title: Use ForeignKey Relationships for Model Associations
Status: Accepted
Context:
The project system needs to represent relationships between residents, houses, and maintenance requests. Each maintenance request needs to be linked to a specific resident and a specific house, since a resident always creates a request for a particular house.
Alternatives considered:
 One option was to store related data manually using IDs without defining proper relationships. Another option was to use Django’s ForeignKey relationships to connect the models.
Storing IDs manually can lead to errors and make data management more difficult. Using ForeignKey relationships ensures that the connections between models are properly maintained.
Decision:
 We decided to use ForeignKey relationships in the MaintenanceRequest model to link it with the Resident and House models. This allows each request to be linked with one resident model and one house model, while still allowing a resident or house to have multiple requests.
Code reference:
 models.py (MaintenanceRequest model – resident and house ForeignKey fields)
Consequences:
 This approach improves data consistency and makes it easier to fetch related data using Django’s ORM. It also makes the system more structured. However, it requires understanding how relational databases work.

ADR 3
Title: Use Class-Based Views for Handling Requests
Status: Accepted
Context:
The designed system needs to support multiple operations, which includes, creating, viewing, updating, and deleting maintenance requests. These operations require structured, reusable logic to keep the code organized.
Alternative Considerations:
 One option was to use Function-Based Views, which are simple and easy to write. Another option was to use Class-Based Views, which provide built-in functionality and support code reuse.
Function-Based Views can become repetitive when handling similar operations. Class-Based Views provide a more organized approach and reduce duplication.
Decision:
 We decided to use Class-Based Views because they allow us to reuse common functionality and keep the code in a structured way. Django provides built-in views such as ListView, CreateView, UpdateView, and DeleteView, which simplify the implementation of CRUD operations for maintenance requests.
Code reference:
 views.py (ListView, CreateView, UpdateView, DeleteView for MaintenanceRequest)
Consequences:
By using this approach, code duplication and maintainability can be improved. It also makes the system easier to extend in the future. 
