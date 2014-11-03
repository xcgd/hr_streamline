from openerp.osv import fields, osv
from openerp.tools.translate import _

from .util import default_context


class hr_operational_department(osv.Model):
    """Department an employee gets to work for.
    One employee may be working for multiple operational departments at the
    same time.
    This is a separate object so priorities can be changed.
    """

    _name = 'hr.operational_department'

    _order = 'priority ASC, department_id ASC'

    _columns = {
        'department_id': fields.many2one(
            'hr.department',
            u"Department",
            ondelete='cascade',
            required=True,
        ),

        'employee_id': fields.many2one(
            'hr.employee',
            u"Employee",
            ondelete='cascade',
            required=True,
        ),

        'company_id': fields.related(
            'department_id',
            'company_id',
            type='many2one',
            obj='res.company',
            string=u"Department company",
            readonly=True,
        ),

        'priority': fields.integer(
            u"Priority",
            help=(
                u"Number used to sort operational department lists. The "
                u"lowest priority is the most important."
            ),
        ),
    }

    _defaults = {
        'priority': 10,
    }

    _sql_constraints = [
        (
            'unique_department_employee',
            'UNIQUE(department_id, employee_id)',
            _(u"The department is already in the list.")
        )
    ]

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        context = default_context(self, cr, uid, context)

        op_deps = self.browse(cr, uid, ids, context=context)
        return [
            (op_dep.id, op_dep.department_id.name)
            for op_dep in op_deps
        ]

    def name_search(
        self, cr, uid, name='', args=None, operator='ilike', context=None,
        limit=80
    ):
        if not args:
            args = []

        if not name:
            return super(hr_operational_department, self).name_search(
                cr, uid, name=name, args=args, operator=operator,
                context=context, limit=limit
            )

        ids = self.search(
            cr, uid,
            [('department_id.name', operator, name)] + args,
            limit=limit,
            context=context
        )

        return self.name_get(cr, uid, ids, context=context)
