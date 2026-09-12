# -*- coding: utf-8 -*-
{
    'name': 'Minutes of Meeting (MOM)',
    'version': '18.0.1.0.0',
    'category': 'Project Management',
    'summary': 'Manage Minutes of Meeting with tracking and approval workflow',
    'description': """
        Minutes of Meeting Module
        
        This module provides functionality to manage Minutes of Meeting (MOM) with:
        
        Features:
        - Create and manage meeting minutes
        - Track open points and action items
        - Assign responsibilities
        - Track target and actual completion dates
        - Approval workflow (Draft → In Progress → Completed → Approved)
        - State history tracking
        - Multiple attendees management
        - Meeting conductor/champion tracking
    """,
    'author': 'ASD',
    'depends': ['mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/mom_sequence_data.xml',
        'data/mom_demo_data.xml',
        'views/mom_format_views.xml',
        'views/mom_format_line_views.xml',
        'views/mom_open_point_views.xml',
        'views/mom_menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
