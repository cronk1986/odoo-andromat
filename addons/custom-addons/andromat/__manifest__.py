{
    "name": "Andromat",
    "category": "Accounting",
    "sequence": 150,
    "summary": "Personalizaciones de vistas y funcionalidades",
    "description": "",
    "depends": [
        "project", 
        "helpdesk_mgmt",
        "helpdesk_mgmt_timesheet",
        "contacts", 
        "sale_management", 
        "contract_sale", 
        "contract_sale_generation", 
        "account",
        "contract",
        "hr_timesheet"
    ],
    "data": [
        #"views/contact.xml",
        "views/ticket.xml",
        "views/account.xml",
        "views/contract_template.xml",
        "views/contract.xml"
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}