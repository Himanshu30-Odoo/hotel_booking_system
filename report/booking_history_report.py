

# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class ReportBooking(models.AbstractModel):
    _name = 'report.hotel_booking_system.practice_template1'


    def booking_history(self, obj):
        domain = [('booking_date','>=',obj.start_date),('booking_date','<=',obj.end_date)]     
        records = self.env['room.booking'].search(domain)
        return records  

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['booking.wizard'].browse(docids)
        booking_history = self.booking_history(docs[0])
        return {
            'doc_ids': docs.ids,
            'doc_model': 'booking.wizard',
            'docs': docs,
            'booking_history':self.booking_history,
        }

    
      
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:




