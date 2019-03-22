# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Didotech srl (<http://www.didotech.com>)
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Payments Due list",
    'version': '3.7.12.17',
    'category': 'Generic Modules/Payment',
    'description': """A due list of pending payments. The list contains every expected payment, generated by invoices. The list is fully filterable.""",
    'author': 'Didotech srl, Agile Business Group, Zikzakmedia SL',
    'website': 'http://www.didotech.com',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'report_webkit'
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/payment_view.xml',
        'views/move_view.xml',
        'views/partner_view.xml',
        'views/account_invoice_view.xml',
        'reports/reports.xml',
    ],
    "demo": [],
    "active": False,
    "installable": True
}
