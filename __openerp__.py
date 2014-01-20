# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '1.3',
    'author': 'XCG Consulting',
    'category': 'Human Resources',
    'description': """ enchancements to the hr module to
    streamline its usage
    """,
    'website': 'http://www.openerp-experts.com',
    'depends': [
        'base',
        'hr',
        'hr_contract',
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
