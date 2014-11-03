#!/usr/bin/env python

"""Fill operational departments by taking the current department of each
employee.
"""

import xmlrpclib

# DB Connection, modify these params to aim the correct database

HOST = 'localhost'
PORT = 8169
USER = 'admin'
PASS = 'a'
DB = 'elias_copy'

url = 'http://%s:%d/xmlrpc/common' % (HOST, PORT)
sock = xmlrpclib.ServerProxy(url)
uid = sock.login(DB, USER, PASS)
print('Logged in as %s (uid: %d)' % (USER, uid))

url = 'http://%s:%d/xmlrpc/object' % (HOST, PORT)
sock = xmlrpclib.ServerProxy(url, allow_none=True)

# Find employees and save their department.
employee_ids = sock.execute(
    DB, uid, PASS, 'hr.employee', 'search', []
)
employees = sock.execute(
    DB, uid, PASS, 'hr.employee', 'read', employee_ids, [
        'department_id',
    ]
)
emp_deps = {
    employee['id']: employee['department_id'][0]
    for employee in employees
    if employee['department_id']
}
print('Found %d employees with departments' % len(emp_deps))

counter = 0

# Create an operational department for each (employee, department) couple.
for employee_id, department_id in emp_deps.iteritems():
    sock.execute(
        DB, uid, PASS, 'hr.operational_department', 'create', {
            'department_id': department_id,
            'employee_id': employee_id,
        }
    )

    counter += 1
    if counter % 20 == 0:
        print('Processed %d employees' % counter)

print('Done.')
