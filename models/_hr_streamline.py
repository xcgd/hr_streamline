# -*- coding: utf-8 -*-
from base64 import b64decode
from cStringIO import StringIO
from PIL import Image

import openerp

from osv import fields
from osv import osv

from tools.translate import _


class hr_employee_streamline(osv.osv):

    _inherit = 'hr.employee'

    _columns ={
        'signature' : fields.binary(_('Signature')),
        'signature_type' : fields.char(_('Signature Type (.png, jpg, ..)')),
    }

    def _update_values(self, values):
        if not 'signature' in values:
            return
        file_like = StringIO(b64decode(values['signature']))
        values['signature_type'] = Image.open(file_like).format.lower()

    def create(self, cr, uid, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).create(cr, uid, values,
                                                          context)

    def write(self, cr, uid, ids, values, context=None):
        self._update_values(values)
        return super(hr_employee_streamline, self).write(cr, uid, ids, values,
                                                         context=context)
