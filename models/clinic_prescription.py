def action_confirm(self):
    # existing logic
    for record in self:
        self.env['pharmacy.queue'].create({
            'patient_id': record.patient_id.id,
            'prescription_id': record.id,
            'doctor_id': record.doctor_id.id,
        })
    return True
