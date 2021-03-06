# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import MissingError, ValidationError ,except_orm


class ScanBarcodeServiceCardUsingLine(models.TransientModel):
    _name = 'scan.barcode.izi.service.card.using.line'

    name = fields.Char(string="Name")
    message = fields.Text(string="Message")
    upper_waist = fields.Float(string='Upper of Waist')  # eo trên
    lower_waist = fields.Float(string='Lower of Waist')  # eo dưới
    middle_waist = fields.Float(string='Middle Waist')  # eo giữa
    arm = fields.Float(string='Arm')  # bắp tay
    right_upper_thighs = fields.Float(string='Right Upper Thigh')  # bắp đùi phải trên
    left_upper_thighs = fields.Float(string='Left Upper Thigh')  # bắp đùi trái trên
    right_lower_thighs = fields.Float(string='Right lower Thigh')  # bắp đùi phải dưới
    left_lower_thighs = fields.Float(string='Left lower Thigh')  # bắp đùi trái dưới
    flank = fields.Float(string='Flank')  # hông
    armpit = fields.Float(string='Armpit')  # Nách
    lats = fields.Float(string='Lats')  # xoài
    back = fields.Float(string='Back')  # lưng
    weight = fields.Float(string='Weight')  # cân nặng
    high = fields.Float(string='High')  # chiều cao
    upper_abdomen = fields.Float(string='Upper Abdomen')  # bụng trên
    middle_abdomen = fields.Float(string='Middle Abdomen')  # bụng giữa
    abdomen = fields.Float(string='Abdomen')  # bụng dưới
    right_upper_calf = fields.Float(string='Right Upper Calf')  # bắp chan phải trên
    left_upper_calf = fields.Float(string='Left Upper Calf')  # bắp chan phải trên
    right_lower_calf = fields.Float(string='Right Lower Calf')  # bắp chan phải trên
    left_lower_calf = fields.Float(string='Left Lower Calf')  # bắp chan phải trên
    measurement_time = fields.Datetime(string='Measurement  time', default=lambda self: fields.Datetime.now())  # Thời gian đo
    technician = fields.Many2one('hr.employee', string='Technicain')  # Kỹ thuật viên
    note = fields.Char(string='Note')
    check_invisible_therapy_body = fields.Boolean(default=False)

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            try:
                using_line_id = int(self.name)
                if using_line_id < -2147483648 or using_line_id > 2147483647:  # kiểm tra dữ liệu nhập có lớn hơn giá trị tối đa của int4
                    return {
                        'value': {
                            'name': False,
                            'message': 'Mã nhập không hợp lệ, liên hệ Admin! [%s]' % (str(self.name))
                        }
                    }
                ObjUsingLine = self.env['izi.service.card.using.line']
                using_line = ObjUsingLine.search([('id', '=', int(self.name))])
                if using_line:
                    str_body_area = ''
                    str_bed = ''
                    str_employee = ''
                    str_service = '[%s]%s' % (str(using_line.service_id.default_code), str(using_line.service_id.name))
                    str_customer = str(using_line.using_id.customer_id.name)
                    for bed in using_line.bed_ids:
                        str_bed += '[%s]%s, ' % (str(bed.room_id.name), str(bed.name))
                    for employee in using_line.employee_ids:
                        str_employee += '%s, ' % (str(employee.name))
                    if using_line.body_area_ids:
                        for body_area in using_line.body_area_ids:
                            str_body_area += '%s, ' % (str(body_area.name))
                    if using_line.state == 'new':
                        if using_line.service_id.x_is_massage or using_line.service_id.x_is_injection:
                            message = 'Bắt đầu làm dịch vụ!\n' \
                                      'Dịch vụ: %s\n' \
                                      'Khách hàng: %s\n' \
                                      'Giường: %s\n' \
                                      'Vùng cơ thể thực hiện: %s\n' \
                                      'Nhân viên làm: %s' % (
                                      str(str_service), str(str_customer), str(str_bed), str(str_body_area), str(str_employee))
                        else:
                            message = 'Bắt đầu làm dịch vụ!\n' \
                                      'Dịch vụ: %s\n' \
                                      'Khách hàng: %s\n' \
                                      'Giường: %s\n' \
                                      'Nhân viên làm: %s' % (str(str_service), str(str_customer), str(str_bed), str(str_employee))
                        using_line.action_confirm_bed()
                        self.check_invisible_therapy_body = False
                        self.name = False
                    elif using_line.state == 'working':
                        if using_line.service_id.product_tmpl_id.x_measure_ok:
                            self.check_invisible_therapy_body = True
                            message = False
                            therapy_record = self.env['therapy.record'].search(
                                [('id', '=', using_line.therapy_record_id.id)])
                            if therapy_record:
                                query = """
                                        SELECT * FROM  therapy_body_measure WHERE therapy_record_id = %s ORDER BY measurement_time DESC
                                        """
                                self._cr.execute(query, ([therapy_record.id]))
                                res = self._cr.dictfetchall()
                                for therapy_body in res:
                                    technician = therapy_body['technician']
                                    self.technician = technician
                                    break
                            self.measurement_time = datetime.now()
                        else:
                            self.check_invisible_therapy_body = False
                            if using_line.service_id.x_is_massage or using_line.service_id.x_is_injection:
                                message = 'Hoàn thành làm dịch vụ!\n' \
                                          'Dịch vụ: %s\n' \
                                          'Khách hàng: %s\n' \
                                          'Giường: %s\n' \
                                          'Vùng cơ thể thực hiện: %s\n' \
                                          'Nhân viên làm: %s' % (
                                              str(str_service), str(str_customer), str(str_bed), str(str_body_area),
                                              str(str_employee))
                            else:
                                message = 'Hoàn thành làm dịch vụ!\n' \
                                          'Dịch vụ: %s\n' \
                                          'Khách hàng: %s\n' \
                                          'Giường: %s\n' \
                                          'Nhân viên làm: %s' % (
                                          str(str_service), str(str_customer), str(str_bed), str(str_employee))
                            using_line.action_done()
                            self.name = False
                    elif using_line.state == 'done':
                        message = 'Công việc này đã hoàn thành, vui lòng không quét mã!\n' \
                                  'Dịch vụ: %s\n' \
                                  'Khách hàng: %s\n' \
                                  'Giường: %s\n' \
                                  'Nhân viên làm: %s' % (str(str_service), str(str_customer), str(str_bed), str(str_employee))
                        self.name = False
                    else:
                        message = 'Trạng thái của công việc: %s' % (str(using_line.state))
                        self.name = False
                else:
                    message = 'Không tìm thấy công việc có mã %s. Để nhanh chóng vui lòng liên hệ quầy để xác nhận công việc, hoặc kiểm tra lại quy trình in phiếu!' % (str(self.name))

                self.message = message
            except ValueError:
                return {
                    'value': {
                        'name': False,
                        'message': 'Chỉ nhập mã là chữ số!'
                    }
                }
        else:
            pass

    @api.multi
    def action_pass(self):
        using_line = self.env['izi.service.card.using.line'].search([('id', '=', int(self.name))])
        str_service = '[%s]%s' % (str(using_line.service_id.default_code), str(using_line.service_id.name))
        str_customer = str(using_line.using_id.customer_id.name)
        str_bed = ''
        for bed in using_line.bed_ids:
            str_bed += '[%s]%s, ' % (str(bed.room_id.name), str(bed.name))
        str_employee = ''
        for employee in using_line.employee_ids:
            str_employee += '%s, ' % (str(employee.name))
        message = 'Hoàn thành làm dịch vụ!\n' \
                  'Dịch vụ: %s\n' \
                  'Khách hàng: %s\n' \
                  'Giường: %s\n' \
                  'Nhân viên làm: %s' % (
                      str(str_service), str(str_customer), str(str_bed), str(str_employee))
        using_line.action_done()
        self.name = False
        self.message = message
        self.check_invisible_therapy_body = False

    @api.multi
    def confirm(self):
        if not self.technician:
            raise ValidationError('Bạn cần chọn người đo.')
        if not self.measurement_time:
            raise ValidationError('Bạn cần chọn ngày đo.')

        using_line = self.env['izi.service.card.using.line'].search([('id', '=', int(self.name))])
        if using_line.therapy_record_id:
        # therapy_prescription = self.env['therapy.prescription'].search([('id', '=', using_line.therapy_record_id.id)])
            therapy_body = self.env['therapy.body.measure']
            res = {
                'technician': self.technician.id,
                'measurement_time': self.measurement_time,
                'upper_waist': self.upper_waist,
                'lower_waist': self.lower_waist,
                'middle_waist': self.middle_waist,
                'arm': self.arm,
                'right_upper_thighs': self.right_upper_thighs,
                'left_upper_thighs': self.left_upper_thighs,
                'right_lower_thighs': self.right_lower_thighs,
                'left_lower_thighs': self.left_lower_thighs,
                'flank': self.flank,
                'armpit': self.armpit,
                'lats':self.lats,
                'back': self.back,
                'weight': self.weight,
                'high': self.high,
                'upper_abdomen': self.upper_abdomen,
                'middle_abdomen': self.middle_abdomen,
                'abdomen': self.abdomen,
                'right_upper_calf': self.right_upper_calf,
                'left_upper_calf': self.left_upper_calf,
                'right_lower_calf': self.right_lower_calf,
                'left_lower_calf': self.left_lower_calf,
                'measurement_time': self.measurement_time,
                'note': self.note,
                'therapy_record_id': using_line.therapy_record_id.id
            }
            therapy_body.create(res)
        self.technician = False
        self.upper_waist = False
        self.note = False
        self.measurement_time = False
        self.left_lower_calf = False
        self.right_lower_calf = False
        self.left_upper_calf = False
        self.right_upper_calf = False
        self.abdomen = False
        self.middle_abdomen = False
        self.upper_abdomen = False
        self.high = False
        self.back = False
        self.weight = False
        self.lats = False
        self.flank = False
        self.armpit = False
        self.left_lower_thighs = False
        self.right_lower_thighs = False
        self.arm = False
        self.middle_waist = False
        self.lower_waist = False
        self.right_upper_thighs = False
        self.left_upper_thighs = False

        self.action_pass()
