from odoo import fields, models, _


class ClinicConsultancy(models.Model):
    _name = 'clinic.consultancy'
    _description = 'Clinic Consultancy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'consultation_date desc'

    ref = fields.Char(string='Consultation ID', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    consultation_date = fields.Date(string='Consultation Date', required=True, default=fields.Date.context_today)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
    consulting_doctor = fields.Many2one('res.users', string='Consulting Doctor', required=True)
    diagnosis = fields.Text(string='Diagnosis')
    notes = fields.Html(string='Consultation Notes')
    follow_up_date = fields.Date(string='Follow-Up Date')
    is_referral = fields.Boolean(string='Referral Case', default=False)
    referred_by = fields.Many2one('res.partner', string='Referred By')
    guardian = fields.Many2one('res.partner', string='Guardian')
    is_married = fields.Boolean(string='Is Married', default=False)
    spouse = fields.Many2one('res.partner', string='Spouse')

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = fields.Date.today()
                record.age = today.year - record.dob.year - (
                    (today.month, today.day) < (record.dob.month, record.dob.day))
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('clinic.consultancy') or _('New')
        return super(ClinicConsultancy, self).create(vals)
