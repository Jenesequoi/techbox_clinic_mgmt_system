from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ClinicLaboratoryTest(models.Model):
    _name = 'clinic.laboratory.test'
    _description = 'Laboratory Test'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Fields
    name = fields.Char(string='Test Reference', default=lambda self: _('New'), copy=False, readonly=True)
    reception_id = fields.Many2one('clinic.reception', string='Reception Reference', required=True, ondelete='restrict')
    patient_id = fields.Many2one(related='reception_id.patient_name', string='Patient', store=True, readonly=True)
    date = fields.Date(string='Visit Date', default=fields.Date.context_today, required=True)
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
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting', tracking=True, group_expand='_expand_states')
    department_id = fields.Many2one('clinic.department', string='Department', required=True, ondelete='restrict')
    doctor_id = fields.Many2one('hr.employee', string='Doctor In Charge', required=True, help="Select the doctor responsible for this test")
    is_billed = fields.Boolean(string="Is Billed", default=False, readonly=True)

    @api.model
    def create(self, vals):
        """Generate a unique reference for the lab test"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.laboratory.test') or _('New')
        return super(ClinicLaboratoryTest, self).create(vals)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Reset doctor when department changes and filter doctors"""
        self.doctor_id = False
        if self.department_id:
            return {
                'domain': {
                    'doctor_id': [('department_id', '=', self.department_id.id)]
                }
            }
        return {'domain': {'doctor_id': []}}

    def _expand_states(self, states, domain, order):
        """Expand state selection for group_by"""
        return [key for key, val in type(self).state.selection]

    def action_start(self):
        """Set state to In Progress"""
        for rec in self:
            if rec.state == 'waiting':
                rec.state = 'in_progress'

    def action_complete(self):
        """Set state to Completed"""
        for rec in self:
            if rec.state == 'in_progress':
                rec.state = 'completed'

    def action_cancel(self):
        """Set state to Cancelled"""
        for rec in self:
            if rec.state not in ('completed', 'cancelled'):
                rec.state = 'cancelled'

    def action_reset(self):
        """Reset state to Waiting"""
        for rec in self:
            if rec.state in ('cancelled', 'completed'):
                rec.state = 'waiting'

    def action_create_invoice(self):
        """Create an invoice for the lab test using department's service product and price"""
        self.ensure_one()
        
        # Log for debugging
        _logger.info("Creating invoice for Lab Test ID: %s, Reference: %s, Department: %s, Service Product: %s, Service Price: %s",
                     self.id, self.name, self.department_id.name or 'None',
                     self.department_id.service_product_id.name or 'None',
                     self.department_id.service_price or 0.0)

        # Validate required fields
        if not self.patient_id:
            raise UserError(_("No patient is linked to this lab test. Please set a valid reception reference."))
        if not self.department_id:
            raise UserError(_("No department is selected for this lab test."))
        if not self.department_id.service_product_id:
            raise UserError(_("The department '%s' is missing a service product.") % self.department_id.name)
        if not self.department_id.service_price:
            raise UserError(_("The department '%s' is missing a service price.") % self.department_id.name)
        if not self.department_id.service_product_id.active:
            raise UserError(_("The service product '%s' is inactive.") % self.department_id.service_product_id.name)

        # Prepare invoice line
        invoice_line_vals = {
            'name': f'Lab Test - {self.get_test_type_label()} ({self.department_id.name})',
            'quantity': 1.0,
            'price_unit': self.department_id.service_price,
            'product_id': self.department_id.service_product_id.id,
        }

        # Prepare invoice
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,
            'invoice_origin': self.name or f'Lab Test #{self.id}',
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
            'invoice_date': fields.Date.today(),
        }

        # Create invoice
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        self.is_billed = True

        return {
            'name': _('Customer Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    def action_view_invoice(self):
        """View the invoice associated with this lab test"""
        self.ensure_one()
        invoice = self.env['account.move'].search([('invoice_origin', '=', self.name or f'Lab Test #{self.id}')], limit=1)
        if invoice:
            return {
                'name': _('Customer Invoice'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
                'target': 'current',
            }
        raise UserError(_("No invoice found for this lab test."))

    def get_test_type_label(self):
        """Return the human-readable label for the test type"""
        return dict(self.fields_get(['test_type'])['test_type']['selection']).get(self.test_type, 'Other')