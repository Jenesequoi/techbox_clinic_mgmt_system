from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PharmacyDispense(models.Model):
    _name = 'pharmacy.dispense'
    _description = 'Medication Dispensing Log'
    _order = 'dispensed_on desc'

    prescription_id = fields.Many2one('clinic.prescription', string="Prescription", required=True)
    pharmacist_id = fields.Many2one('res.users', string="Dispensed By", default=lambda self: self.env.user, readonly=True)
    dispensed_on = fields.Datetime(string="Dispensed On", default=fields.Datetime.now, readonly=True)
    line_ids = fields.One2many('pharmacy.dispense.line', 'dispense_id', string="Dispensed Items")

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

            rec.prescription_id.verification_status = 'dispensed'


class PharmacyDispenseLine(models.Model):
    _name = 'pharmacy.dispense.line'
    _description = 'Dispensed Medication Line'

    dispense_id = fields.Many2one('pharmacy.dispense', string="Dispense Record", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Medication", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    expiry_date = fields.Date(string="Expiry Date")
