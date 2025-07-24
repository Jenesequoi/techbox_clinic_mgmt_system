from odoo import models, fields, api, tools
from datetime import datetime, timedelta

class ClinicDashboard(models.Model):
    _name = 'clinic.dashboard'
    _description = 'Clinic Dashboard'
    _auto = False  # This is a database view

    name = fields.Char(string='Service Type', readonly=True)
    total_appointments = fields.Integer(string='Total Appointments', readonly=True)
    completed_appointments = fields.Integer(string='Completed Appointments', readonly=True)
    today_appointments = fields.Integer(string='Today\'s Appointments', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    service = fields.Selection([
        ('consultation', 'Consultation'),
        ('mch', 'MCH'),
        ('pharmacy', 'Pharmacy')
    ], string='Service', readonly=True)

    def init(self):
        """Initialize the database view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("DROP TABLE IF EXISTS %s CASCADE" % (self._table,))
        
        query = """
            CREATE VIEW %s AS (
                WITH appointments AS (
                    SELECT 
                        id,
                        service,
                        date,
                        CASE WHEN date = CURRENT_DATE THEN 1 ELSE 0 END as is_today
                    FROM clinic_reception
                )
                SELECT
                    ROW_NUMBER() OVER () as id,
                    service as name,
                    service,
                    date,
                    COUNT(*) as total_appointments,
                    SUM(CASE WHEN is_today = 1 THEN 1 ELSE 0 END) as today_appointments,
                    0 as completed_appointments
                FROM appointments
                GROUP BY service, date
            )
        """
        self.env.cr.execute(query % self._table)

    @api.model
    def get_dashboard_data(self):
        """Get aggregated dashboard data"""
        today = fields.Date.today()
        domain = [('date', '=', today)]
        
        dashboard_data = {
            'today_total': self.env['clinic.reception'].search_count(domain),
            'today_by_service': {},
            'week_trend': [],
        }

        # Get appointments by service for today
        for service in dict(self._fields['service'].selection):
            count = self.env['clinic.reception'].search_count(domain + [('service', '=', service)])
            dashboard_data['today_by_service'][service] = count

        # Get last 7 days trend
        for i in range(7):
            date = today - timedelta(days=i)
            count = self.env['clinic.reception'].search_count([('date', '=', date)])
            dashboard_data['week_trend'].append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })

        return dashboard_data
