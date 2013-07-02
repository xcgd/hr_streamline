# -*- coding: utf-8 -*-
import base64
import os

from openerp.tools import convert_xml_import
from osv import osv

from openerp.tests.common import TransactionCase


ROOT = os.path.dirname(__file__)
DATA = os.path.join(ROOT, 'data.xml')

with open(os.path.join(ROOT, 'data.jpg')) as img:
    IMG = base64.b64encode(img.read())


class TestHrStreamline(TransactionCase):

    def setUp(self):
        super(TestHrStreamline, self).setUp()
        # load xml data
        convert_xml_import(self.cr, 'hr_streamline', DATA, {}, 'update')

    @property
    def _employee(self):
        return self.registry('hr.employee')

    @property
    def _resource(self):
        return self.registry('resource.resource')

    def test_add_image_ok(self):
        # shortcut
        cr, uid = self.cr, self.uid
        # create a resource
        resource_id = self._resource.create(cr, uid, {
            'name': 'test_resource',
        })
        # create an employee
        employee_id = self._employee.create(cr, uid, {
            'name': 'test_resource',
            'resource_id': resource_id,
            'signature': IMG,
        })
        # little check
        self.assertFalse(employee_id is False)
        # write
        employee = self._employee.browse(cr, uid, employee_id)
        self.assertEqual(employee.signature_type, 'jpeg')

    def test_write_image_ok(self):
        # shortcut
        cr, uid = self.cr, self.uid
        # get an employee
        employee_ids = self._employee.search(cr, uid, [
            ('name', '=', 'florent'),
        ])
        # write
        res = self._employee.write(cr, uid, employee_ids, {
            'signature': IMG,
        })
        # little check
        self.assertTrue(res)
        # write
        employee = self._employee.browse(cr, uid, employee_ids[0])
        self.assertEqual(employee.signature_type, 'jpeg')

    def test_write_image_ko(self):
        # shortcut
        cr, uid = self.cr, self.uid
        # get an employee
        employee_ids = self._employee.search(cr, uid, [
            ('name', '=', 'florent'),
        ])
        # prepare values
        values = {
            'signature': 'dummy_text_for_signaturebad_content',
        }
        # write should failed
        self.assertRaisesRegexp(osv.except_osv,
                            'Invalid Image',
                            self._employee.write,
                            cr, uid, employee_ids, values)
