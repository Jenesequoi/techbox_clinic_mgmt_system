from odoo import models, fields, api

class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Patient Information"

    # Basic patient info
    name = fields.Char(string="Full Name", required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    # Optional reference fields
    address = fields.Text(string="Address")
    medical_history = fields.Text(string="Medical History")

    # Automatic creation date
    date_created = fields.Datetime(string="Created On", default=fields.Datetime.now)

    # Example of a computed field
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                birthdate = record.date_of_birth
                record.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            else:
                record.age = 0

