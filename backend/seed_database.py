"""
Database Seeding Script
Populates the database with sample data for demo purposes
"""

import sys
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add parent directory to path for imports
sys.path.insert(0, '/Users/samikshalad/Documents/Mrityunjay Lad/MJ CRM/backend')

from app.core.database import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.lead import Lead, LeadStatus, LeadSource
from app.models.contact import Contact
from app.models.company import Company
from app.models.deal import Deal, DealStage
from app.models.activity import Activity, ActivityType, ActivityStatus
from app.models.product import Product, ProductType


def seed_database():
    """Seed the database with sample data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Check if demo data already exists
        existing_user = db.query(User).filter(User.email == "demo@mjcrm.com").first()
        if existing_user:
            print("Demo data already exists. Skipping seeding.")
            return
        
        # Create Organization
        org_id = str(uuid.uuid4())
        organization = Organization(
            id=org_id,
            name="MJ CRM Demo",
            slug="mj-crm-demo",
            industry="Technology",
            website="https://mjcrm.demo",
            address="123 Demo Street, Tech City",
            phone="+1-555-0123"
        )
        db.add(organization)
        db.flush()
        print(f"✓ Created organization: {organization.name}")
        
        # Create Demo User
        demo_password = "demo123"  # Known password for demo
        demo_user = User(
            id=str(uuid.uuid4()),
            email="demo@mjcrm.com",
            full_name="Demo User",
            hashed_password=get_password_hash(demo_password),
            phone="+1-555-0124",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            organization_id=org_id
        )
        db.add(demo_user)
        db.flush()
        print(f"✓ Created demo user: {demo_user.email} (password: {demo_password})")
        
        # Create Companies
        companies_data = [
            {
                "name": "TechCorp Inc.",
                "website": "https://techcorp.com",
                "industry": "Technology",
                "size": "500-1000",
                "address": "456 Tech Avenue, Silicon Valley, CA",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "phone": "+1-555-0100"
            },
            {
                "name": "Global Solutions Ltd",
                "website": "https://globalsolutions.com",
                "industry": "Consulting",
                "size": "100-500",
                "address": "789 Business Park, London",
                "city": "London",
                "state": "England",
                "country": "UK",
                "phone": "+44-20-1234-5678"
            },
            {
                "name": "Startup Ventures",
                "website": "https://startupventures.io",
                "industry": "Software",
                "size": "10-50",
                "address": "321 Innovation Drive, Austin, TX",
                "city": "Austin",
                "state": "TX",
                "country": "USA",
                "phone": "+1-555-0200"
            }
        ]
        
        companies = []
        for company_data in companies_data:
            company = Company(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                **company_data
            )
            db.add(company)
            companies.append(company)
        db.flush()
        print(f"✓ Created {len(companies)} companies")
        
        # Create Contacts
        contacts_data = [
            {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@techcorp.com",
                "phone": "+1-555-0101",
                "mobile": "+1-555-0102",
                "job_title": "CTO",
                "department": "Engineering",
                "company_id": companies[0].id,
                "linkedin": "linkedin.com/in/johnsmith",
                "notes": "Key decision maker for technology purchases"
            },
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@globalsolutions.com",
                "phone": "+44-20-1234-5679",
                "mobile": "+44-7700-900123",
                "job_title": "CEO",
                "department": "Executive",
                "company_id": companies[1].id,
                "linkedin": "linkedin.com/in/sarahjohnson",
                "notes": "Interested in enterprise solutions"
            },
            {
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael.chen@startupventures.io",
                "phone": "+1-555-0201",
                "mobile": "+1-555-0202",
                "job_title": "Founder",
                "department": "Management",
                "company_id": companies[2].id,
                "linkedin": "linkedin.com/in/michaelchen",
                "notes": "Early-stage startup, budget conscious"
            }
        ]
        
        contacts = []
        for contact_data in contacts_data:
            contact = Contact(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                created_by_id=demo_user.id,
                **contact_data
            )
            db.add(contact)
            contacts.append(contact)
        db.flush()
        print(f"✓ Created {len(contacts)} contacts")
        
        # Create Leads
        leads_data = [
            {
                "first_name": "Emily",
                "last_name": "Davis",
                "email": "emily.davis@innovateco.com",
                "phone": "+1-555-0300",
                "company": "InnovateCo",
                "job_title": "VP of Sales",
                "status": LeadStatus.QUALIFIED,
                "source": LeadSource.WEBSITE,
                "estimated_value": 50000.0,
                "probability": 70,
                "contact_id": contacts[0].id,
                "notes": "Expressed interest in premium package"
            },
            {
                "first_name": "Robert",
                "last_name": "Wilson",
                "email": "robert.wilson@enterprise.net",
                "phone": "+1-555-0301",
                "company": "Enterprise Net",
                "job_title": "Director of Operations",
                "status": LeadStatus.CONTACTED,
                "source": LeadSource.REFERRAL,
                "estimated_value": 75000.0,
                "probability": 50,
                "notes": "Referred by existing customer"
            },
            {
                "first_name": "Lisa",
                "last_name": "Anderson",
                "email": "lisa.anderson@growthmetrics.com",
                "phone": "+1-555-0302",
                "company": "Growth Metrics",
                "job_title": "CEO",
                "status": LeadStatus.NEW,
                "source": LeadSource.SOCIAL_MEDIA,
                "estimated_value": 100000.0,
                "probability": 30,
                "notes": "Cold outreach, follow up next week"
            },
            {
                "first_name": "David",
                "last_name": "Brown",
                "email": "david.brown@techstart.io",
                "phone": "+1-555-0303",
                "company": "TechStart IO",
                "job_title": "CTO",
                "status": LeadStatus.PROPOSAL,
                "source": LeadSource.WEBSITE,
                "estimated_value": 45000.0,
                "probability": 80,
                "contact_id": contacts[1].id,
                "notes": "Proposal sent, awaiting feedback"
            },
            {
                "first_name": "Jennifer",
                "last_name": "Taylor",
                "email": "jennifer.taylor@cloudscale.com",
                "phone": "+1-555-0304",
                "company": "CloudScale",
                "job_title": "VP of Engineering",
                "status": LeadStatus.NEGOTIATION,
                "source": LeadSource.EVENT,
                "estimated_value": 120000.0,
                "probability": 90,
                "contact_id": contacts[2].id,
                "notes": "Finalizing contract terms"
            }
        ]
        
        leads = []
        for lead_data in leads_data:
            lead = Lead(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                assigned_to_id=demo_user.id,
                **lead_data
            )
            db.add(lead)
            leads.append(lead)
        db.flush()
        print(f"✓ Created {len(leads)} leads")
        
        # Create Deals
        deals_data = [
            {
                "name": "TechCorp Enterprise License",
                "description": "Annual enterprise license for TechCorp",
                "value": 50000.0,
                "currency": "USD",
                "probability": 80,
                "expected_close_date": datetime.now() + timedelta(days=30),
                "stage": DealStage.PROPOSAL,
                "company_id": companies[0].id,
                "assigned_to_id": demo_user.id,
                "contact_id": contacts[0].id
            },
            {
                "name": "Global Solutions Consulting",
                "description": "Consulting services for Global Solutions",
                "value": 75000.0,
                "currency": "USD",
                "probability": 60,
                "expected_close_date": datetime.now() + timedelta(days=45),
                "stage": DealStage.NEGOTIATION,
                "company_id": companies[1].id,
                "assigned_to_id": demo_user.id,
                "contact_id": contacts[1].id
            },
            {
                "name": "Startup Ventures MVP",
                "description": "MVP development for Startup Ventures",
                "value": 25000.0,
                "currency": "USD",
                "probability": 90,
                "expected_close_date": datetime.now() + timedelta(days=15),
                "stage": DealStage.WON,
                "company_id": companies[2].id,
                "assigned_to_id": demo_user.id,
                "contact_id": contacts[2].id,
                "actual_close_date": datetime.now() - timedelta(days=5)
            }
        ]
        
        deals = []
        for deal_data in deals_data:
            deal = Deal(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                **deal_data
            )
            db.add(deal)
            deals.append(deal)
        db.flush()
        print(f"✓ Created {len(deals)} deals")
        
        # Create Activities
        activities_data = [
            {
                "type": ActivityType.CALL,
                "status": ActivityStatus.COMPLETED,
                "subject": "Initial discovery call with John Smith",
                "description": "Discussed their current pain points and requirements",
                "scheduled_at": datetime.now() - timedelta(days=7),
                "completed_at": datetime.now() - timedelta(days=7),
                "duration_minutes": 30,
                "lead_id": leads[0].id,
                "contact_id": contacts[0].id,
                "created_by_id": demo_user.id
            },
            {
                "type": ActivityType.MEETING,
                "status": ActivityStatus.SCHEDULED,
                "subject": "Product demo for Sarah Johnson",
                "description": "Schedule a comprehensive product demonstration",
                "scheduled_at": datetime.now() + timedelta(days=3),
                "duration_minutes": 60,
                "lead_id": leads[1].id,
                "contact_id": contacts[1].id,
                "created_by_id": demo_user.id,
                "reminder_minutes_before": 60
            },
            {
                "type": ActivityType.EMAIL,
                "status": ActivityStatus.COMPLETED,
                "subject": "Follow-up email to Michael Chen",
                "description": "Sent pricing information and case studies",
                "scheduled_at": datetime.now() - timedelta(days=2),
                "completed_at": datetime.now() - timedelta(days=2),
                "lead_id": leads[2].id,
                "contact_id": contacts[2].id,
                "created_by_id": demo_user.id
            },
            {
                "type": ActivityType.CALL,
                "status": ActivityStatus.SCHEDULED,
                "subject": "Contract review with David Brown",
                "description": "Review contract terms and answer questions",
                "scheduled_at": datetime.now() + timedelta(days=1),
                "duration_minutes": 45,
                "deal_id": deals[0].id,
                "contact_id": contacts[0].id,
                "created_by_id": demo_user.id,
                "reminder_minutes_before": 30
            },
            {
                "type": ActivityType.MEETING,
                "status": ActivityStatus.COMPLETED,
                "subject": "Final negotiation with Jennifer Taylor",
                "description": "Finalized contract terms and signed agreement",
                "scheduled_at": datetime.now() - timedelta(days=1),
                "completed_at": datetime.now() - timedelta(days=1),
                "duration_minutes": 90,
                "deal_id": deals[2].id,
                "contact_id": contacts[2].id,
                "created_by_id": demo_user.id
            }
        ]
        
        for activity_data in activities_data:
            activity = Activity(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                **activity_data
            )
            db.add(activity)
        db.flush()
        print(f"✓ Created {len(activities_data)} activities")
        
        # Create Products
        products_data = [
            {
                "name": "CRM Basic",
                "description": "Essential CRM features for small teams",
                "sku": "CRM-BASIC-001",
                "type": ProductType.SERVICE,
                "price": 29.0,
                "currency": "USD",
                "quantity_in_stock": 9999,
                "low_stock_threshold": 100,
                "is_active": True,
                "notes": "Monthly subscription per user"
            },
            {
                "name": "CRM Professional",
                "description": "Advanced CRM features with analytics",
                "sku": "CRM-PRO-002",
                "type": ProductType.SERVICE,
                "price": 79.0,
                "currency": "USD",
                "quantity_in_stock": 9999,
                "low_stock_threshold": 100,
                "is_active": True,
                "notes": "Monthly subscription per user"
            },
            {
                "name": "CRM Enterprise",
                "description": "Full-featured CRM with custom integrations",
                "sku": "CRM-ENT-003",
                "type": ProductType.SERVICE,
                "price": 199.0,
                "currency": "USD",
                "quantity_in_stock": 9999,
                "low_stock_threshold": 50,
                "is_active": True,
                "notes": "Monthly subscription per user, includes dedicated support"
            },
            {
                "name": "Onboarding Package",
                "description": "Professional onboarding and training",
                "sku": "SRV-ONBOARD-001",
                "type": ProductType.SERVICE,
                "price": 500.0,
                "currency": "USD",
                "quantity_in_stock": 100,
                "low_stock_threshold": 10,
                "is_active": True,
                "notes": "One-time fee"
            },
            {
                "name": "Data Migration Service",
                "description": "Complete data migration from legacy systems",
                "sku": "SRV-MIGRATION-001",
                "type": ProductType.SERVICE,
                "price": 1500.0,
                "currency": "USD",
                "quantity_in_stock": 50,
                "low_stock_threshold": 5,
                "is_active": True,
                "notes": "One-time fee, custom pricing based on data volume"
            }
        ]
        
        for product_data in products_data:
            product = Product(
                id=str(uuid.uuid4()),
                organization_id=org_id,
                **product_data
            )
            db.add(product)
        db.flush()
        print(f"✓ Created {len(products_data)} products")
        
        # Commit all changes
        db.commit()
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print(f"\nDemo Login Credentials:")
        print(f"  Email: demo@mjcrm.com")
        print(f"  Password: demo123")
        print(f"\nSample Data Created:")
        print(f"  - 1 Organization")
        print(f"  - 1 Demo User (Admin)")
        print(f"  - 3 Companies")
        print(f"  - 3 Contacts")
        print(f"  - 5 Leads")
        print(f"  - 3 Deals")
        print(f"  - 5 Activities")
        print(f"  - 5 Products")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
