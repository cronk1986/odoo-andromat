# Copyright 2019-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models
from odoo.tools import ormcache

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    tax_agency_id = fields.Many2one("aeat.tax.agency", string="Tax Agency")
    representative_vat = fields.Char(
        string="L.R. VAT number",
        size=9,
        help="Legal Representative VAT number for all the AEAT reports of this company.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create immediately all the AEAT sequences when creating company."""
        companies = super().create(vals_list)
        models = (
            self.env["ir.model"]
            .sudo()
            .search([("model", "=like", "l10n.es.aeat.%.report")])
        )
        for model in models:
            try:
                self.env[model.model]._register_hook(companies=companies)
            except Exception as e:
                _logger.debug(e)
        return companies

    @ormcache("tax_template", "company")
    def _get_tax_id_from_tax_template(self, tax_template, company):
        """Low level cached search for a tax given its tax template and
        company.
        """
        xmlids = (
            self.sudo()
            .env["ir.model.data"]
            .search_read(
                [
                    ("model", "=", "account.tax.template"),
                    ("res_id", "=", tax_template.id),
                ],
                ["name", "module"],
            )
        )
        return (
            xmlids
            and self.sudo()
            .env["ir.model.data"]
            .search(
                [
                    ("model", "=", "account.tax"),
                    ("module", "=", xmlids[0]["module"]),
                    ("name", "=", "{}_{}".format(company.id, xmlids[0]["name"])),
                ]
            )
            .res_id
            or False
        )

    @ormcache("account_template", "company")
    def _get_account_id_from_account_template(self, account_template, company):
        """Low level cached search for a tax given its account template and
        company.
        """
        xmlids = (
            self.sudo()
            .env["ir.model.data"]
            .search_read(
                [
                    ("model", "=", "account.account.template"),
                    ("res_id", "=", account_template.id),
                ],
                ["name", "module"],
            )
        )
        return (
            xmlids
            and self.sudo()
            .env["ir.model.data"]
            .search(
                [
                    ("model", "=", "account.account"),
                    ("module", "=", xmlids[0]["module"]),
                    ("name", "=", "{}_{}".format(company.id, xmlids[0]["name"])),
                ]
            )
            .res_id
            or False
        )

    def get_taxes_from_templates(self, tax_templates):
        """Return company taxes that match the given tax templates."""
        self.ensure_one()
        tax_ids = []
        # We need to rebrowse the records to avoid a problem with the ormcache
        # and virtual records that populate m2m as NewId.
        for tmpl in self.env["account.tax.template"].browse(tax_templates.ids):
            tax_id = self._get_tax_id_from_tax_template(tmpl, self)
            if tax_id:
                tax_ids.append(tax_id)
        return self.env["account.tax"].browse(tax_ids)

    def get_account_from_template(self, account_template):
        """Return company account that match the given account template."""
        self.ensure_one()
        account_id = []
        if account_template:
            account_id = self._get_account_id_from_account_template(
                account_template, self
            )
        return self.env["account.account"].browse(account_id or [])
