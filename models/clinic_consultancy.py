from odoo import models, fields

class ClinicConsultancy(models.Model):
    _name = 'clinic.consultancy'
    _description = 'Clinic Consultancy'

    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    date = fields.Date(string='Consultation Date')
    notes = fields.Text(string='Notes')
