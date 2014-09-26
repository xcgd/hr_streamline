# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '1.5',
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
        'hr_employee.xml',
        'menu.xml',
    ],
    'test': [
    ],
    'installable': True,
}
