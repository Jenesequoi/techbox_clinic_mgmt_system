{
    'name': 'Clinic Consultancy',
    'version': '1.0',
    'category': 'Clinic Management',
    'summary': 'Manage consultancy sessions in the clinic',
    'description': 'A module to record and manage consultancy sessions.',
    'author': 'Your Name',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/consultancy_views.xml',
    ],
    'installable': True,
    'application': True,
}
