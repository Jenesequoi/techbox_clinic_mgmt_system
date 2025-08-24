from odoo import models, fields, api

class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Patient Information"

    # Link to res.partner (patient must be a partner)
    partner_id = fields.Many2one(
        "res.partner", string="Patient", required=True, ondelete="cascade"
    )
    name = fields.Char(related="partner_id.name", store=True, readonly=True)

    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    # Contact Info (from partner)
    phone = fields.Char(related="partner_id.phone", store=True, readonly=False)
    email = fields.Char(related="partner_id.email", store=True, readonly=False)
    address = fields.Char(related="partner_id.contact_address", readonly=True)

    # Medical History: linked to consultations instead of text
    consultation_ids = fields.One2many(
        "clinic.consultation", "patient_id", string="Medical History"
    )

    # Extra clinical info
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], string="Blood Group")
    allergies = fields.Text(string="Allergies")
    chronic_conditions = fields.Text(string="Chronic Conditions")
    current_medication = fields.Text(string="Current Medication")

    # Emergency contact
    emergency_contact_name = fields.Char(string="Emergency Contact Name")
    emergency_contact_phone = fields.Char(string="Emergency Contact Phone")
    emergency_contact_relation = fields.Char(string="Relationship")

    # Insurance
    insurance_provider = fields.Char(string="Insurance Provider")
    insurance_number = fields.Char(string="Insurance Number")

    # System fields
    date_created = fields.Datetime(string="Created On", default=fields.Datetime.now)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                birthdate = record.date_of_birth
                record.age = (
                    today.year - birthdate.year -
                    ((today.month, today.day) < (birthdate.month, birthdate.day))
                )
            else:
                record.age = 0
