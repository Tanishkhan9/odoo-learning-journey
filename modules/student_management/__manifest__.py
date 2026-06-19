{
    'name': 'Student Management',
    'version': '1.0',
    'category': 'Education',
    'sequence': 1,
    'description': 'Student Management System - A practical example module for learning Odoo development',
    'author': 'Odoo Learning Journey',
    'depends': ['base', 'course_management'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/student_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/menu.xml',
        'views/student_views.xml',
        'data/student_demo.xml',
    ],
    'demo': [
        'data/student_demo.xml',
    ],
    'qweb': [],
    'test': [
        'tests/test_student_model.py',
    ],
}
