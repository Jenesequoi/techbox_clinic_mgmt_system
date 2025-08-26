{
    'name': 'TechBox Clinic Management System',
    'version': '1.0',
    'summary': 'Clinic Management System built in Odoo 17',
    'description': """
        Complete Clinic Management System including Reception, Consultations, 
        MCH, Laboratory, Imaging, Pharmacy, and Configuration modules built in Odoo 17.
    """,
    'author': 'Techbox, SoftlinkOptions',
    'website': 'https://www.techbox.com',  # optional, but recommended
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'depends': [
        'base',
        'mail',
        'hr',       # for employees
        'account',  # needed for invoicing in Imaging and Pharmacy
    ],
    'data': [
        # Security
        'security/clinic_security.xml',
        'security/ir.model.access.csv',

        # Core Views (must load before menus)
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

        # Sequences (must load before menus so references work)
        'data/ir_sequence_data.xml',

        # Menus (always last so all actions/views exist already)
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 10,
}
