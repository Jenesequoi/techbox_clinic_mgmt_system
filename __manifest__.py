{
    'name': 'TechBox Clinic Management System',
    'version': '1.0',
    'description': 'Clinic Management System built in Odoo17',
    'summary': 'Clinic Management System built in Odoo17',
    'author': 'Techbox, SoftlinkOptions',
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'depends': [
        'base',
        'mail',
        'product',
        'hr',
    ],
    'data': [
        # Security rules first
        'security/ir.model.access.csv',

        # Data records
        'data/clinic_department_data.xml',
        'data/ir_sequence_data.xml',

        # Views that define models & actions (load before menus)
        'views/clinic_department_views.xml',
        'views/clinic_dashboard_views.xml',
        'views/pharmacy_dispense_views.xml',
        'views/clinic_reception_views.xml',
        'views/clinic_prescription_views.xml',
        'views/pharmacy_queue_views.xml',

        # Menus last
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
}

