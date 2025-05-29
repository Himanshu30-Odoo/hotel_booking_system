# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo.tools.misc import xlwt
from io import BytesIO
import base64
from xlwt import easyxf
from odoo import fields, models, _
from datetime import datetime
import decimal
from bs4 import BeautifulSoup


class decoration_order_history_excel(models.TransientModel):
    _name ='booking.room.wizard'

    def room_booking_button(self):
        active_ids = self._context.get('active_ids')
        booking_ids = self.env['room.booking'].browse(active_ids)

        workbook = xlwt.Workbook()
        content = easyxf('font:height 200; font:bold True; pattern: pattern solid, fore_color gray25;  align: horiz left;')
        content_customer = easyxf('font:height 200;  align: horiz left;   ')
        content1 = easyxf('font:height 200; align: horiz left;  ')

        content_amount = easyxf('font:height 200; font:bold True; pattern: pattern solid, fore_color gray25; align: horiz right;  ')
        content1_amount = easyxf('font:height 200; align: horiz right;  ')
        content_add = easyxf('font:height 200; align: horiz left;  ')
        header_style = easyxf('font:height 300;pattern: pattern solid, fore_color gray25; align: horiz center;font:bold True;')
        content1_amount_bold = easyxf('font:height 200; align: horiz right;font:bold True;  ')
            
        for room_booking in booking_ids:
                worksheet = workbook.add_sheet(room_booking.name)
                worksheet.col(0).width = 900
                worksheet.col(1).width = 2000
                worksheet.col(2).width = 8400
                worksheet.col(3).width = 4800
                worksheet.col(4).width = 5000
                worksheet.col(5).width = 4400
                worksheet.col(6).width = 5000
                worksheet.col(7).width = 4400
                
        # worksheet.write_merge(2,3,2,4,'Client Order',header_style)
            
        # worksheet.write(5,1,"Customer Name",content)
        # worksheet.write(5,2,trainee_learner.name or '',content1)
        
        # worksheet.write(5,4,"Date Of Birth",content)
        # worksheet.write(5,5,trainee_learner.dob or '',content1)
        
        counter=1

        worksheet.write_merge(counter,counter+1,2,9,'Room Booking',header_style)
          
        counter += 4
               
        n_final_date = ' '
        if room_booking.check_in:
            final_date = datetime.strptime(str(room_booking.check_in), '%Y-%m-%d').date()
            n_final_date = final_date.strftime('%d-%m-%Y')
        worksheet.write(counter,3,"Check In :",content)
        worksheet.write(counter,4,n_final_date or '',content1)

        n_final_date = ' '
        if room_booking.check_out:
            final_date = datetime.strptime(str(room_booking.check_out), '%Y-%m-%d').date()
            n_final_date = final_date.strftime('%d-%m-%Y')
        worksheet.write(counter,6,"Check Out :",content)
        worksheet.write(counter,7,n_final_date or '',content1)

        counter +=4
        worksheet.write(counter,3,"Customer :",content)
        worksheet.write(counter,4,room_booking.guest_id.name or '',content1)
        worksheet.write(counter,6,"Total Amount :",content)
        worksheet.write(counter,7,room_booking.total_amount or '',content1)

        counter +=2
        worksheet.write(counter,3,"Gender :",content)
        worksheet.write(counter,4,room_booking.gender or '',content1)
        worksheet.write(counter,6,"Total Tax :",content)
        worksheet.write(counter,7,room_booking.tax_ids.name or '',content1)
        

        counter +=2
        worksheet.write(counter,3,"Room No. :",content)
        worksheet.write(counter,4,room_booking.room_id.name or '',content1)
        worksheet.write(counter,6,"Total Amount With Tax :",content)
        worksheet.write(counter,7,room_booking.amount_with_tax or '',content1)

        counter +=4
        worksheet.write(counter,2,"Description :",content)
        worksheet.write(counter,3,room_booking.description or '',content1)
       
    
        
        
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodebytes(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})
        active_id = self.ids[0]
        url = ('web/content/?model=booking.room.wizard&download=true&field=excel_file&id=%s&filename=%s' % (
        active_id, 'Room_Booking.xls'))
        if self.excel_file:
                return {'type': 'ir.actions.act_url',
                        'url': url,
                        'target': 'new'}

    excel_file = fields.Binary('Excel File')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
