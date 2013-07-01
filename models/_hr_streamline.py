# -*- coding: utf-8 -*-
import openerp

from osv import fields
from osv import osv

from tools.translate import _


class hr_employee_streamline(osv.osv):

    _inherit = 'hr.employee'

    _columns ={
        'signature' : fields.binary(_('Signature'))
    }
