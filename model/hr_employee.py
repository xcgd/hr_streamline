# -*- coding: utf-8 -*-
from base64 import b64decode
from cStringIO import StringIO
from PIL import Image

from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_employee_streamline(osv.Model):

    _inherit = 'hr.employee'

    def _get_managers(self, cr, uid, ids, field, arg, context=None):
        """Returns the manager of the user
        or openerp.osv.orm.browse_null instance
        if no manager is found
        """
        res = dict()
        for employee in self.browse(cr, uid, ids, context=context):
            if employee.department_id:
                manager = employee.department_id.manager_id
            else:
                manager = osv.orm.browse_null()
            res[employee.id] = manager
        return res

    def _search_managers(self, cr, uid, obj, name, args, context):
        ids = set()
        for cond in args:
            _id = cond[2]
            if cond[1] == '=':
                req = (
                    'SELECT hr_employee.id '
                    'FROM hr_employee '
                    'JOIN hr_department ON '
                    'hr_employee.department_id=hr_department.id '
                    'WHERE hr_department.manager_id = %s' % _id)
                cr.execute(req)
        r = cr.fetchall()
        for x in r:
            ids.add(x[0])
        if ids:
            return [('id', 'in', tuple(ids))]
        return [('id', '=', '0')]

    def is_purchase_validator(self, cr, uid, ids, field_names, args,
                              context=None):
        res = {}
        pool = self.pool['ir.model.data']
        l = pool.get_object(cr,
                            uid,
                            'purchase',
                            'group_purchase_manager'
                            )
        list_users = l.users
        m_users = [m.id for m in list_users]

        for employee in self.browse(cr, uid, ids, context=context):
            res[employee.id] = {
                    'is_validator': employee.user_id.id in m_users
                }
        return res

    _columns = {
        'signature': fields.binary(_('Signature')),
        'signature_type': fields.char(_('Signature Type (.png, jpg, ..)')),
        'manager_id': fields.function(
            _get_managers,
            fnct_search=_search_managers,
            method=True,
            string="Manager",
            type='many2one',
            obj='hr.employee',
            store=False),

        'operational_department_ids': fields.one2many(
            'hr.operational_department',
            'employee_id',
            u"Operational departments",
            help=(
                u"Departments (in any company) the employee gets to work for."
            ),
        ),

        'admin_doc_ids': fields.many2many(
            'document_attachment', 'admin_doc_rel_',
            'res_id', 'doc_id',
            'Administrative documents',
            ondelete="cascade",
        ),
        'validation_group_1': fields.many2one(
            'hr.vgroups',
            string="Validation group 1",
        ),
        'validation_group_2': fields.many2one(
            'hr.vgroups',
            string="Validation group 2",
        ),
        'validation_groups': fields.many2many(
            'hr.vgroups',
            'hr_employee_hr_vgroups_rel',
            'vgroup_id',
            'employee_id',
            string="Validation groups member of",
            readonly=True,
        ),
        'is_validator': fields.function(
            is_purchase_validator,
            readonly=True,
            type='boolean',
            string="Purchase validator",
            store={
                'hr.employee': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['employee_id', 'validation_group_1',
                     'validation_group_2', 'validation_groups'], 10),
            },
            multi='val',
        ),
    }

    def _update_values(self, values):
        if 'signature' not in values:
            return
        # invalidate signature and type
        if not values['signature']:
            values['signature'] = False
            values['signature_type'] = False
            return  # quit
        # load image and get its format
        try:
            file_like = StringIO(b64decode(values['signature']))
            format_ = Image.open(file_like).format.lower()
        # oops
        except Exception:
            raise osv.except_osv(
                _('Invalid Image'),
                _('Image can not be loaded!'))
        # keep the signature image format
        values['signature_type'] = format_

    def find_employees_by_category(
            self, cr, uid, cat_name,
            parent_cat_name=None, context=None,
            browse=False):
        """Find employees wich are tagged
        with a category whose name is cat_name.
        If parent_cat_name is specified, the category
        must be a child of the category whose name is parent_cat_name.
        Return a list of employee ids
        or a list of browse objects if browse is True.
        Return an empty list if no employee or
        no filtering categories matches the given criteria.

        :param cat_name: category name of the eemployee
        :param parent_cat_name: parent category name
        """
        category_osv = self.pool.get("hr.employee.category")
        employee_osv = self.pool.get("hr.employee")

        search_arg = [('name', '=', cat_name)]
        if parent_cat_name is not None:
            parent_ids = category_osv.search(
                cr, uid, [('name', '=', parent_cat_name)],
                limit=1, context=context)
            search_arg.append(('parent_id', 'child_of', parent_ids))
        cat_ids = category_osv.search(cr, uid, search_arg,
                                      limit=1, context=context)
        if not cat_ids:
            return cat_ids
        search_arg = [('category_ids', 'child_of', [cat_ids])]
        employee_ids = employee_osv.search(
            cr, uid,
            search_arg,
            context=context
        )
        if browse and employee_ids:
            return employee_osv.browse(
                cr, uid,
                employee_ids,
                context=context
            )
        return employee_ids

    def create(self, cr, uid, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).create(cr, uid, values,
                                                          context)

    def write(self, cr, uid, ids, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).write(cr, uid, ids, values,
                                                         context=context)


class hr_vgroups(osv.Model):

    _name = "hr.vgroups"

    _columns = {

        'name': fields.char('Group name', required=True),

        'for_validation_1': fields.one2many(
            'hr.employee',
            'validation_group_1',
            string="For first level validation employees",
            readonly=True,
        ),

        'for_validation_2': fields.one2many(
            'hr.employee',
            'validation_group_2',
            string="For second level validation employees",
            readonly=True,
        ),

        'members': fields.many2many(
            'hr.employee',
            'hr_employee_hr_vgroups_rel',
            'employee_id',
            'vgroup_id',
            domain=[('is_validator', '!=', False)],
            string="Group members",
        ),
    }

