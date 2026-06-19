from odoo import fields, models


class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(string='Course Name', required=True, index=True)
    code = fields.Char(string='Course Code', required=True, index=True)
    description = fields.Text(string='Description')
    duration_weeks = fields.Integer(string='Duration (Weeks)', default=8)
    is_active = fields.Boolean(string='Active', default=True)
