# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011-2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Thanks to Antonio de Vincentiis http://www.devincentiis.it/ ,
#    GAzie http://gazie.sourceforge.net/
#    and Cecchi s.r.l http://www.cecchi.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

'''
*****************************************************************************************
 Questa classe genera il file RiBa standard ABI-CBI passando alla funzione "creaFile" i due array di seguito specificati:
$intestazione = array monodimensionale con i seguenti index:
              [0] = credit_sia variabile lunghezza 5 alfanumerico
              [1] = credit_abi assuntrice variabile lunghezza 5 numerico
              [2] = credit_cab assuntrice variabile lunghezza 5 numerico
              [3] = credit_conto conto variabile lunghezza 10 alfanumerico
              [4] = data_creazione variabile lunghezza 6 numerico formato GGMMAA
              [5] = nome_supporto variabile lunghezza 20 alfanumerico
              [6] = codice_divisa variabile lunghezza 1 alfanumerico opzionale default "E"
              [7] = name_company nome ragione sociale creditore variabile lunghezza 24 alfanumerico
              [8] = indirizzo_creditore variabile lunghezza 24 alfanumerico
              [9] = cap_citta_creditore variabile lunghezza 24 alfanumerico
              [10] = ref (definizione attivita) creditore
              [11] = codice fiscale/partita iva creditore alfanumerico opzionale

$ricevute_bancarie = array bidimensionale con i seguenti index:
                   [0] = numero ricevuta lunghezza 10 numerico
                   [1] = data scadenza lunghezza 6 numerico
                   [2] = importo in centesimi di euro
                   [3] = nome debitore lunghezza 60 alfanumerico
                   [4] = codice fiscale/partita iva debitore lunghezza 16 alfanumerico
                   [5] = indirizzo debitore lunghezza 30 alfanumerico
                   [6] = cap debitore lunghezza 5 numerico
                   [7] = citta debitore alfanumerico
                   [8] = debitor_province debitore alfanumerico
                   [9] = abi banca domiciliataria lunghezza 5 numerico
                   [10] = cab banca domiciliataria lunghezza 5 numerico
                   [11] = descrizione banca domiciliataria lunghezza 50 alfanumerico
                   [12] = codice cliente attribuito dal creditore lunghezza 16 numerico
                   [13] = numero fattura lunghezza 40 alfanumerico
                   [14] = data effettiva della fattura
                   [15] = CUP
                   [16] = CIG
'''

import base64
from openerp.osv import fields, orm
from openerp.tools.translate import _
from datetime import datetime


class riba_file_export(orm.TransientModel):
    def __init__(self, *args, **kwargs):
        super(riba_file_export, self).__init__(*args, **kwargs)
        self._progressivo = 0
        self._assuntrice = 0
        self._sia = 0
        self._data = 0
        self._valuta = 0
        self._supporto = 0
        self._totale = 0
        self._creditore = 0
        self._descrizione = ''
        self._codice = ''
        self._comune_provincia_debitor = ''

    def _RecordIB(self, sia_assuntrice, abi_assuntrice, data_creazione, nome_supporto, codice_divisa):  #record di testa
        self._sia = sia_assuntrice.rjust(5, '0')
        self._assuntrice = abi_assuntrice.rjust(5, '0')
        self._data = data_creazione.rjust(6, '0')
        self._valuta = codice_divisa[0:1]
        self._supporto = nome_supporto.ljust(20, ' ')
        return " IB" + self._sia + self._assuntrice + self._data + self._supporto + " " * 74 + self._valuta + " " * 6 + "\r\n"

    def _Record14(self, scadenza, importo, abi_assuntrice, cab_assuntrice, conto, abi_domiciliataria, cab_domiciliataria, sia_credit, codice_cliente):
        self._totale += importo
        return " 14" + str(self._progressivo).rjust(7, '0') + " " * 12 + scadenza + "30000" + str(int(round(importo * 100))).rjust(13, '0') + "-" + abi_assuntrice.rjust(5, '0') + cab_assuntrice.rjust(5,'0') + conto.ljust(12,'0') + abi_domiciliataria.rjust(5,'0') + cab_domiciliataria.rjust(5,'0') + " " * 12 + str(sia_credit).rjust(5,'0') + "4" + codice_cliente.ljust(16) + " " * 6 + self._valuta + "\r\n"

    def _Record20(self, ragione_soc1_creditore, indirizzo_creditore, cap_citta_creditore, ref_creditore,):
        self._creditore = ragione_soc1_creditore.ljust(24)
        return " 20" + str(self._progressivo).rjust(7, '0') + self._creditore[0:24] + indirizzo_creditore.ljust(24)[0:24] + cap_citta_creditore.ljust(24)[0:24]+ ref_creditore.ljust(24)[0:24]  + " " * 14 + "\r\n"

    def _Record30(self, nome_debitore, codice_fiscale_debitore):
        return " 30" + str(self._progressivo).rjust(7, '0') + nome_debitore.ljust(60)[0:60] + codice_fiscale_debitore.ljust(16, ' ') + " " * 34 + "\r\n"

    def _Record40(self, indirizzo_debitore, cap_debitore, comune_debitore, provincia_debitore, descrizione_domiciliataria=""):
        self._comune_provincia_debitor = comune_debitore + provincia_debitore.rjust(25-len(comune_debitore), ' ')
        return " 40" + str(self._progressivo).rjust(7, '0') + indirizzo_debitore.ljust(30)[0:30] + str(cap_debitore).rjust(5, '0') + self._comune_provincia_debitor + descrizione_domiciliataria.ljust(50)[0:50] + "\r\n"

    def _Record50(self, importo_debito, invoice_ref, data_invoice, partita_iva_creditore, cup, cig):
        self._descrizione = cup + cig + 'FT N. ' + invoice_ref + ' DEL ' + data_invoice #+ ' IMP '+ str(importo_debito)
        return " 50" + str(self._progressivo).rjust(7, '0') + self._descrizione.ljust(80)[0:80] + " " * 10 + partita_iva_creditore.ljust(16, ' ') + " " * 4 + "\r\n"

    def _Record51(self, numero_ricevuta_creditore):
        return " 51" + str(self._progressivo).rjust(7, '0') + str(numero_ricevuta_creditore).rjust(10, '0') + self._creditore[0:20] + " " * 80 + "\r\n"

    def _Record70(self):
        return " 70" + str(self._progressivo).rjust(7, '0') + " " * 110 + "\r\n"

    def _RecordEF(self):  # record di coda
        return " EF" + self._sia + self._assuntrice + self._data + self._supporto + " " * 6 + str(self._progressivo).rjust(7, '0') + str(int(round(self._totale * 100))).rjust(15, '0') + "0" * 15 + str(int(self._progressivo)*7+2).rjust(7,'0') + " " * 24 + self._valuta + " " * 6 + "\r\n"

    def _creaFile(self, intestazione, ricevute_bancarie):
        accumulatore = self._RecordIB(intestazione[0], intestazione[1], intestazione[4], intestazione[5],
                                      intestazione[6])
        for value in ricevute_bancarie:  # estraggo le ricevute dall'array
            self._progressivo += 1
            if not value[9] or not value[10]:
                raise orm.except_orm('Error', _('No ABI / CAB specified for bank in ') + value[3])
            accumulatore += self._Record14(
                value[1], value[2], intestazione[1], intestazione[2], intestazione[3], value[9], value[10],
                intestazione[0], value[12])
            accumulatore += self._Record20(intestazione[7], intestazione[8], intestazione[9],
                                           intestazione[10])
            accumulatore += self._Record30(value[3], value[4])
            accumulatore += self._Record40(value[5], value[6], value[7], value[8], value[11])
            accumulatore += self._Record50(value[2], value[13], value[14], intestazione[11], value[15],
                                           value[16])
            accumulatore += self._Record51(value[0])
            accumulatore += self._Record70()
        accumulatore += self._RecordEF()
        self._progressivo = 0
        self._totale = 0
        return accumulatore.replace(u'�', ' ')

    def encode_latin_1(self, text):
        text_latin_1 = ''
        for row in text.split('\n'):
            print(row)
            try:
                text += row.encode("iso-8859-1") + '\n'
            except UnicodeEncodeError:
                raise orm.except_orm(_('Error'), u"Row '{}' contains non ASCII charachters".format(row))

        return text_latin_1

    def act_getfile(self, cr, uid, ids, context=None):

        self._progressivo = 0
        self._assuntrice = 0
        self._sia = 0
        self._data = 0
        self._valuta = 0
        self._supporto = 0
        self._totale = 0
        self._creditore = 0
        self._descrizione = ''
        self._codice = ''
        self._comune_provincia_debitor = ''

        active_ids = context and context.get('active_ids', [])
        order_obj = self.pool['riba.distinta'].browse(cr, uid, active_ids, context=context)[0]
        credit_bank = order_obj.config.bank_id
        name_company = order_obj.config.company_id.partner_id.name
        if not credit_bank.iban:
            raise orm.except_orm('Error', _('No IBAN specified'))
        iban = credit_bank.iban.replace(" ", "")
        credit_abi = credit_bank.bank.abi or iban[-22:-17]
        credit_cab = credit_bank.bank.cab or iban[-17:-12]
        credit_conto = iban[-12:]
        if not credit_bank.codice_sia:
            raise orm.except_orm('Error', _('No SIA Code specified for: ') + name_company)
        credit_sia = credit_bank.codice_sia
        credit_account = iban[15:27]
        dataemissione = datetime.now().strftime("%d%m%y")
        nome_supporto = datetime.now().strftime("%d%m%y%H%M%S") + credit_sia
        creditor_address = order_obj.config.company_id.partner_id.address
        if not creditor_address[0].street:
            raise orm.except_orm('Error', _('No address specified for: ') + name_company)
        creditor_city = ''
        if creditor_address[0].city:
            creditor_city = creditor_address[0].city
        creditor_province = ''
        if creditor_address[0].province:
            creditor_province = creditor_address[0].province.code
        if not order_obj.config.company_id.partner_id.vat and not order_obj.config.company_id.partner_id.fiscalcode:
            raise orm.except_orm('Error', _('No VAT or Fiscalcode specified for: ') + name_company)
        array_testata = [
               credit_sia,
               credit_abi,
               credit_cab,
               credit_conto,
               dataemissione,
               nome_supporto,
               'E',
               name_company,
               creditor_address[0].street or '',
               creditor_address[0].zip and creditor_address[0].zip.replace('x', '0')[0:5] or '' + ' ' + creditor_city,
               order_obj.config.company_id.partner_id.ref or '',
               order_obj.config.company_id.partner_id.vat and order_obj.config.company_id.partner_id.vat[2:] or order_obj.config.company_id.partner_id.fiscalcode,
            ]
        arrayRiba = []
        for line in order_obj.line_ids:
            if line.state == 'unsolved':
                continue
            debit_abi = False
            debit_cab = False
            if line.bank_riba_id:
                debit_riba_bank = line.bank_riba_id
                if debit_riba_bank.abi and debit_riba_bank.cab:
                    debit_abi = debit_riba_bank.abi
                    debit_cab = debit_riba_bank.cab
                    if not debit_abi or not debit_cab:
                        raise orm.except_orm('Error', _('No bank or IBAN specified for ') + line.bank_riba_id.name)
                debit_bank_name = debit_riba_bank.name
            elif line.bank_id:
                debit_bank = line.bank_id
                if debit_bank.iban:
                    debit_iban = debit_bank.iban.replace(" ", "")
                    debit_abi = debit_iban[5:10]
                    debit_cab = debit_iban[10:15]
                    if not debit_abi or not debit_cab:
                        raise orm.except_orm('Error', _('No bank or IBAN specified for ') + debit_bank.name)

                debit_bank_name = debit_bank.bank.name or debit_bank.bank_name
            else:
                raise orm.except_orm('Error', _('No bank or IBAN specified for ') + line.partner_id.name)

            if not line.partner_id.address:
                raise orm.except_orm('Error', _('No address specified for ') + line.partner_id.name)
            debitor_address = line.partner_id.address
            if debitor_address[0].street:
                debitor_street = debitor_address[0].street
            else:
                raise orm.except_orm('Error', _('No Street specified for ') + line.partner_id.name)
            if debitor_address[0].zip:
                debitor_zip = debitor_address[0].zip.replace('x', '0')[0:5]
            else:
                raise orm.except_orm('Error', _('No CAP specified for ') + line.partner_id.name)
            # TODO search for bank_riba_id: if exists, use its abi cab
            
            if debitor_address[0].city:
                debitor_city = debitor_address[0].city.ljust(23)[0:23] or ''
            else:
                raise orm.except_orm('Error', _('No City specified for ') + line.partner_id.name)
            debitor_province = ''
            if debitor_address[0].province:
                debitor_province = debitor_address[0].province.code
            if not line.due_date:  # ??? VERIFICARE
                due_date = '000000'
            else:
                due_date = datetime.strptime(line.due_date[:10], '%Y-%m-%d').strftime("%d%m%y")

            if not line.partner_id.vat and not line.partner_id.fiscalcode:
                raise orm.except_orm('Error', _('No VAT or Fiscal code specified for ') + line.partner_id.name)
            if not debit_bank_name:  # .bank and debit_bank.bank.name or debit_bank.bank_name):
                raise orm.except_orm('Error', _('No debit_bank specified for ') + line.partner_id.name)
            cup = ''
            cig = ''
            if line.cup:
                cup = 'CUP: ' + str(line.cup)
            if line.cig:
                cig = ' CIG: ' + str(line.cig) + ' '
            Riba = [
                line.sequence,
                due_date,
                line.amount,
                line.partner_id.name,
                not line.partner_id.not_use_vat_on_riba and line.partner_id.vat and line.partner_id.vat[2:] or line.partner_id.fiscalcode,
                debitor_street,
                debitor_zip,
                debitor_city,
                debitor_province,
                debit_abi,
                debit_cab,
                debit_bank_name,  # .bank and debit_bank.bank.name or debit_bank.bank_name,
                line.partner_id.ref or '',
                # line.move_line_id.name,
                line.invoice_number,
                # datetime.strptime(line.distinta_id.date_created, '%Y-%m-%d').strftime("%d/%m/%Y"),
                line.invoice_date,
                cup,
                cig,
            ]

            if not debit_abi and not debit_cab:
                import pdb;pdb.set_trace()
            arrayRiba.append(Riba)

        # Uncomment this lines if you have problems with Unicode characters and want to know the line
        # (DEBUG only)
        # out = self.encode_latin_1(self._creaFile(array_testata, arrayRiba))
        # out = base64.encodestring(out)

        out = base64.encodestring(self._creaFile(array_testata, arrayRiba).encode("iso-8859-1"))
        file_name = '{0}.txt'.format(order_obj.name.replace(' ', '').replace('/', '_'))
        return self.write(cr, uid, ids, {'state': 'get', 'riba_export_file': out, 'riba_export_name': file_name}, context=context)

    _name = "riba.file.export"

    _columns = {
        'state': fields.selection((('choose', 'choose'),  # choose accounts
                                   ('get', 'get'),        # get the file
                                   )),
        'riba_export_file': fields.binary('File', readonly=True),
        'riba_export_name': fields.char('File Name', readonly=True)
    }
    _defaults = {
        'state': lambda *a: 'choose',
    }

