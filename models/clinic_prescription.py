
from odoo import models, fields, api, _


class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Clinic Prescription'

    name = fields.Char(string='Prescription ID', required=True, default='New', readonly=True, copy=False)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    line_ids = fields.One2many('clinic.prescription.line', 'prescription_id', string='Medications')

    verification_status = fields.Selection([
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('flagged', 'Flagged for Review')
    ], default='pending', string='Verification Status')

    verified_by = fields.Many2one('res.users', string='Verified By', readonly=True)
    verification_date = fields.Datetime(string='Verified On', readonly=True)
    has_expired_drugs = fields.Boolean(string='Has Expired Drugs', compute='_compute_expiry_warning')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.prescription') or 'New'
        return super().create(vals)

    @api.depends('line_ids.expiry_date')
    def _compute_expiry_warning(self):
        for rec in self:
            rec.has_expired_drugs = any(
                line.expiry_date and line.expiry_date < fields.Date.today() for line in rec.line_ids
            )

    def action_approve_dispense(self):
        for rec in self:
            rec.verification_status = 'approved'
            rec.verified_by = self.env.user
            rec.verification_date = fields.Datetime.now()

    def action_flag_issue(self):
        for rec in self:
            rec.verification_status = 'flagged'
            rec.verified_by = self.env.user
            rec.verification_date = fields.Datetime.now()


class ClinicPrescriptionLine(models.Model):
    _name = 'clinic.prescription.line'
    _description = 'Prescription Medication Line'

    prescription_id = fields.Many2one('clinic.prescription', string='Prescription', required=True, ondelete='cascade')
    medication = fields.Char(string='Medication', required=True)
    dosage = fields.Char(string='Dosage')
    instructions = fields.Text(string='Instructions')
    availability = fields.Boolean(string='Available', default=True)
    expiry_date = fields.Date(string='Expiry Date')
