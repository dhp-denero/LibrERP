# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 ISA s.r.l. (<http://www.isa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Account Central Journal',
    'version': '3.1.3.0.1',
    'author': "ISA S.r.l.,Odoo Community Association (OCA)",
    'website': 'http://www.isa.it',
    'category': 'Generic Modules/Accounting',
    'description': """
Managing the printing of the "Central Journal" """,
    'depends': [
        'base',
        'account',
        'report_webkit'
    ],
    'init_xml': [],
    'update_xml': [
        'report/webkit_model.xml',
        'report/report.xml',
        'wizard/central_journal_report.xml',
        'account_view.xml'
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': ''
}
