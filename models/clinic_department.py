from odoo import fields, models, api, _

class ClinicDepartment(models.Model):
    _name = 'clinic.department'
    _description = 'Clinic Department'
    _order = 'sequence, id'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
    
    
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Appointment Count')
    today_appointment_count = fields.Integer(compute='_compute_appointment_count', string='Today\'s Appointments')
    waiting_count = fields.Integer(compute='_compute_appointment_count', string='Waiting Count')
    completion_rate = fields.Float(compute='_compute_appointment_count', string='Completion Rate')

    @api.depends('code')
    def _compute_appointment_count(self):
        today = fields.Date.today()
        for department in self:
            domain = [('department_id', '=', department.id)]
            today_domain = domain + [('date', '=', today)]
            
            department.appointment_count = self.env['clinic.reception'].search_count(domain)
            today_appointments = self.env['clinic.reception'].search_count(today_domain)
            completed_appointments = self.env['clinic.reception'].search_count(today_domain + [('state', '=', 'completed')])
            waiting_appointments = self.env['clinic.reception'].search_count(today_domain + [('state', '=', 'waiting')])
            
            department.today_appointment_count = today_appointments
            department.waiting_count = waiting_appointments
            department.completion_rate = (completed_appointments / today_appointments * 100) if today_appointments > 0 else 0

    def action_view_appointments(self):
        return {
            'name': _('Department Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'tree,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id}
        }

    def action_view_today_appointments(self):
        return {
            'name': _('Today\'s Appointments'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'tree,form',
            'domain': [
                ('department_id', '=', self.id),
                ('date', '=', fields.Date.today())
            ],
            'context': {'default_department_id': self.id}
        }

    def action_department_stats(self):
        return {
            'name': _('Department Statistics'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'graph,pivot',
            'domain': [('department_id', '=', self.id)],
            'context': {'group_by': ['date:day']}
        }

    def action_department_report(self):
        return {
            'name': _('Department Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'clinic.reception',
            'view_mode': 'pivot',
            'domain': [('department_id', '=', self.id)],
            'context': {
                'group_by': ['date:month', 'state'],
                'pivot_measures': ['__count']
            }
        }
