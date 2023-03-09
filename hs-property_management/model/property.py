from datetime import datetime
from odoo import models, fields


class PropertyManagement(models.Model):
    _inherit = "hr.employee"

    given_materials_line_ids = fields.One2many("given.materials.line", "given_materials_line_id", string="Property")


class Property(models.Model):
    _name = "given.materials.line"

    given_materials_line_id = fields.Many2one("hr.employee", string="Property")
    name = fields.Many2one("product.template", string="Name")
    assign_date = fields.Datetime("Issue date", readonly=True, default=datetime.today())
    qty = fields.Integer("Quantity")
    given_condition = fields.Selection([("new", "New"), ("used", "Used")], string="Given Condition")
    returned = fields.Boolean(string="Returned")
    return_date = fields.Datetime(string="Return Date")
    return_condition = fields.Selection([("normal", "Normal"), ("damaged", "Damaged")], string="Return Condition")


class Product(models.Model):
    _inherit = "product.template"

    employee_use = fields.Boolean(string="Employee Use")
