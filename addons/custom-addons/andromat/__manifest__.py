{
    "name": "Andromat",
    "category": "Accounting",
    "sequence": 150,
    "summary": "Personalizaciones de vistas y funcionalidades",
    "description": "",
    "depends": [
        "project",
        "hr_timesheet",
        "helpdesk_mgmt",
        "helpdesk_mgmt_timesheet",
        "project_timesheet_time_control",
        "contacts",
        "sale_management",
        "contract",
        "contract_sale",
        "contract_sale_generation",
        "account"
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