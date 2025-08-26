from odoo import models, fields, api

class ClinicConsultancy(models.Model):
    _name = 'clinic.consultancy'
    _description = 'Clinic Consultancy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

<<<<<<< HEAD
    name = fields.Char(string='Consultancy No.', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('clinic.reception.consultation'))
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True, tracking=True)
    date = fields.Datetime(string='Consultation Date', default=fields.Datetime.now, tracking=True)

    complaint = fields.Text(string='Chief Complaint')
    visit_history = fields.Text(string='Visit History')
    medical_record = fields.Text(string='Medical Record')
    notes = fields.Text(string='Additional Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ], string='Status', default='draft', tracking=True)

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        """ Mark consultation as done and create invoice """
        for record in self:
            if not record.invoice_id:
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': record.patient_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': f"Consultation Fee - {record.name}",
                        'quantity': 1,
                        'price_unit': 100.0,  # 👈 set your consultation fee or fetch from config
                    })]
                })
                record.invoice_id = invoice.id
            record.state = 'done'
        return True
=======
    name = fields.Char(string='Consultancy Name', required=True)
    patient_id = fields.Many2one('res.partner', string='Patient')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    date = fields.Date(string='Consultation Date')
    notes = fields.Text(string='Notes')
>>>>>>> origin/testing
