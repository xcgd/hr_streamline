# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '1.6',
    'author': 'XCG Consulting',
    'category': 'Human Resources',
    'description': """Enchancements to the hr module to
    streamline its usage
    """,
    'website': 'http://odoo.consulting/',
    'depends': [
        'base',
        'hr',
        'document_attachment',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/hr_employee.xml',
        'views/hr_operational_department.xml',
        'menu.xml',
    ],
    'demo': [
        'demo/hr.operational_department.csv',
    ],
    'test': [
    ],
    'installable': True,
}
