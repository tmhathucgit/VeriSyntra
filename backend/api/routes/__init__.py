"""
API routes package
Vietnamese business context: Authentication and authorization routes
"""

from .auth import router as auth_router

__all__ = ['auth_router']
