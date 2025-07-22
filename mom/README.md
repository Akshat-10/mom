# Minutes of Meeting (MOM) Module

## Overview

The Minutes of Meeting (MOM) module is a standalone Odoo application for managing meeting minutes with comprehensive tracking and approval workflows.

## Features

### Core Functionality

- **Meeting Management**: Create and manage meeting minutes with detailed information
- **Open Points Tracking**: Track action items, decisions, issues, and risks
- **Responsibility Assignment**: Assign suppliers/partners as responsible parties
- **Date Tracking**: Monitor target dates and actual completion dates
- **Approval Workflow**: Structured workflow (Draft → In Progress → Completed → Approved)
- **State History**: Complete audit trail of all state changes

### Meeting Information

- Meeting title and reference number (auto-generated)
- Meeting date, type, and location
- Project name and customer association
- Duration tracking and next meeting scheduling
- Rich text meeting notes

### Attendee Management

- Multiple attendees selection from employees
- Meeting conductor/champion designation
- Easy attendee management with avatar display

### Open Points

- Categorized open points (Action Items, Decisions, Issues, Risks, Follow-ups)
- Priority levels (Low, Medium, High, Critical)
- Reusable open point templates
- Statistics on open point usage across meetings

### Search and Filtering

- Advanced search capabilities
- Filter by state, responsibility, dates
- Group by various criteria
- Personal records view ("My Records")
- Late items tracking

## Installation

1. Copy the `mom` folder to your Odoo addons directory
2. Update the addons list in Odoo
3. Install the "Minutes of Meeting (MOM)" module

## Dependencies

- mail
- hr

## Usage

### Creating a Meeting

1. Navigate to Minutes of Meeting → MOM → Minutes of Meeting
2. Click "Create" to start a new meeting record
3. Fill in meeting details:
   - Meeting title
   - Meeting date and type
   - Project name and customer (optional)
   - Meeting location and duration
4. Select open point and assign responsibility
5. Set target completion date
6. Add attendees and meeting conductor
7. Save the record

### Managing Meeting States

- **Draft**: Initial state for new meetings
- **In Progress**: Meeting actions are being worked on
- **Completed**: All actions completed (requires actual completion date)
- **Approved**: Meeting formally approved
- **Cancelled**: Meeting cancelled

### Open Points Configuration

1. Navigate to Configuration → Open Points
2. Create reusable open point templates
3. Categorize and prioritize for better organization
4. View statistics on usage across meetings

## Security

- Regular users can create, read, update, and delete MOM records
- System administrators have full access to all configurations
- Open points are read-only for regular users

## License

LGPL-3
