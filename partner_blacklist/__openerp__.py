# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Didotech Srl ( info @ didotech.com). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Partner Blacklist and Color',
    'version': '1.2',
    'category': 'Generic Modules/Others',
    'description': """
	    Aggiunge un campo per indicare i partner bloccati
	""",
    'author': 'Didotech SRL',
    'website': 'www.didotech.com/',
    'depends': [
        'base',
        'sale',
        'purchase',
        'warning',
        'account_due_list',
        'res_users_helper_functions'
    ],
    'data': [
        'views/partner_view.xml',
        'security/security.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
