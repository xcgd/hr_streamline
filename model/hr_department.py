from openerp import models

from openerp.addons.analytic_structure.MetaAnalytic import MetaAnalytic


class HrDepartment(models.Model):
    """Add analytics into departments:
    - Departments may contain analytic fields.
    """

    __metaclass__ = MetaAnalytic

    _analytic = 'hr.department'

    _inherit = 'hr.department'
