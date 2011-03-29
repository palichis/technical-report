# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2010 SIA "KN dati". (http://kndati.lv) All Rights Reserved.
#                    General contacts <info@kndati.lv>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from report import report_sxw
import time 
import tools
import pdb
from lxml import etree


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
                'informes': self._get_informes,
                'get_campos':  self._get_campos,
                'get_menus' : self._get_menus,
                'get_help' : self._get_help,
                'get_wizard' : self._get_wizard,
                })

    def _get_menus(self,objeto):
        menu = {}
        res = ""
        model_ids = self.pool.get('ir.actions.act_window').search(self.cr,self.uid,[('res_model','=', objeto)])
        for model in model_ids:
            values_ids = self.pool.get('ir.values').search(self.cr, self.uid,[('value','=', 'ir.actions.act_window,' + str(model))])
            if values_ids:
                values_ids = values_ids[0]
                values_obj = self.pool.get('ir.values').browse(self.cr, self.uid,values_ids)
                if values_obj.res_id:
                    menu_obj = self.pool.get('ir.ui.menu').browse(self.cr, self.uid,values_obj.res_id)
                    if menu_obj:
                        res = menu_obj.name
                        while menu_obj.parent_id:
                            menu_obj = self.pool.get('ir.ui.menu').browse(self.cr, self.uid,menu_obj.parent_id.id)
                            res = menu_obj.name + "/"+ res
            menu[res] = res
        vector = []
        for men in menu:
            vector.append(men)
        vector.sort()
        return vector
        
        
    def _get_informes(self,obj):
        info_obj=self.pool.get('ir.actions.report.xml')
        info_ids = info_obj.search(self.cr,self.uid,[('model','=',obj)])
        if info_ids:
            informes = info_obj.read(self.cr,self.uid,info_ids,[])
            return informes
        return []

    def _get_help(self,obj,campo):
        modobj = self.pool.get(obj)
        res = modobj.fields_get(self.cr, self.uid,fields=campo).items()
        try:
            return res[0][1]['help']
        except:
            return []

    def _get_campos(self, xml):        
        tree = etree.XML(xml)
        print tree.iter()
        dic = []
        for e in tree.iter():
            dic.append('\n')
            if e.get('position'):
                if e.get('name'):
                    dic.append(e.get('name')+ " inherit " + e.get('position')) 
            else:
                if e.get('name'):
                    dic.append(' '+e.get('name')+',')
        for i in range(dic.count(None)):
            dic.remove(None)
        return dic

    def _get_wizard(self, xml):        
        tree = etree.XML(xml)
        print tree.iter()
        dic = []
        for e in tree.iter():
            dic.append('\n')
            if e.get('position'):
                if e.get('name'):
                    dic.append(e.get('name')+ " inherit " + e.get('position')) 
            else:
                if e.get('name'):
                    dic.append(' '+e.get('name')+',')
        for i in range(dic.count(None)):
            dic.remove(None)
        return True
   

