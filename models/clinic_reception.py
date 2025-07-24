from odoo import fields, models, api, _
from datetime import datetime, date


class ClinicReception(models.Model):
    _name = 'clinic.reception'
    _description = 'Clinic Reception'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Computed fields for dashboard
    appointments_count = fields.Integer(compute='_compute_appointment_stats')
    completed_count = fields.Integer(compute='_compute_appointment_stats')
    waiting_count = fields.Integer(compute='_compute_appointment_stats')
    completion_rate = fields.Float(compute='_compute_appointment_stats')


    ref = fields.Char(string='Visit ID', readonly=True, copy=False, default='/')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    patient_name = fields.Many2one('res.partner', string='Patient', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True)
    department_id = fields.Many2one('clinic.department', string='Department', required=True)
    service = fields.Char(related='department_id.code', store=True, string='Service Code')
    complaint = fields.Text(string='Complaint', required=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'M-Pesa'),
        ('insurance', 'Insurance')
    ], string='Payment Method', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals.get('ref') == '/':
                department_id = vals.get('department_id')
                if not department_id:
                    raise ValueError(_('Department is required to generate visit ID.'))
                
                department = self.env['clinic.department'].browse(department_id)
                if not department:
                    raise ValueError(_('Invalid department selected.'))
                
                sequence_code = f'clinic.reception.{department.code}'
                sequence = self.env['ir.sequence'].sudo().next_by_code(sequence_code)
                
                if not sequence:
                    # Fallback to create sequence if it doesn't exist
                    self.env['ir.sequence'].sudo().create({
                        'name': f'{department.name} Visits',
                        'code': sequence_code,
                        'prefix': f'{department.code.upper()}/%(year)s/',
                        'padding': 5,
                        'number_next': 1,
                    })
                    sequence = self.env['ir.sequence'].sudo().next_by_code(sequence_code)
                
                if not sequence:
                    raise ValueError(_('Could not generate visit ID. Please check sequence configuration.'))
                
                vals['ref'] = sequence
        
        return super().create(vals_list)
    is_referral = fields.Boolean(string='Is Referral', default=False)
    referral_id = fields.Many2one('res.partner', string='Referral Healthcare Provider')
    guardian = fields.Many2one('res.partner', string='Guardian')
    is_married = fields.Boolean(string='Is Married', default=False)
    spouse = fields.Many2one('res.partner', string='Spouse', tracking=True)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting', tracking=True, group_expand='_expand_states')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset(self):
        self.write({'state': 'waiting'})
    
    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = date.today()
                dob = fields.Date.from_string(record.dob)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
            else:
                record.age = 0

    @api.depends('date', 'state', 'service')
    def _compute_appointment_stats(self):
        today = fields.Date.today()
        for record in self:
            # Get appointments for today for this service
            domain = [
                ('date', '=', today),
                ('service', '=', record.service)
            ]
            
            # Count total appointments
            record.appointments_count = self.search_count(domain)
            
            # Count completed appointments
            record.completed_count = self.search_count(domain + [('state', '=', 'completed')])
            
            # Count waiting appointments
            record.waiting_count = self.search_count(domain + [('state', '=', 'waiting')])
            
            # Calculate completion rate
            record.completion_rate = (record.completed_count / record.appointments_count * 100) if record.appointments_count > 0 else 0

    def action_view_today_appointments(self):
        self.ensure_one()
        return {
            'name': _('Today\'s Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'list,form',
            'domain': [
                ('date', '=', fields.Date.today()),
                ('service', '=', self.service)
            ],
            'context': {'default_service': self.service}
        }

    def action_department_stats(self):
        self.ensure_one()
        return {
            'name': _('Department Statistics'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'graph,pivot',
            'domain': [('service', '=', self.service)],
            'context': {'group_by': ['date:day']}
        }

    def action_department_report(self):
        self.ensure_one()
        return {
            'name': _('Department Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'pivot',
            'domain': [('service', '=', self.service)],
            'context': {
                'group_by': ['date:month', 'state'],
                'pivot_measures': ['appointments_count', 'completed_count']
            }
        }
