# -*- coding: utf-8 -*-
# Filename: models/pharmacy_queue.py

from odoo import models, fields, api

class PharmacyQueue(models.Model):
    _name = 'pharmacy.queue'
    _description = 'Pharmacy Queue'
    _order = 'create_date asc'

    name = fields.Char(
        string="Queue ID", 
        required=True, 
        copy=False, 
        readonly=True, 
        default='New'
    )
    patient_id = fields.Many2one(
        'res.partner', 
        string='Patient', 
        required=True
    )
    prescription_id = fields.Many2one(
        'clinic.prescription', 
        string='Prescription', 
        required=True
    )
    doctor_id = fields.Many2one(
        'res.users', 
        string='Prescribing Doctor', 
        required=True
    )
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled')
    ], 
        string='Status', 
        default='waiting'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pharmacy.queue') or 'New'
        return super(PharmacyQueue, self).create(vals)
