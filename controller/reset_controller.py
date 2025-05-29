from odoo import http
from odoo.http import request

class HotelRoomResetController(http.Controller):

    @http.route('/reset/rooms', type='json', auth='user')
    def reset_rooms(self):
        rooms = request.env['hotel.room'].sudo().search([])
        for room in rooms:
            room.write({'status': 'available'})
        return {'status': 'success', 'message': 'All rooms reset to available.'}
