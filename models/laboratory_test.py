from odoo import models, fields, api, _

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
    
    