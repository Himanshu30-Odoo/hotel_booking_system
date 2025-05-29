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
from odoo.exceptions import ValidationError , UserError 

class report_room_booking(models.AbstractModel): 
    _name = 'report.hotel_booking_system.booking_template1'


    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['room.booking'].browse(docids)
        
        if not docs:
            raise UserError("No valid records found to generate the report.")

        print("docs=====",docs)
        return {
            'doc_ids': docs.ids,
            'doc_model':'room.booking',
            'docs': docs,
        }

    
      
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
