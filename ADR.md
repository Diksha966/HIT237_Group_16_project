#### ADR 1 #### 

### Title :### Use Django MTV Architecture

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

#### ADR 2 ####

### Title: Use ForeignKey Relationships for Model Associations

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

#### ADR 3###

### Title: Use Class-Based Views for Handling Requests

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

#### ADR 4##

### Title: Use Django QuerySet API for Data Retrieval

Status: Accepted

Context:

The system needs to retrieve and display maintenance requests in different ways, such as showing all requests, filtering requests by resident, and filtering by status. Efficient data retrieval is important for the system to work properly.

Alternatives considered:

One option was to use raw SQL queries to interact with the database directly. Another option was to use Django’s QuerySet API.

Raw SQL provides more control but can make the code more sophisticated and aeduous to maintain. Django’s QuerySet API provides a simpler and more readable way to interact with the database.

Decision:

Our team ended up using Django’s QuerySet API because it integrates well with Django models and disentangles database operations. It allows us to fetch and filter data using some methods like all() and filter().

Code reference:

views.py (MaintenanceRequest queries using all() and filter())

Consequences:

This improves code readability and maintainability. It also lessens the possible pitfall of errors compared to the raw SQL. However, it may be less flexible for very complex queries.

#### ARD 5 ###

### Title: Use Django Built-in Authentication System

Status: Accepted

Context: 

The system requires users to log in so that the residents and housing officers can securely access and manage their maintenance requests. Different users need controlled access to specific system features.

Alternatives considered:

One option was to build a custom authentication system from scratch. Another option was to use Django's built-in authentication system.

Building a custom system would take more time and could introduce security issues. Django's built-in authentication system is already tested and secure.

Decision:

We decided to use Django's built-in authentication system because it provides secure and reliable user management. It includes features such as login, logout, and user authentication, and integrates well with the Django models and views of the project.

Code reference:
views.py (login/logout handling), settings.py (authentication configuration)

Consequences:
This method improves security and also saves development time. It also features safeguards to ensure authentication is handled using a robust system. However, it offers less flexibility compared to building a fully custom solution.

#### ADR 6 ###

### Title: Use Template Inheritance for UI Structure

Status: Accepted

Context: Our site includes multiple web pages, such as home, login, and request pages, and all shares a similar layout as well. Repeating the same HTML structure on all pages would lead to duplication and make updates a bit difficult.

Alternatives considered: One option was to create separate HTML files for each page, without reusing code. Another option was to use Django’s template inheritance feature.
Creating separate files would result in duplicate code and make maintenance more difficult. Template inheritance allows the reuse of a common layout.

Decision: We decided to use Django template inheritance, with creating a base template that includes common elements such as the header, footer, and navigations. Other templates have also been used to extend this base template, ensuring consistency across all the applications.

Code reference: templates/base.html, templates/*.html

Consequences: This approach reduces code duplication and ensures a consistent user interface. It also makes it easier to update the layout. However, it requires understanding how templates extend from a base file.

