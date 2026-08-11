# CRM Database Schema

## Overview
This document describes the database schema for the CRM system. The system uses PostgreSQL with SQLAlchemy ORM.

## Entity Relationship Diagram

```
organizations (1) ----< (N) users
organizations (1) ----< (N) companies
organizations (1) ----< (N) leads
organizations (1) ----< (N) contacts
organizations (1) ----< (N) deals
organizations (1) ----< (N) activities
organizations (1) ----< (N) products

users (1) ----< (N) leads (assigned_to)
users (1) ----< (N) contacts (created_by)
users (1) ----< (N) deals (assigned_to)
users (1) ----< (N) activities (created_by)

companies (1) ----< (N) contacts
companies (1) ----< (N) deals

contacts (1) ----< (N) leads
contacts (1) ----< (N) activities
contacts (1) ----< (N) deals

leads (1) ----< (N) activities
deals (1) ----< (N) activities
```

## Tables

### organizations
Multi-tenant organization management.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| name | String | Organization name |
| slug | String (Unique) | URL-friendly identifier |
| industry | String | Industry type |
| website | String | Organization website |
| logo_url | String | Logo image URL |
| address | Text | Physical address |
| phone | String | Contact phone |
| settings | Text (JSON) | Custom organization settings |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### users
User accounts with role-based access control.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| email | String (Unique) | User email |
| full_name | String | Full name |
| hashed_password | String | Bcrypt hashed password |
| phone | String | Phone number |
| role | Enum | Role (admin, manager, sales_rep, executive, owner, investor) |
| is_active | Boolean | Account status |
| is_verified | Boolean | Email verification status |
| avatar_url | String | Profile image URL |
| organization_id | String (FK) | Belongs to organization |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### companies
Customer companies/accounts.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| name | String | Company name |
| website | String | Company website |
| industry | String | Industry type |
| size | String | Company size (e.g., "1-10", "11-50") |
| address | Text | Physical address |
| city | String | City |
| state | String | State/Province |
| country | String | Country |
| postal_code | String | Postal/ZIP code |
| phone | String | Phone number |
| email | String | General email |
| notes | Text | Additional notes |
| tags | Text (JSON) | Tags array |
| logo_url | String | Company logo URL |
| organization_id | String (FK) | Belongs to organization |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### contacts
Individual contacts at customer companies.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| first_name | String | First name |
| last_name | String | Last name |
| email | String | Email address |
| phone | String | Phone number |
| mobile | String | Mobile number |
| job_title | String | Job title |
| department | String | Department |
| linkedin | String | LinkedIn profile URL |
| twitter | String | Twitter profile URL |
| notes | Text | Additional notes |
| tags | Text (JSON) | Tags array |
| avatar_url | String | Profile image URL |
| organization_id | String (FK) | Belongs to organization |
| company_id | String (FK) | Works at company |
| created_by_id | String (FK) | Created by user |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### leads
Potential customers in the sales pipeline.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| first_name | String | First name |
| last_name | String | Last name |
| email | String | Email address |
| phone | String | Phone number |
| company | String | Company name |
| job_title | String | Job title |
| status | Enum | Status (new, contacted, qualified, proposal, negotiation, won, lost) |
| source | Enum | Source (website, referral, cold_call, cold_email, social_media, event, partner, other) |
| estimated_value | Float | Estimated deal value |
| probability | Integer | Win probability (0-100) |
| notes | Text | Additional notes |
| tags | Text (JSON) | Tags array |
| organization_id | String (FK) | Belongs to organization |
| assigned_to_id | String (FK) | Assigned to user |
| contact_id | String (FK) | Linked to contact |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### deals
Sales opportunities/deals.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| name | String | Deal name |
| description | Text | Deal description |
| value | Float | Deal value |
| currency | String | Currency code (default: USD) |
| probability | Integer | Win probability (0-100) |
| expected_close_date | Date | Expected close date |
| actual_close_date | Date | Actual close date |
| stage | Enum | Stage (prospecting, qualification, proposal, negotiation, won, lost) |
| lost_reason | Text | Reason if lost |
| notes | Text | Additional notes |
| tags | Text (JSON) | Tags array |
| organization_id | String (FK) | Belongs to organization |
| company_id | String (FK) | Associated company |
| assigned_to_id | String (FK) | Assigned to user |
| contact_id | String (FK) | Primary contact |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### activities
Sales activities (calls, emails, meetings, notes, tasks).

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| type | Enum | Type (call, email, meeting, note, task, sms, other) |
| status | Enum | Status (scheduled, completed, cancelled, no_show) |
| subject | String | Activity subject |
| description | Text | Activity description |
| location | String | Location (for meetings) |
| scheduled_at | Timestamp | Scheduled time |
| duration_minutes | Integer | Duration in minutes |
| completed_at | Timestamp | Completion time |
| reminder_minutes_before | Integer | Reminder time before activity |
| reminder_sent | Boolean | Reminder sent status |
| notes | Text | Additional notes |
| organization_id | String (FK) | Belongs to organization |
| created_by_id | String (FK) | Created by user |
| lead_id | String (FK) | Related lead |
| contact_id | String (FK) | Related contact |
| deal_id | String (FK) | Related deal |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

### products
Products and services catalog.

| Column | Type | Description |
|--------|------|-------------|
| id | String (PK) | Unique identifier |
| name | String | Product name |
| description | Text | Product description |
| sku | String (Unique) | Stock keeping unit |
| type | Enum | Type (product, service, subscription, maintenance, other) |
| price | Float | Unit price |
| currency | String | Currency code (default: USD) |
| quantity_in_stock | Integer | Stock quantity |
| low_stock_threshold | Integer | Low stock alert threshold |
| notes | Text | Additional notes |
| tags | Text (JSON) | Tags array |
| is_active | Boolean | Active status |
| organization_id | String (FK) | Belongs to organization |
| created_at | Timestamp | Creation timestamp |
| updated_at | Timestamp | Last update timestamp |

## Enums

### UserRole
- admin
- manager
- sales_rep
- executive
- owner
- investor

### LeadStatus
- new
- contacted
- qualified
- proposal
- negotiation
- won
- lost

### LeadSource
- website
- referral
- cold_call
- cold_email
- social_media
- event
- partner
- other

### DealStage
- prospecting
- qualification
- proposal
- negotiation
- won
- lost

### ActivityType
- call
- email
- meeting
- note
- task
- sms
- other

### ActivityStatus
- scheduled
- completed
- cancelled
- no_show

### ProductType
- product
- service
- subscription
- maintenance
- other

## Indexes

All tables have indexes on:
- Primary keys (id)
- Foreign keys
- Frequently queried fields (email, status, stage, type, etc.)

## Notes

1. **Multi-tenancy**: All data is scoped to an organization using `organization_id`
2. **Soft deletes**: Not implemented initially, can be added later
3. **Timestamps**: All tables have `created_at` and `updated_at`
4. **JSON fields**: Tags and settings are stored as JSON strings for flexibility
5. **UUIDs**: All IDs are UUID strings for distributed system compatibility
