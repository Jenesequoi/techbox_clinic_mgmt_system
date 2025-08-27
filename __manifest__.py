{
    'name': 'TechBox Clinic Management System',
    'version': '1.0',
    'summary': 'Clinic Management System built in Odoo 17',
    'description': """
        Complete Clinic Management System including Reception, Consultations, 
        MCH, Laboratory, Imaging, Pharmacy, and Configuration modules built in Odoo 17.
    """,
    'author': 'Techbox, SoftlinkOptions',
    'website': 'https://www.techbox.com',
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'depends': [
        'base',
        'mail',
        'hr',       # For employees
        'account',  # Needed for invoicing in Imaging and Pharmacy
    ],
    'data': [
        # Security & Access Rules
        'security/clinic_security.xml',
        'security/ir.model.access.csv',

        # Sequences (must load early for defaults in models)
        'data/ir_sequence_data.xml',

        # Core Views
        'views/clinic_dashboard_views.xml',
        'views/clinic_reception_views.xml',
        'views/clinic_consultancy_views.xml',
        'views/clinic_mch_views.xml',
        'views/laboratory_test_views.xml',
        'views/imaging_views.xml',
        'views/clinic_prescription_views.xml',
        'views/pharmacy_queue_views.xml',
        'views/pharmacy_dispense_views.xml',
        'views/clinic_department_views.xml',

        # Menus (always last)
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 10,
}
