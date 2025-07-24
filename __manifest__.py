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
        'views/clinic_reception_views.xml',
        'views/menus.xml',
    ],
    'auto_install': False,
    'application': True,
    'installable': True,
    'sequence': 10,
}