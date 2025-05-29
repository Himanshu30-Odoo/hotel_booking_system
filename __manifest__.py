# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################


{
    'name': 'Hotel Booking System',
    'version': '17.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Tools',
    'description':
        """
        This Module add below functionality into odoo

        - Hotel Booking System\n

    """,
    'summary': 'Manage hotel rooms, bookings, and guests',
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['base', 'web','hr','mail','account','contacts','portal','website'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_generate.xml',
        'data/payment_templates.xml',
        'wizard/hotel_booking_views.xml',
        'views/hotel_room_views.xml',
        'views/room_booking_views.xml',
        'views/guest_views.xml',
        'views/facility_ticket_views.xml',
        'views/portal_template.xml',
        'views/portal_menu.xml',
        'wizard/booking_history.xml',
        'report/room_booking_report_views.xml',
        'report/room_booking_views.xml',
        'report/booking_history_report_menu.xml',
        'report/booking_history_report.xml',
        'views/hotel_room_template.xml',
        'views/room_booking_form.xml',
        'views/booking_confiormation_template.xml',
        'views/room_website_template.xml',
    ],

    # 'assets': {
    # 'web.assets_frontend': [
    #     # You can include CSS/JS here if needed
    # ],
    #         },


    'demo': [ ],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}





