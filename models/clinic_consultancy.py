from odoo import models, fields, api

class ClinicConsultancy(models.Model):
    _name = 'clinic.consultancy'
    _description = 'Clinic Consultancy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Consultation Reference', required=True, copy=False, readonly=True, default='New')
    patient_id = fields.Many2one('clinic.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True, tracking=True)
    date = fields.Datetime(string='Consultation Date', default=fields.Datetime.now, required=True)
    
    complaint = fields.Text(string="Patient Complaint")
    consultation_details = fields.Html(string="Consultation Details")
    visit_history = fields.Text(string="Visit History")
    medical_record = fields.Text(string="Medical Record")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('invoiced', 'Invoiced'),
    ], string='Status', default='draft', tracking=True)

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    # Generate sequence for reference name
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.consultancy') or 'New'
        return super(ClinicConsultancy, self).create(vals)

    def action_start_consultation(self):
        self.write({'state': 'in_progress'})

    def action_complete_and_invoice(self):
        """Mark consultation as complete and create invoice."""
        self.write({'state': 'done'})
        
        # Create invoice
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id if self.patient_id.partner_id else False,
            'invoice_line_ids': [(0, 0, {
                'name': f'Consultation - {self.name}',
                'quantity': 1,
                'price_unit': 1000.0,  # Default consultation fee (can be made configurable)
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.write({'state': 'invoiced', 'invoice_id': invoice.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }
