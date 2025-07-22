# Minutes of Meeting (MOM) Module

## Overview

The Minutes of Meeting (MOM) module is a comprehensive Odoo application designed to facilitate the creation, management, and tracking of meeting minutes with a structured workflow and detailed action item management.

## What is MOM?

**Minutes of Meeting (MOM)** is a formal written record of what transpired during a meeting. It serves as an official document that captures:
- Key discussions and decisions made
- Action items and responsibilities assigned
- Deadlines and target dates
- Attendees and their roles
- Follow-up requirements

MOM ensures accountability, provides a reference for future actions, and helps track progress on meeting outcomes.

## Module Structure

### Main Models

1. **mom.format.base** - The main meeting record containing:
   - Meeting reference (auto-generated)
   - Meeting title, date, and type
   - Project and customer information
   - Attendees and conductor details
   - Overall meeting status and remarks
   - State history tracking

2. **mom.format.line** - Individual action items within a meeting:
   - Open points and action items
   - Responsibility assignments
   - Target and completion dates
   - Individual status tracking
   - Detailed remarks

3. **mom.open.point** - Master data for open point types:
   - Categorized templates (Action Items, Decisions, Issues, Risks, Follow-ups)
   - Priority levels (Low, Medium, High, Critical)
   - Usage statistics

## Key Features

### Meeting Management
- **Structured Meeting Records**: Create comprehensive meeting minutes with all essential details
- **Auto-generated References**: Unique meeting references generated automatically
- **Meeting Types**: Categorize meetings (Regular, Review, Planning, Emergency, Other)
- **Project Association**: Link meetings to specific projects and customers

### Action Item Management (One2Many Relationship)
- **Multiple Action Items**: Add unlimited action items per meeting
- **Sequential Ordering**: Drag-and-drop reordering with automatic serial numbering
- **Individual Tracking**: Each action item has its own status and completion tracking
- **Responsibility Matrix**: Assign different responsibilities for each action item
- **Inherited Defaults**: Action items automatically inherit attendees and conductor from the main meeting

### Workflow Management
- **Dual-Level Workflows**: 
  - Meeting level: Draft → In Progress → Completed → Approved
  - Action item level: Individual status tracking for each line
- **State History**: Complete audit trail with timestamps and user tracking
- **Validation Rules**: Built-in checks for required fields and state transitions

### Advanced Features
- **Bulk Operations**: Manage multiple action items efficiently
- **Smart Defaults**: Automatic data population based on context
- **Search & Filters**: Advanced search capabilities with grouping options
- **Security**: Role-based access control

## Installation

1. Copy the `mom` folder to your Odoo addons directory:
   ```
   C:\odoo\odoo16\custom-addons\mom
   ```
2. Update the apps list in Odoo
3. Install the "Minutes of Meeting (MOM)" module from the Apps menu

## Dependencies

- **mail**: For email integration and activity tracking
- **hr**: For employee management and attendee selection

## Usage Guide

### Creating a Meeting

1. **Navigate**: Minutes of Meeting → MOM → Minutes of Meeting
2. **Create**: Click "Create" to start a new meeting record
3. **Fill Basic Information**:
   - Meeting title (required)
   - Meeting date and type
   - Project name and customer (optional)
   - Attendees and conductor

### Adding Action Items

1. **MOM Lines Tab**: Click on the "MOM Lines" tab in the meeting form
2. **Add Items**: Click "Add a line" to create action items
3. **For Each Action Item**:
   - Select open point type
   - Assign responsibility
   - Set target date
   - Add remarks if needed
4. **Reorder**: Use the handle icon to drag and reorder items

### Managing Workflows

#### Meeting Level States:
- **Draft**: Initial state for planning
- **In Progress**: Meeting is active
- **Completed**: All discussions finalized
- **Approved**: Formally approved by authority
- **Cancelled**: Meeting cancelled

#### Action Item States:
- **Draft**: Item identified but not started
- **In Progress**: Work has begun
- **Completed**: Task finished (requires actual completion date)
- **Approved**: Item formally closed
- **Cancelled**: Item no longer relevant

### Configuration

1. **Open Points Setup**:
   - Navigate to Configuration → Open Points
   - Create templates for common action items
   - Set categories and priorities

2. **MOM Lines View**:
   - Access all action items across meetings
   - Configuration → MOM Lines
   - Filter by status, responsibility, or dates

## Best Practices

1. **Meeting Preparation**:
   - Create the MOM record before the meeting
   - Add known attendees in advance
   - Prepare open point templates

2. **During Meeting**:
   - Add action items in real-time
   - Assign clear responsibilities
   - Set realistic target dates

3. **Post-Meeting**:
   - Review and finalize all action items
   - Send for approval when complete
   - Track progress regularly

## Security & Access Control

- **Regular Users**: Full CRUD access to MOM records and lines
- **Managers**: Additional configuration privileges
- **Read-Only**: View access for stakeholders

## Technical Details

### Models:
- `mom.format.base` - Main meeting model
- `mom.format.line` - Action items (One2Many relation)
- `mom.open.point` - Master data for open points

### Key Fields:
- Auto-sequence generation for meeting references
- Many2Many relationships for attendees
- One2Many relationship for action items
- Computed fields for serial numbering

## License

This module is released under the LGPL-3 License.
