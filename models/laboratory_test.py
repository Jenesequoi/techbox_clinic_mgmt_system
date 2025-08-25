from odoo import models, fields, api, _
from odoo.exceptions import UserError

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
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="waiting", tracking=True)

     # state
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting', tracking=True, group_expand='_expand_states')

    department_id = fields.Many2one(
        'clinic.department',
        string='Department',
        required=True
    )

    # Doctor in charge field
    doctor_id = fields.Many2one('hr.employee',string='Doctor In Charge',required=True,help="Select the doctor responsible for this MCH visit")

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Reset doctor when department changes and filter doctors"""
        self.doctor_id = False
        
        # Return domain to filter employees by department
        if self.department_id:
            return {
                'domain': {
                    'doctor_id': [('department_id', '=', self.department_id.id)]
                }
            }
        else:
            return {
                'domain': {
                    'doctor_id': []
                }
            }


     # Button Actions
    # ---------------------------
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_complete(self):
        for rec in self:
            rec.state = 'completed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset(self):
        for rec in self:
            rec.state = 'waiting'

    # ---------- Create Invoice ----------
    def action_create_invoice(self):
        self.ensure_one()

        if not self.patient_id:
            raise UserError(_("No patient linked to this lab test."))

        if not self.department_id.service_product_id or not self.department_id.service_price:
            raise UserError(_("Department is missing Service Product or Price."))

        invoice_line_vals = {
            'name': f'Lab Test - {self.test_type} ({self.department_id.name})',
            'quantity': 1.0,
            'price_unit': self.department_id.service_price,
            'product_id': self.department_id.service_product_id.id,
        }

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,  # Patient as customer
            'invoice_origin': self.name or f'Lab Test #{self.id}',
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
        }

        invoice = self.env['account.move'].create(invoice_vals)

        return {
            'name': _('Customer Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

        def _get_test_price(self):
            """Return the price for the laboratory test based on test_type or department."""
            self.ensure_one()
            # Example: Use department service price as a fallback
            price = self.department_id.service_price or 0.0
            
            # Optional: Define prices per test type
            test_price_map = {
                'cbc': 50.0,
                'blood_sugar': 30.0,
                'malaria': 40.0,
                'hiv': 60.0,
                'urinalysis': 35.0,
                'stool_analysis': 45.0,
                'pregnancy': 25.0,
                'liver_function': 70.0,
                'kidney_function': 65.0,
                'typhoid': 55.0,
                'cholesterol': 50.0,
                'other': self.department_id.service_price or 0.0,
            }
            return test_price_map.get(self.test_type, price)
