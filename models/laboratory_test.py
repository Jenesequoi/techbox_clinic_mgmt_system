from odoo import models, fields, api, _

class ClinicLaboratoryTest(models.Model):
    _name='clinic.laboratory.test'
    _description='Laboratory Test'
    _inherit=['mail.thread','mail.activity.mixin']
    _order='date desc'

    # Fields for laboratory
    reception_id = fields.Many2one('clinic.reception',string='Reception Reference',required=True)
    patient_id = fields.Many2one(related='reception_id.patient_name',string='Patient',store=True,readonly=True)
    date = fields.Date(string='Visit Date', default=fields.Date.context_today)
    test_type = fields.Selection([
        ('cbc', 'Complete Blood Count (CBC)'),
        ('blood_sugar', 'Blood Sugar / Glucose Test'),
        ('malaria', 'Malaria Test'),
        ('hiv', 'HIV Test'),
        ('urinalysis', 'Urinalysis'),
        ('stool_analysis', 'Stool Analysis'),
        ('pregnancy', 'Pregnancy Test'),
        ('liver_function', 'Liver Function Test'),
        ('kidney_function', 'Kidney Function Test'),
        ('typhoid', 'Typhoid Test (Widal)'),
        ('cholesterol', 'Cholesterol Test'),
        ('other', 'Other'),
        ], string="Test Type", required=True)
    description = fields.Text(string="Description / Remarks")
    status = fields.Selection([
        ('queued', 'Queued'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='queued', tracking=True)
    