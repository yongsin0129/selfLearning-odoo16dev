from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ResStudent(models.Model):
    _name = 'res.student'
    # _inherit = 'res.partner'
    _description = 'Student'

    name = fields.Char(string='大名')
    nickname = fields.Char(string='綽號')
    math_score = fields.Float(string='數學成績')
    chinese_score = fields.Float(string='國文成績')
    avg_score = fields.Float(string='學期平均', compute='_compute_score')
    birthday = fields.Date(string='生日', required=True)
    school_id = fields.Many2one('res.company', string='所屬學校')
    school_city = fields.Char(string='所在城市', related='school_id.city')
    senior_id = fields.Many2one('res.student', string='直屬學長姐')
    junior_ids = fields.One2many('res.student', 'senior_id', string='直屬學弟妹')
    teacher_ids = fields.Many2many('res.partner', string='指導老師', domain=[('is_company', '!=', True)])
    gender = fields.Selection([("male", "男"), ("female", "女"), ("other", "其他")], string='性別')
    is_leadership = fields.Boolean(default=False)
    is_active = fields.Boolean(default=True)
    # channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id', copy=False)

    @api.depends('math_score', 'chinese_score')
    def _compute_score(self):
        for record in self:
            record.avg_score = (record.math_score + record.chinese_score) / 2

    @api.onchange('school_id')
    def _onchange_shcool(self):
        for record in self:
            record.school_city = record.school_id.city

    @api.constrains('math_score', 'chinese_score')
    def _validate_score(self):
        for record in self:
            if record.math_score < 0 or record.chinese_score < 0:
                raise ValidationError(_("分數必須大於零"))

    @api.model
    def create(self, values):
        if values.get('is_active') is False:
            values.update({
                'is_leadership': False
            })
        return super(ResStudent, self).create(values)