# Overview

ArtistConnect is a Flask-based MVP platform that connects event organizers with artists. The application enables artists to create profiles showcasing their skills, demos, and availability, while organizers can browse artists, view their profiles, and send booking requests. Artists can then accept or reject these requests through their dashboard. This is designed as a minimal viable product suitable for demos, college projects, or startup MVPs without payment processing.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework Architecture
The application uses Flask 3 with a modular structure following the application factory pattern. The main components are organized into:

- **Application Factory**: Creates and configures Flask app instances with proper initialization
- **Database Layer**: SQLAlchemy ORM with SQLite for data persistence
- **Template System**: Jinja2 templates with custom filters for content rendering
- **Static Assets**: Custom CSS with a dark theme design system

## Database Design
The application uses SQLite as the primary database with four core models:

- **User Model**: Handles authentication and stores basic user information with role-based access (artist/organizer)
- **ArtistProfile**: Extended profile information for artists including category, location, bio, demo links, and charges
- **OrganizerProfile**: Basic profile extension for organizers with organization details
- **BookingRequest**: Manages the booking workflow with status tracking (pending/accepted/rejected)

The database schema uses foreign key relationships to maintain data integrity and supports the core booking workflow.

## Authentication System
The application implements a simple session-based authentication system:

- Password hashing using Werkzeug's security functions
- Session management for user state persistence
- Role-based access control with decorators
- Login/logout functionality with proper session cleanup

## User Interface Architecture
The frontend uses a component-based template system:

- **Base Template**: Provides consistent navigation and flash messaging
- **Role-Specific Dashboards**: Separate interfaces for artists and organizers
- **Profile Management**: Dedicated pages for viewing and editing artist profiles
- **Booking Flow**: Multi-step process for creating and managing booking requests

The CSS framework uses CSS custom properties for theming and follows a utility-first approach similar to Tailwind CSS.

## Data Flow Pattern
The application follows a traditional MVC pattern:

1. Routes handle HTTP requests and form processing
2. Models manage data persistence and business logic
3. Templates render dynamic content with proper data binding
4. Flash messaging provides user feedback across redirects

## Security Considerations
- Password hashing for secure credential storage
- Session-based authentication with role verification
- CSRF protection through Flask's built-in mechanisms
- Input validation and sanitization in forms

# External Dependencies

## Core Framework Dependencies
- **Flask 3.0.3**: Main web framework providing routing, templating, and request handling
- **Flask-SQLAlchemy 3.1.1**: Database ORM integration for Flask applications
- **Flask-Migrate 4.0.7**: Database migration support for schema changes
- **Werkzeug 3.0.4**: WSGI utility library providing security and utilities

## Utility Libraries
- **python-dotenv 1.0.1**: Environment variable management for configuration
- **email-validator 2.2.0**: Email address validation for user registration

## Database
- **SQLite**: Embedded database solution requiring no external setup
- Database file stored locally as `artistconnect.db` in the project root

## Development Tools
The application is designed to run in development mode with:
- Built-in Flask development server
- Debug mode enabled for development
- Hot reloading for template and code changes

## Hosting Requirements
- Python 3.7+ environment
- File system access for SQLite database
- Static file serving capability
- No external database or service dependencies required