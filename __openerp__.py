# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '1.5.2',
    'author': 'XCG Consulting',
    'category': 'Human Resources',
    'description': """ enchancements to the hr module to
    streamline its usage
    """,
    'website': 'http://www.openerp-experts.com',
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
    'test': [
    ],
    'installable': True,
}
