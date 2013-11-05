from openerp.osv import fields, osv


class admin_doc_type(osv.Model):
    """Kind of an administrative document employees have to provide."""

    _name = 'admin_doc_type'

    _columns = {
        'name': fields.char('Description', size=256),
    }


class admin_doc(osv.Model):
    """An administrative document employees have to provide.
    Inherit[s] from ir.attachment to store documents as attachments.
    """

    _name = 'admin_doc'

    _inherits = {
        'ir.attachment': 'file_id',
    }

    _columns = {
        'type_id': fields.many2one('admin_doc_type',
                                   'Type',
                                   required=True),
        'employee_id': fields.many2one('hr.employee',
                                       'Employee'),
        'file_id': fields.many2one('ir.attachment',
                                   'File',
                                   ondelete='restrict',
                                   required=True),
    }

    def create(self, cr, uid, vals, context=None):
        """- Fill the "name" from the original filename.
        - Associate the new attachment with the current employee.
        """

        vals['name'] = vals['datas_fname']

        vals['res_model'] = 'hr.employee'
        vals['res_id'] = vals['employee_id']

        return super(admin_doc, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """Fill the "name" from the original filename."""

        if 'datas_fname' in vals:
            vals['name'] = vals['datas_fname']

        return super(admin_doc, self).write(cr, uid, ids, vals,
                                            context=context)

    def unlink(self, cr, uid, ids, context=None):
        """Delete the attachment associated with records being deleted."""

        brs = self.browse(cr, uid, ids, context=context)
        attachment_ids = [br.file_id.id for br in brs]

        ret = super(admin_doc, self).unlink(cr, uid, ids, context=context)

        attachment_obj = self.pool.get('ir.attachment')
        attachment_obj.unlink(cr, uid, attachment_ids, context=context)

        return ret
