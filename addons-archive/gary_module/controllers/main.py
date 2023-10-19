from odoo import _
from odoo.http import Controller, Response, request, route
from odoo.tools import date_utils
import json
import logging

_logger = logging.getLogger(__name__)

class StudentController(Controller):
    @route('/student/all', methods=['GET'], type='http', auth='public', cors='*', csrf=False)
    def get_student_list(self):

        # logger 
        _logger.info('----get_student_list for logger test-----> \n')

        # controller 
        data = []
        students = request.env['res.student'].sudo().search([])
        for student in students:
            val = {
                'id': student.id,
                'name': student.name,
                'nickname': student.nickname,
                'gender': student.gender
            }
            data.append(val)
        result = {'data': data}
        body = json.dumps(result, default=date_utils.json_default)
        return Response(
            body, status=200,
            headers=[('Content-Type', 'application/json'), ('Content-Length', len(body))]
        )  

    @route('/student', methods=['POST'], type='json', auth='public', cors='*', csrf=False)
    def create_student(self):

        # logger 
        _logger.info('----create_student-----> %s \n', request.httprequest.data)

        # controller 
        student_data = json.loads(request.httprequest.data)
        val = {
            'name': student_data.get('name'),
            'nickname': student_data.get('nickname'),
            'gender': student_data.get('gender'),
            'birthday': student_data.get('birthday')
        }

        student_obj = request.env['res.student'].sudo()
        student_obj.create(val)
        result = {'code': 200, 'message': 'Created Successfully'}
        body = json.dumps(result, default=date_utils.json_default)
        return Response(
            body, status=200,
            headers=[('Content-Type', 'application/json'), ('Content-Length', len(body))]
        )