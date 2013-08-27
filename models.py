# -*- coding: utf-8 -*-
from base64 import b64decode
from cStringIO import StringIO
from PIL import Image

import openerp
from openerp.tools.translate import _

from osv import fields
from osv import osv


class hr_employee_streamline(osv.osv):

    _inherit = 'hr.employee'

    def _get_managers(self, cr, uid, ids, field, arg, context=None):
        """Returns the manager of the user
        or openerp.osv.orm.browse_null instance
        if no manager is found
        """
        res = dict()
        for employee in self.browse(cr, uid, ids,context=context):
            if employee.department_id:
                manager = employee.department_id.manager_id
            else:
                manager = openerp.osv.orm.browse_null()
            res[employee.id] = manager
        return res

    _columns ={
        'signature' : fields.binary(_('Signature')),
        'signature_type' : fields.char(_('Signature Type (.png, jpg, ..)')),
        'manager_id': fields.function(
            _get_managers,
            method=True,
            string="Manager",
            type='many2one',
            obj='hr.employee',
            store=False),
    }

    def _update_values(self, values):
        if not 'signature' in values:
            return
        # invalidate signature and type
        if not values['signature']:
            values['signature'] = False
            values['signature_type'] = False
            return # quit
        # load image and get its format
        try:
            file_like = StringIO(b64decode(values['signature']))
            format_ = Image.open(file_like).format.lower()
        # oops
        except Exception, e:
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
