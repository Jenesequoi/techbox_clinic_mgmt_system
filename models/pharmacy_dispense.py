from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PharmacyDispense(models.Model):
    _name = 'pharmacy.dispense'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # <-- ADD INHERITANCE HERE
    _description = 'Medication Dispensing Log'
    _order = 'dispensed_on desc'

    name = fields.Char(string='Dispense Reference', required=True, readonly=True, default='New') # Added a name field
    prescription_id = fields.Many2one('clinic.prescription', string="Prescription", required=True, tracking=True)
    pharmacist_id = fields.Many2one('res.users', string="Dispensed By", default=lambda self: self.env.user, readonly=True, tracking=True)
    dispensed_on = fields.Datetime(string="Dispensed On", default=fields.Datetime.now, readonly=True)
    status = fields.Selection([ # Added a status field for better tracking
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('pharmacy.dispense.line', 'dispense_id', string="Dispensed Items")
    notes = fields.Text(string='Internal Notes') # Added a notes field

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pharmacy.dispense') or 'New'
        return super(PharmacyDispense, self).create(vals)

    def action_complete_dispense(self):
        for rec in self:
            for line in rec.line_ids:
                if line.quantity > line.product_id.qty_available:
                    raise ValidationError(_(
                        "Not enough stock for product: %s. Only %s available." %
                        (line.product_id.display_name, line.product_id.qty_available)
                    ))

                if line.expiry_date and line.expiry_date < fields.Date.today():
                    raise ValidationError(_(
                        "Product %s is expired and cannot be dispensed." % line.product_id.display_name
                    ))

                # Deduct stock (simplified, assumes real stock management system)
                line.product_id.qty_available -= line.quantity

            rec.status = 'completed'
            rec.prescription_id.verification_status = 'dispensed'
            rec.message_post(body=_("Dispensing completed successfully."))

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancelled'
            rec.message_post(body=_("Dispensing cancelled."))


class PharmacyDispenseLine(models.Model):
    _name = 'pharmacy.dispense.line'
    _description = 'Dispensed Medication Line'

    dispense_id = fields.Many2one('pharmacy.dispense', string="Dispense Record", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Medication", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    expiry_date = fields.Date(string="Expiry Date")