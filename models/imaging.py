from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ClinicImaging(models.Model):
    _name = 'clinic.imaging'
    _description = 'Imaging Study'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Fields for imaging
    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    reception_id = fields.Many2one(
        'clinic.reception',
        string='Reception Reference',
        required=True
    )
    patient_id = fields.Many2one(
        related='reception_id.patient_name',
        string='Patient',
        store=True,
        readonly=True
    )
    date = fields.Date(
        string='Visit Date',
        default=fields.Date.context_today
    )
    imaging_type = fields.Selection([
        ('xray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('mammography', 'Mammography'),
        ('fluoroscopy', 'Fluoroscopy'),
        ('angiography', 'Angiography'),
        ('bone_density', 'Bone Density Scan (DEXA)'),
        ('pet_scan', 'PET Scan'),
        ('other', 'Other'),
    ], string="Imaging Type", required=True)
    body_part = fields.Char(string="Body Part/Area")
    description = fields.Text(string="Description / Findings")
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="waiting", tracking=True)
    result_attachment = fields.Binary(string="Result Attachment")
    result_filename = fields.Char(string="File Name")
    technician_id = fields.Many2one(
        'res.users',
        string="Technician",
        default=lambda self: self.env.user
    )
    notes = fields.Text(string="Technician Notes")
    invoice_id = fields.Many2one(
        'account.move',
        string="Invoice",
        readonly=True,
        copy=False
    )

    # Imaging price mapping (default prices)
    imaging_price = fields.Monetary(
        string="Imaging Price",
        compute="_compute_imaging_price",
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.company.currency_id.id
    )

    @api.depends('imaging_type')
    def _compute_imaging_price(self):
        """Assign default prices based on imaging type"""
        price_map = {
            'xray': 50.0,
            'ultrasound': 80.0,
            'ct_scan': 200.0,
            'mri': 300.0,
            'mammography': 150.0,
            'fluoroscopy': 120.0,
            'angiography': 250.0,
            'bone_density': 100.0,
            'pet_scan': 500.0,
            'other': 75.0,
        }
        for rec in self:
            rec.imaging_price = price_map.get(rec.imaging_type, 0.0)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.imaging.request') or _('New')
        return super(ClinicImaging, self).create(vals)

    def action_mark_in_progress(self):
        self.write({'status': 'in_progress'})

    def action_mark_completed(self):
        self.write({'status': 'completed'})

    def action_mark_cancelled(self):
        self.write({'status': 'cancelled'})

    def action_create_invoice(self):
        """Create an invoice for the imaging study"""
        for rec in self:
            if rec.invoice_id:
                raise UserError(_("An invoice is already linked to this imaging study."))

            if not rec.patient_id:
                raise UserError(_("No patient is linked to this imaging study."))

            # Find the partner (patient record must have res.partner link)
            partner = rec.reception_id.patient_id.partner_id
            if not partner:
                raise UserError(_("Patient does not have a linked partner (customer record)."))

            # Get label for imaging type
            imaging_label = dict(self._fields['imaging_type'].selection).get(rec.imaging_type)

            move_vals = {
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [(0, 0, {
                    'name': f"Imaging: {imaging_label} ({rec.body_part or 'N/A'})",
                    'quantity': 1,
                    'price_unit': rec.imaging_price,
                })]
            }
            invoice = self.env['account.move'].create(move_vals)
            rec.invoice_id = invoice.id

            return {
                'name': _('Invoice'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
            }
