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


    ref = fields.Char(string='Visit_Id', required=True, copy=False)
    # patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    patient_name = fields.Many2one('res.partner', string='Patient', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', store=True, tracking=True)
    department_id = fields.Many2one('clinic.department', string='Department', required=True)
    service = fields.Char(related='department_id.code', store=True, string='Service Code')
    is_referral = fields.Boolean(string='Is Referral', default=False)
    referral_id = fields.Many2one('res.partner', string='Referral Doctor')
    guardian = fields.Many2one('res.partner', string='Guardian')
    is_married = fields.Boolean(string='Is Married', default=False)
    spouse = fields.Many2one('res.partner', string='Spouse', tracking=True)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting', tracking=True)

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
