# HIT237 Group 16 Project Plan

## Project scope
Extend the Django housing maintenance application with authentication, a service layer, exception handling, and a meaningful test suite.

## Delivery phases

### Phase 1: Stabilise the application
- Review the existing models, views, and templates
- Repair broken templates and missing delete pages
- Confirm the app runs end to end

### Phase 2: Authentication and access control
- Add login, logout, and registration
- Protect create, update, and delete actions with login requirements
- Update navigation and templates to reflect signed-in users

### Phase 3: Service layer and exception handling
- Move CRUD and validation logic into housing/services.py
- Add custom service exceptions
- Enforce relationship validation and guarded deletes

### Phase 4: Testing and documentation
- Write service tests for business rules
- Write view tests for permission boundaries
- Update ADR entries, README, project plan, and contract
- Prepare supplementary diagrams

## Current task allocation
- Authentication and UI updates: Armaan, Achintha
- Service layer and validation: Chetanya, Diksha
- Testing and documentation: All members

## Acceptance criteria
- Authenticated users can manage records
- Invalid house/resident combinations are rejected
- Deleting records with dependencies is blocked
- Tests cover meaningful behaviour and permissions
- ADR explains each architectural decision and supersession
