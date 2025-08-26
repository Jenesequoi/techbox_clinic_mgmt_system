from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ClinicMCH(models.Model):
    _name = 'clinic.mch'
    _description = 'Maternal and Child Health'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Basic Information
    name = fields.Char(string='MCH Reference', default=lambda self: _('New'), copy=False, readonly=True)
    reception_id = fields.Many2one(
        'clinic.reception',
        string='Reception Reference',
        required=True,
        ondelete='restrict'
    )
    department_id = fields.Many2one(
        'clinic.department',
        string='Department',
        required=True,
        ondelete='restrict'
    )
    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        related='reception_id.patient_name',
        store=True,
        readonly=True
    )
    doctor_id = fields.Many2one(
        'hr.employee',
        string='Doctor In Charge',
        required=True,
        help="Select the doctor responsible for this MCH visit"
    )
    date = fields.Date(
        string='Visit Date',
        default=fields.Date.context_today,
        required=True
    )
    service_type = fields.Selection([
        ('family_planning', 'Family Planning'),
        ('preconceptual', 'Preconceptual Care'),
        ('antenatal', 'Antenatal Care'),
        ('immunization', 'Immunization'),
        ('postnatal', 'Postnatal Care')
    ], string='Service Type', required=True, tracking=True)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting', tracking=True, group_expand='_expand_states')
    is_billed = fields.Boolean(string="Is Billed", default=False, readonly=True)

    # Family Planning Fields
    fp_method = fields.Selection([
        ('none', 'None'),
        ('implant', 'Implant'),
        ('pills', 'Oral Pills'),
        ('iud', 'IUD'),
        ('injection', 'Injectable'),
        ('condom', 'Condom'),
        ('natural', 'Natural Methods')
    ], string='Method Used')
    fp_advice_given = fields.Boolean(string='Counseling Provided')
    fp_advice_details = fields.Text(string='Counseling Details')
    fp_next_visit = fields.Date(string='Next Follow-up')

    # Preconceptual Care Fields
    pc_genetic_history = fields.Text(string='Genetic/Family History')
    pc_reproductive_history = fields.Text(string='Reproductive History')
    pc_environmental_hazards = fields.Text(string='Environmental Hazards')
    pc_special_diet = fields.Text(string='Special Diet')
    pc_weight = fields.Float(string='Weight (kg)')
    pc_physical_activity = fields.Text(string='Physical Activity')
    pc_substance_abuse = fields.Boolean(string='Substance Abuse')
    pc_medication = fields.Text(string='Current Medications')
    pc_oral_health = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ], string='Oral Health')
    pc_violence_screening = fields.Boolean(string='IPV Screening Done')
    pc_mental_health = fields.Text(string='Mental Health Notes')

    # Antenatal Care Fields
    anc_visit_number = fields.Selection([
        ('1', 'First Contact'),
        ('2', '12-20 Weeks'),
        ('3', '26 Weeks'),
        ('4', '30 Weeks'),
        ('5', '34 Weeks'),
        ('6', '36 Weeks'),
        ('7', '38 Weeks'),
        ('8', '40 Weeks')
    ], string='ANC Visit Number')
    anc_bp = fields.Char(string='Blood Pressure')
    anc_weight = fields.Float(string='Weight (kg)')
    anc_height = fields.Float(string='Height (cm)')
    anc_fundal_height = fields.Integer(string='Fundal Height (cm)')
    anc_fetal_heart_rate = fields.Integer(string='Fetal Heart Rate')
    anc_urine_test = fields.Text(string='Urine Test Results')
    anc_blood_test = fields.Text(string='Blood Test Results')
    anc_ultrasound = fields.Text(string='Ultrasound Findings')
    anc_education_given = fields.Text(string='Health Education Provided')
    anc_complications = fields.Text(string='Complications Identified')

    # Immunization Fields
    immunization_type = fields.Selection([
        ('bcg', 'BCG'),
        ('opv', 'OPV'),
        ('pentavalent', 'Pentavalent'),
        ('pcv', 'PCV'),
        ('rota', 'Rota'),
        ('measles', 'Measles'),
        ('yellow_fever', 'Yellow Fever'),
        ('tt', 'Tetanus Toxoid')
    ], string='Vaccine Given')
    immunization_dose = fields.Char(string='Dose Number')
    immunization_date = fields.Date(string='Date Given', default=fields.Date.context_today)
    immunization_next_date = fields.Date(string='Next Due Date')
    immunization_lot_number = fields.Char(string='Lot Number')
    immunization_site = fields.Selection([
        ('left_arm', 'Left Arm'),
        ('right_arm', 'Right Arm'),
        ('thigh', 'Thigh'),
        ('oral', 'Oral')
    ], string='Administration Site')
    immunization_provider = fields.Char(string='Provider Name')
    immunization_reaction = fields.Text(string='Adverse Reactions')
    immunization_reaction_management = fields.Text(string='Reaction Management')

    # Postnatal Care Fields
    pnc_visit_day = fields.Selection([
        ('0', 'Within 24 hours'),
        ('3', 'Day 3'),
        ('7', 'Week 1'),
        ('6', 'Week 6')
    ], string='PNC Visit Timing')
    pnc_mother_condition = fields.Text(string="Mother's Condition")
    pnc_mother_complications = fields.Text(string="Mother's Complications")
    pnc_baby_condition = fields.Text(string="Baby's Condition")
    pnc_baby_weight = fields.Float(string="Baby's Weight (kg)")
    pnc_baby_feeding = fields.Selection([
        ('exclusive_bf', 'Exclusive Breastfeeding'),
        ('mixed', 'Mixed Feeding'),
        ('formula', 'Formula Only')
    ], string='Feeding Method')
    pnc_breastfeeding = fields.Selection([
        ('established', 'Established'),
        ('difficulties', 'Experiencing Difficulties'),
        ('not_breastfeeding', 'Not Breastfeeding')
    ], string='Breastfeeding Status')
    pnc_breastfeeding_issues = fields.Text(string='Breastfeeding Issues')
    pnc_breastfeeding_support = fields.Text(string='Support Provided')
    pnc_family_planning = fields.Text(string='Family Planning Discussion')
    pnc_next_visit = fields.Date(string='Next PNC Visit')

    # Common Fields
    notes = fields.Text(string='Clinical Notes')
    next_visit = fields.Date(string='Next Appointment')
    follow_up_instructions = fields.Text(string='Follow-up Instructions')

    @api.model
    def create(self, vals):
        """Generate a unique reference for the MCH record"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('clinic.mch') or _('New')
        return super(ClinicMCH, self).create(vals)

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

    @api.onchange('service_type')
    def _onchange_service_type(self):
        """Reset service-specific fields when service type changes"""
        fields_to_reset = {
            'family_planning': ['fp_method', 'fp_advice_given', 'fp_advice_details', 'fp_next_visit'],
            'preconceptual': ['pc_genetic_history', 'pc_reproductive_history', 'pc_environmental_hazards', 
                             'pc_special_diet', 'pc_weight', 'pc_physical_activity', 'pc_substance_abuse', 
                             'pc_medication', 'pc_oral_health', 'pc_violence_screening', 'pc_mental_health'],
            'antenatal': ['anc_visit_number', 'anc_bp', 'anc_weight', 'anc_height', 'anc_fundal_height', 
                          'anc_fetal_heart_rate', 'anc_urine_test', 'anc_blood_test', 'anc_ultrasound', 
                          'anc_education_given', 'anc_complications'],
            'immunization': ['immunization_type', 'immunization_dose', 'immunization_date', 
                            'immunization_next_date', 'immunization_lot_number', 'immunization_site', 
                            'immunization_provider', 'immunization_reaction', 'immunization_reaction_management'],
            'postnatal': ['pnc_visit_day', 'pnc_mother_condition', 'pnc_mother_complications', 
                          'pnc_baby_condition', 'pnc_baby_weight', 'pnc_baby_feeding', 'pnc_breastfeeding', 
                          'pnc_breastfeeding_issues', 'pnc_breastfeeding_support', 'pnc_family_planning', 
                          'pnc_next_visit']
        }
        for field in fields_to_reset.get(self.service_type, []):
            self[field] = False

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
        """Create an invoice for the MCH visit using department's service product and price"""
        self.ensure_one()
        
        # Log for debugging
        _logger.info("Creating invoice for MCH ID: %s, Reference: %s, Department: %s, Service Product: %s, Service Price: %s",
                     self.id, self.name, self.department_id.name or 'None',
                     self.department_id.service_product_id.name or 'None',
                     self.department_id.service_price or 0.0)

        # Validate required fields
        if not self.patient_id:
            raise UserError(_("No patient is linked to this MCH visit. Please set a valid reception reference."))
        if not self.department_id:
            raise UserError(_("No department is selected for this MCH visit."))
        if not self.department_id.service_product_id:
            raise UserError(_("The department '%s' is missing a service product.") % self.department_id.name)
        if not self.department_id.service_price:
            raise UserError(_("The department '%s' is missing a service price.") % self.department_id.name)
        if not self.department_id.service_product_id.active:
            raise UserError(_("The service product '%s' is inactive.") % self.department_id.service_product_id.name)

        # Prepare invoice line
        invoice_line_vals = {
            'name': f'MCH Visit - {self.get_service_type_label()} ({self.department_id.name})',
            'quantity': 1.0,
            'price_unit': self.department_id.service_price,
            'product_id': self.department_id.service_product_id.id,
        }

        # Prepare invoice
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.id,
            'invoice_origin': self.name or f'MCH #{self.id}',
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
            'invoice_date': fields.Date.today(),
        }

        # Create invoice
        invoice = self.env['account.move'].sudo().create(invoice_vals)
        self.is_billed = True

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Invoice Created'),
                'message': _('Invoice %s has been created for this MCH visit.') % invoice.name,
                'type': 'success',
                'sticky': False,
            }
        }

    def action_view_invoice(self):
        """View the invoice associated with this MCH visit"""
        self.ensure_one()
        invoice = self.env['account.move'].search([('invoice_origin', '=', self.name or f'MCH #{self.id}')], limit=1)
        if invoice:
            return {
                'name': _('Customer Invoice'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
                'target': 'current',
            }
        raise UserError(_("No invoice found for this MCH visit."))

    def get_service_type_label(self):
        """Return the human-readable label for the service type"""
        return dict(self.fields_get(['service_type'])['service_type']['selection']).get(self.service_type, 'Unknown')