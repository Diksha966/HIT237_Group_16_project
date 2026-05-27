### ADR 1 

#### Title : Use Django MTV Architecture

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

### ADR 2 

#### Title: Use ForeignKey Relationships for Model Associations

Status: Accepted

Context:

The project system needs to represent relationships between residents, houses, and maintenance requests. Each maintenance request needs to be linked to a specific resident and a specific house, since a resident always creates a request for a particular house.

Alternatives considered:

One option was to store related data manually using IDs without defining proper relationships. Another option was to use Django’s ForeignKey relationships to connect the models.

Storing IDs manually can lead to errors and make data management more difficult. Using ForeignKey relationships ensures that the connections between models are properly maintained.

Decision:

We decided to use ForeignKey relationships in the MaintenanceRequest model to link it with the Resident and House models. This allows each request to be linked with one resident model and one house model, while still allowing a resident or house to have multiple requests.

Code reference:

models.py (MaintenanceRequest model – resident and house ForeignKey fields) line 50 and 51.

Consequences:

This approach improves data consistency and makes it easier to fetch related data using Django’s ORM. It also makes the system more structured. However, it requires understanding how relational databases work.

### ADR 3

#### Title: Use Class-Based Views for Handling Requests

Status: Superseded by ADR 7

Context:

The designed system needs to support multiple operations, which includes, creating, viewing, updating, and deleting maintenance requests. These operations require structured, reusable logic to keep the code organized.

Alternative Considerations:

One option was to use Function-Based Views, which are simple and easy to write. Another option was to use Class-Based Views, which provide built-in functionality and support code reuse.

Function-Based Views can become repetitive when handling similar operations. Class-Based Views provide a more organized approach and reduce duplication.

Decision:

We decided to use Class-Based Views because they allow us to reuse common functionality and keep the code in a structured way. Django provides built-in views such as ListView, CreateView, UpdateView, and DeleteView, which simplify the implementation of CRUD operations for maintenance requests.

Code reference:

views.py ( Project level- Planned implementation using, ListView, CreateView, UpdateView, DeleteView for MaintenanceRequest)

Consequences:

By using this approach, code duplication and maintainability can be improved. It also makes the system easier to extend in the future. 

### ADR 4

#### Title: Use Django QuerySet API for Data Retrieval

Status: Superseded by ADR 7

Context:

The system needs to retrieve and display maintenance requests in different ways, such as showing all requests, filtering requests by resident, and filtering by status. Efficient data retrieval is important for the system to work properly.

Alternatives considered:

One option was to use raw SQL queries to interact with the database directly. Another option was to use Django’s QuerySet API.

Raw SQL provides more control but can make the code more sophisticated and aeduous to maintain. Django’s QuerySet API provides a simpler and more readable way to interact with the database.

Decision:

Our team ended up using Django’s QuerySet API because it integrates well with Django models and disentangles database operations. It allows us to fetch and filter data using some methods like all() and filter().

Code reference:

views.py ( Project level- Planned use of, MaintenanceRequest queries using all() and filter())

Consequences:

This improves code readability and maintainability. It also lessens the possible pitfall of errors compared to the raw SQL. However, it may be less flexible for very complex queries.

### ADR 5 ###

#### Title: Use Django Built-in Authentication System

Status: Superseded by ADR 8

Context: 

The system requires users to log in so that the residents and housing officers can securely access and manage their maintenance requests. Different users need controlled access to specific system features.

Alternatives considered:

One option was to build a custom authentication system from scratch. Another option was to use Django's built-in authentication system.

Building a custom system would take more time and could introduce security issues. Django's built-in authentication system is already tested and secure.

Decision:

We decided to use Django's built-in authentication system because it provides secure and reliable user management. It includes features such as login, logout, and user authentication, and integrates well with the Django models and views of the project.

Code reference:
views.py ( Planned use of Django Architecture system using, login/logout handling), settings.py (authentication configuration)

Consequences:
This method improves security and also saves development time. It also features safeguards to ensure authentication is handled using a robust system. However, it offers less flexibility compared to building a fully custom solution.

### ADR 6 

#### Title: Use Template Inheritance for UI Structure

Status: Accepted

Context: Our site includes multiple web pages, such as home, login, and request pages, and all shares a similar layout as well. Repeating the same HTML structure on all pages would lead to duplication and make updates a bit difficult.

Alternatives considered: One option was to create separate HTML files for each page, without reusing code. Another option was to use Django’s template inheritance feature.
Creating separate files would result in duplicate code and make maintenance more difficult. Template inheritance allows the reuse of a common layout.

Decision: We decided to use Django template inheritance, with creating a base template that includes common elements such as the header, footer, and navigations. Other templates have also been used to extend this base template, ensuring consistency across all the applications.

Code reference: templates/base.html, templates/home.html

Consequences: This approach reduces code duplication and ensures a consistent user interface. It also makes it easier to update the layout. However, it requires understanding how templates extend from a base file.

### ADR 7

#### Title: Introduce a Service Layer for Business Rules

Status: Accepted

Context:

As the application grew, CRUD logic was becoming mixed directly into class-based views. The team needed a place to centralise validation, relationship checks, and deletion rules so that views stayed thin and business rules were easier to test.

Alternatives considered:

One option was to keep business logic inside the views. Another option was to move the logic into a dedicated service layer.

Keeping the logic in views would make the code harder to test and reuse. A service layer improves separation of concerns and supports explicit exception handling.

Decision:

We introduced housing/services.py and housing/exceptions.py to manage create, update, delete, listing, and summary operations for houses, residents, and maintenance requests. Views now call these service functions and translate service exceptions into form or message feedback.

Code reference:

housing/services.py, housing/exceptions.py, housing/views.py

Consequences:

Business rules such as resident-house consistency and guarded deletion are now reusable and testable. This makes the codebase easier to maintain, but adds a small amount of indirection compared with direct model saves.

### ADR 8

#### Title: Use Django Authentication with Logged-In Permission Boundaries

Status: Accepted

Context:

The extended assignment requires user authentication and permission boundaries. The application needs to distinguish between public browsing and authenticated management actions.

Alternatives considered:

One option was to leave the app public. Another option was to build a custom authentication system. A third option was to use Django's built-in authentication framework with login-required restrictions on write operations.

Leaving the app public would not satisfy the assignment. A custom auth system would add unnecessary security risk and maintenance cost. Django's built-in system is secure and already integrated with the framework.

Decision:

We implemented login, logout, and registration pages using Django's auth system. Create, update, and delete views for houses, residents, and maintenance requests are protected with LoginRequiredMixin, while list and home views remain public.

Code reference:

housing/views.py, housing/urls.py, housing/templates/registration/login.html, housing/templates/registration/register.html, housing_project/settings.py

Consequences:

This provides clear access boundaries and a better user experience, while keeping the authentication implementation straightforward. The trade-off is that the current access model is role-neutral and does not yet differentiate between staff and non-staff users.

### ADR 9

#### Title: Validate Related Objects and Guard Deletions in the Service Layer

Status: Accepted

Context:

The application stores Residents, Houses, and MaintenanceRequests as linked records. If these relationships are edited incorrectly, the data model can become inconsistent or important records can be removed accidentally.

Alternatives considered:

One option was to rely only on form validation. Another option was to enforce relationship checks and deletion rules in the service layer.

Form-only checks would be easier to bypass if the logic is reused in multiple views. Service-level checks ensure the same rule is applied everywhere.

Decision:

We added service-layer validation to ensure that a resident used in a maintenance request belongs to the selected house. We also blocked deleting a house when residents or requests still exist, and blocked deleting a resident when requests still exist.

Code reference:

housing/services.py, housing/views.py, housing/tests.py

Consequences:

This protects the integrity of the data model and prevents accidental data loss. It also creates user-visible validation errors, which are now handled consistently by the views.

### ADR 10

#### Title: Test Behaviour at the Service, View, and Permission Boundaries

Status: Accepted

Context:

The assignment requires a meaningful test suite. The team needed a strategy that proves the architecture works without writing tests that simply mirror implementation details.

Alternatives considered:

One option was to focus only on model tests. Another option was to write tests only for view responses. A third option was to combine service, view, and permission tests that assert user-visible behaviour.

Model-only tests would miss the new architecture. View-only tests would not confirm the service layer is enforcing business rules. A mixed approach gives broader coverage.

Decision:

We wrote tests for service behaviour, public versus protected view access, authenticated create actions, and guarded deletion rules. The tests focus on meaningful outcomes such as rejected invalid relationships, successful record creation, and login redirects.

Code reference:

housing/tests.py, housing/services.py, housing/views.py

Consequences:

The suite verifies the most important business rules and permission boundaries while remaining maintainable. It does not attempt to exhaustively test Django internals or every template detail, because those are already covered by the framework and would add little value.

