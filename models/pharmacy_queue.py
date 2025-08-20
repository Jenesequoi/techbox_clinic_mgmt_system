from odoo import models, fields, api
from odoo.exceptions import UserError

class PharmacyQueue(models.Model):
    _name = 'pharmacy.queue'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # <-- ADD INHERITANCE HERE
    _description = 'Pharmacy Queue'
    _order = 'create_date asc'

    name = fields.Char(
        string="Queue ID",
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        required=True,
        tracking=True # Track if patient is changed
    )
    prescription_id = fields.Many2one(
        'clinic.prescription',
        string='Prescription',
        required=True,
        tracking=True
    )
    doctor_id = fields.Many2one(
        'res.users',
        string='Prescribing Doctor',
        required=True,
        tracking=True
    )
    pharmacist_id = fields.Many2one( # Added pharmacist field
        'res.users',
        string='Attending Pharmacist',
        tracking=True
    )
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_review', 'In Review'),
        ('ready', 'Ready for Pickup'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled')
    ],
        string='Status',
        default='waiting',
        tracking=True # <-- VERY IMPORTANT: Track status changes in chatter
    )
    notes = fields.Html(string='Internal Notes') # Added a notes field

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pharmacy.queue') or 'New'
        return super(PharmacyQueue, self).create(vals)

    def action_start_review(self):
        for rec in self:
            rec.status = 'in_review'
            rec.pharmacist_id = self.env.user
            rec.message_post(body=_("Review started by %s.") % self.env.user.name)

    def action_mark_ready(self):
        for rec in self:
            rec.status = 'ready'
            rec.message_post(body=_("Medication is ready for pickup."))

    def action_dispense(self):
        for rec in self:
            rec.status = 'dispensed'
            rec.message_post(body=_("Medication dispensed to patient."))

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancelled'
            rec.message_post(body=_("Queue entry cancelled."))