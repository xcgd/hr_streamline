# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '1.1',
    'author': 'XCG Consulting',
    'category': 'Human Resources',
    'description': """ enchancements to the hr module to streamline its usage""",
    'website': 'http://www.openerp-experts.com',
    'depends': [
        'base',
        'hr',
    ],
     'data': [
        'security/ir.model.access.csv',
        'view/hr_streamline.xml',
    ],
    'test': [
    ],
    'installable': True,
 }
