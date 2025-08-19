from odoo import models, fields, api
from datetime import timedelta

class ClinicMCH(models.Model):
    _name = 'clinic.mch'
    _description = 'Maternal and Child Health'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Basic Information
    reception_id = fields.Many2one(
        'clinic.reception',
        string='Reception Reference',
        required=True,
        ondelete='cascade'
    )
    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        related='reception_id.patient_name',
        store=True,
        readonly=True
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

    # ========== Family Planning Fields ==========
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

    # ========== Preconceptual Care Fields ==========
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

    # ========== Antenatal Care Fields ==========
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

    # ========== Immunization Fields ==========
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

    # ========== Postnatal Care Fields ==========
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

    @api.onchange('service_type')
    def _onchange_service_type(self):
        """Reset fields when service type changes"""
        fields_to_reset = {
            'family_planning': ['fp_method', 'fp_advice_given', 'fp_advice_details'],
            'preconceptual': ['pc_genetic_history', 'pc_reproductive_history'],
            'antenatal': ['anc_visit_number', 'anc_bp'],
            'immunization': ['immunization_type', 'immunization_dose'],
            'postnatal': ['pnc_visit_day', 'pnc_mother_condition']
        }
        
        for field in fields_to_reset.get(self.service_type, []):
            self[field] = False