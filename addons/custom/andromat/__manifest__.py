{
    'name': 'Andromat',
    'category': 'Sales/CRM',
    'sequence': 150,
    'summary': 'Personalizaciones de vistas y funcionalidades',
    'description': "",
    'depends': ['project', 'helpdesk_mgmt', 'contacts', 'sale_management', 'contract_sale', 'contract_sale_generation'],
    'data': [
        'views/contact.xml',
        'views/ticket.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}