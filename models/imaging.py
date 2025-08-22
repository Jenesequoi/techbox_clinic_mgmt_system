from odoo import models, fields, api, _

class ClinicImaging(models.Model):
    _name = 'clinic.imaging'
    _description = 'Imaging Study'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Fields for imaging
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    reception_id = fields.Many2one('clinic.reception', string='Reception Reference', required=True)
    patient_id = fields.Many2one(related='reception_id.patient_name', string='Patient', store=True, readonly=True)
    date = fields.Date(string='Visit Date', default=fields.Date.context_today)
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
    technician_id = fields.Many2one('res.users', string="Technician", default=lambda self: self.env.user)
    notes = fields.Text(string="Technician Notes")
    
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