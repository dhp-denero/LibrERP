# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020 Didotech S.r.l. (<http://www.didotech.com/>).
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
    "name": "Purchase Order Lines With Combined Discounts",
    "author": "Didotech.com",
    "version": "1.0.0",
    "category": "Generic Modules/Sales & Purchases",
    'description': """ """,
    "depends": [
        "stock",
        'product',
        "purchase",
        "purchase_discount",
    ],
    "data": [
        "views/purchase_discount_view.xml",
    ],
    "active": False,
    "installable": True
}
