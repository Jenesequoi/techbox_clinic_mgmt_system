from odoo import models, fields

class ClinicConsultancy(models.Model):
    _name = 'clinic.consultancy'
    _description = 'Clinic Consultancy Session'

    name = fields.Char(string="Session Reference", required=True)
    date = fields.Datetime(string="Consultancy Date", required=True, default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', string="Client", required=True)
    consultant = fields.Char(string="Consultant Name", required=True)
    notes = fields.Text(string="Notes")
    fee = fields.Float(string="Fee")
