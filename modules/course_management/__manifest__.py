{
    'name': 'Course Management',
    'version': '1.0',
    'category': 'Education',
    'sequence': 1,
    'description': 'Course Management System - Companion module for learning Odoo development',
    'author': 'Odoo Learning Journey',
    'depends': ['base'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/course_views.xml',
        'data/course_demo.xml',
    ],
    'demo': [
        'data/course_demo.xml',
    ],
}
