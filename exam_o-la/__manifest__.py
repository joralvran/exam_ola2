{
    'name': "Grupo O-LA  - Test",
    'summary': "Módulo de prueba de reclutamiento",
    'description': """
        Este Modulo contiene una prueba evaluativa de conocimientos para el ingreso a la empresa como desarrollador 
    """,
    'author': "Jorge Alavraez",
    'website': "",
    'category': 'Sales',
    'license': 'OPL-1',
    'version': '16.0.0.1',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/exam_report.xml',
        'views/exam_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
