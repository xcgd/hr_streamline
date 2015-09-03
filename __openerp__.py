# -*- coding: utf-8 -*-
##############################################################################
#
#    Human Ressources Employee Streamline, for OpenERP
#    Copyright (C) 2013 XCG Consulting (http://odoo.consulting)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Human Employee Streamline',
    'version': '1.9',
    'author': 'XCG Consulting',
    'category': 'Human Resources',
    'description': """Enchancements to the hr module to
    streamline its usage
    """,
    'website': 'http://odoo.consulting/',
    'depends': [
        'base',
        'hr',
        'analytic_structure',
        'document_attachment',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',

        'views/hr_department.xml',
        'views/hr_employee.xml',
        'views/hr_operational_department.xml',
        'views/hr_view.xml',

        'menu.xml',
    ],
    'demo': [
        'demo/hr.operational_department.csv',
    ],
    'test': [
    ],
    'installable': True,
}
