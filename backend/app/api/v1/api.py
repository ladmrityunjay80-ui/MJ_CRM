"""
API Router
Aggregates all API v1 routes
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, leads, contacts, companies, deals, activities, products, workflows, emails, analytics, documents, import_export, webhooks, notifications, permissions, search, bulk, campaigns, audit_logs, comments, forecasting, mobile, reports, integrations, insights

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(deals.router, prefix="/deals", tags=["deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(import_export.router, prefix="/import-export", tags=["import-export"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(bulk.router, prefix="/bulk", tags=["bulk"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
api_router.include_router(mobile.router, prefix="/mobile", tags=["mobile"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
