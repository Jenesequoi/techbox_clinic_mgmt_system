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
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',

        # ✅ Load this FIRST to prevent menu reference errors
        'views/menus.xml',

        # Other views that depend on menus
        'views/clinic_reception_views.xml',
        'views/clinic_prescription_views.xml',
        'views/pharmacy_dispense_views.xml',
        'views/pharmacy_queue_views.xml',
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
    'sequence': 10,
}
