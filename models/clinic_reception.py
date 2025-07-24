from odoo import fields, models, _


class ClinicReception(models.Model):
    _name = 'clinic.reception'
    _description = 'Clinic Reception'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'


    ref = fields.Char(string='Visit_Id', required=True, copy=False)
    # patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    patient_name = fields.Many2one('res.partner', string='Patient', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', store=True, tracking=True)
    service = fields.Selection(
        [('consultation', 'Consultation'),
         ('mch', 'MCH'),
         ('pharmacy', 'Pharmacy'),
         ('laboratory', 'Laboratory'),
         ('imaging', 'Imaging')], string='Outpatient Service',
        required=True)
    is_referral = fields.Boolean(string='Is Referral', default=False)
    referral_id = fields.Many2one('res.partner', string='Referral Doctor')
    guardian = fields.Many2one('res.partner', string='Guardian')
    is_married = fields.Boolean(string='Is Married', default=False)
    spouse = fields.Many2one('res.partner', string='Spouse')
