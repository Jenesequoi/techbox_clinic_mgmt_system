{
    'name': 'TechBox Clinic Management System',
    'version': '1.0',
    'summary': 'Clinic Management System built in Odoo 17',
    'description': 'Complete Clinic Management System including Reception, Consultations, MCH, Laboratory, Imaging, Pharmacy, and Configuration modules built in Odoo 17.',
    'author': 'Techbox, SoftlinkOptions',
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'depends': [
        'base',
        'mail',
        'hr',  # added from testing
    ],
    'data': [
        # Security
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        
        # Views (load these before menus)
        'views/clinic_dashboard_views.xml',
        'views/clinic_reception_views.xml',
        'views/clinic_consultancy_views.xml',
        'views/clinic_mch_views.xml',
        'views/laboratory_test_views.xml',   # keep from testing
        'views/imaging_views.xml',           # keep from Imaging branch
        'views/clinic_prescription_views.xml',
        'views/pharmacy_queue_views.xml',
        'views/pharmacy_dispense_views.xml',
        'views/clinic_department_views.xml',

        # Menus (must always load last so actions exist already)
        'views/menus.xml',

        # Sequences (optional, uncomment if used)
        # 'data/sequences.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 10,
}
