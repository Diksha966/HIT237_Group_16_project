# HIT237 Group 16 Project

Django-based housing maintenance system for HIT237.

## What is included
- Houses, residents, and maintenance requests
- Authentication with login, logout, and registration
- Service-layer architecture for business rules and validation
- Guarded delete rules and relationship checks
- Meaningful tests for services, views, and permissions

## Running the project
1. Install dependencies from requirements.txt.
2. Run migrations.
3. Start the development server.
4. Open the local site in a browser.

## Key URLs
- Home: /
- Houses: /houses/
- Requests: /requests/
- Residents: /residents/
- Login: /accounts/login/
- Register: /accounts/register/

## Architecture notes
- Models define the data structure.
- Services contain validation and business operations.
- Views focus on request handling and permissions.
- Templates handle presentation.

## Supplementary materials
- ADR.md
- PROJECT-PLAN-Group-16.md
- GROUP-CONTRACT-Group-16.md
- docs/erd.md
- docs/class-diagram.md
