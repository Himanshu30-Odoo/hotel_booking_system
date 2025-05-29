# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields,api
from datetime import date
from dateutil.relativedelta import relativedelta


class BookingWizard(models.TransientModel):
    _name = 'booking.wizard'


    start_date = fields.Date(string='Start Date',default=fields.Datetime.today(), required=True)
    end_date = fields.Date(string='End Date',default=fields.Datetime.today(), required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)


    def print_booking_report(self):
        return self.env.ref('hotel_booking_system.booking_report_menu').report_action(self)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
