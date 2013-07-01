# -*- coding: utf-8 -*-
{
    'name': 'Human Employee Streamline',
    'version': '0.1',
    'category': 'Human Resources',
    'description': """
""",
    'author': 'Florent Pigout <florent.pigout@gmail.com>',
    'maintainer': 'Florent Pigout <florent.pigout@gmail.com>',
    'website': 'http://www.xcg-consulting.fr/fr/services/openerp',
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
