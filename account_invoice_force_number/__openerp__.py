# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': "Force Invoice Number",
    'version': '0.3',
    'category': 'Generic Modules/Accounting',
    'description': """
    This module allows to force the invoice numbering.
    It displays the internal_number field. If user fills that field, the typed value will be used as invoice (and move) number. Otherwise, the next sequence number will be retrieved and saved.
    So, the new field has to be used when user doesn't want to use the default invoice numbering for a specific invoice.
    """,
    'author': 'Agile Business Group, Didotech SRL',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": ['account'],
    "init_xml": [],
    "update_xml": ['invoice_view.xml'],
    "demo_xml": [],
    "active": False,
    "installable": True
}
