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



    def create(self, cr, uid, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).create(cr, uid, values,
                                                          context)

    def write(self, cr, uid, ids, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).write(cr, uid, ids, values,
                                                         context=context)
