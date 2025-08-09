from odoo import fields, models, _


class ClinicMCH(models.Model):
    _name = 'clinic.mch'
    _description = 'Maternal & Child Health'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    reception_id = fields.Many2one('clinic.reception', string='Reception Reference', required=True)
    patient_id = fields.Many2one(related='reception_id.patient_name', string='Patient', store=True)
    date = fields.Date(string='Visit Date', default=fields.Date.context_today)

    # MCH Fields
    pregnancy_status = fields.Selection([
        ('pregnant', 'Pregnant'),
        ('postnatal', 'Postnatal'),
        ('child', 'Child Visit')
    ], string='Visit Type', required=True)

    weeks_pregnant = fields.Integer(string='Weeks Pregnant')
    delivery_date = fields.Date(string='Expected Delivery Date')
    immunization = fields.Boolean(string='Child Immunization')
    notes = fields.Text(string='Visit Notes')