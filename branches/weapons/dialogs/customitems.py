# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import models
import rules
from PySide import QtCore, QtGui

def grouped_widget(title, widget, parent = None):
    grp     = QtGui.QGroupBox(title, parent)
    vbox    = QtGui.QVBoxLayout(grp)
    vbox.addWidget(widget)
    
    return grp

class CustomArmorDialog(QtGui.QDialog):
    def __init__(self, pc, parent = None):
        super(CustomArmorDialog, self).__init__(parent)
        self.pc  = pc
        self.item = None
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        self.setWindowTitle("Add Custom Armor")
            
        self.setMinimumSize(400, 0)
                        
        self.bt_accept = QtGui.QPushButton('Ok'    , self)
        self.bt_cancel = QtGui.QPushButton('Cancel', self)            
        
        lvbox = QtGui.QVBoxLayout(self)
        self.tx_name = QtGui.QLineEdit(self)           
        lvbox.addWidget(grouped_widget("Name", self.tx_name, self))

        self.tx_tn = QtGui.QLineEdit(self)                
        self.tx_rd = QtGui.QLineEdit(self) 
        fr      = QtGui.QFrame(self)
        hbox    = QtGui.QHBoxLayout(fr)
        hbox.addWidget(grouped_widget("Armor TN", self.tx_tn, self))
        hbox.addWidget(grouped_widget("Reduction", self.tx_rd, self))      
        lvbox.addWidget(fr)
        
        self.tx_notes = QtGui.QTextEdit(self)         
        lvbox.addWidget(grouped_widget("Notes", self.tx_notes, self))
        
        self.btbox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.btbox.addButton(self.bt_accept, QtGui.QDialogButtonBox.AcceptRole)
        self.btbox.addButton(self.bt_cancel, QtGui.QDialogButtonBox.RejectRole)
        
        self.btbox.accepted.connect(self.on_accept)
        self.btbox.rejected.connect(self.close    )
        
        lvbox.addWidget(self.btbox)
        
    def load_data(self):
        if self.pc.armor is None:
            return
        self.tx_name .setText(self.pc.armor.name    )
        self.tx_tn   .setText(str(self.pc.armor.tn) )
        self.tx_rd   .setText(str(self.pc.armor.rd) )
        self.tx_notes.setText(self.pc.armor.desc)
            
    def on_accept(self):
        self.item = models.ArmorOutfit()
        try:
            self.item.tn   = int(self.tx_tn.text())
            self.item.rd   = int(self.tx_rd.text())
        except:
            self.item.tn   = 0
            self.item.rd   = 0
        
        self.item.name = self.tx_name.text()
        self.item.desc = self.tx_notes.toPlainText()
        
        if self.item.name == '':
            QtGui.QMessageBox.warning(self, "Custom Armor",
                                      "Please enter a name.")
            return
        
        self.pc.armor = self.item
        self.accept()

class CustomWeaponDialog(QtGui.QDialog):
    def __init__(self, pc, db, parent = None):
        super(CustomWeaponDialog, self).__init__(parent)
        self.pc  = pc
        self.db  = db
        self.item = None
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        self.setWindowTitle("Add Custom Weapon")
            
        self.setMinimumSize(400, 0)
                        
        self.bt_accept = QtGui.QPushButton('Ok'    , self)
        self.bt_cancel = QtGui.QPushButton('Cancel', self)            
        
        # Weapon Name
        lvbox = QtGui.QVBoxLayout(self)
        self.tx_name = QtGui.QLineEdit(self)           
        lvbox.addWidget(grouped_widget("Name", self.tx_name, self))
        
        # Base Weapon
        self.cb_base_weap = QtGui.QComboBox(self)
        lvbox.addWidget(grouped_widget("Base Weapon", self.cb_base_weap, self))        
        self.cb_base_weap.currentIndexChanged.connect( self.on_base_weap_change )
        
        # Stats
        stats_fr = QtGui.QFrame(self)
        form_lo  = QtGui.QFormLayout(stats_fr)        
        
        self.tx_dr      = QtGui.QLineEdit(self)
        self.tx_dr_alt  = QtGui.QLineEdit(self)
        self.tx_rng     = QtGui.QLineEdit(self)
        self.tx_str     = QtGui.QLineEdit(self)
        self.tx_min_str = QtGui.QLineEdit(self)
        
        form_lo.addRow("Primary DR"     , self.tx_dr)
        form_lo.addRow("Secondary DR"   , self.tx_dr_alt)
        form_lo.addRow("Range"          , self.tx_rng)
        form_lo.addRow("Weapon Strength", self.tx_str)
        form_lo.addRow("Min. Strength"  , self.tx_min_str)
        
        lvbox.addWidget(grouped_widget("Stats", stats_fr, self))
        
        self.tx_notes = QtGui.QTextEdit(self)         
        lvbox.addWidget(grouped_widget("Notes", self.tx_notes, self))
        
        self.btbox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.btbox.addButton(self.bt_accept, QtGui.QDialogButtonBox.AcceptRole)
        self.btbox.addButton(self.bt_cancel, QtGui.QDialogButtonBox.RejectRole)
        
        self.btbox.accepted.connect(self.on_accept)
        self.btbox.rejected.connect(self.close    )
        
        lvbox.addWidget(self.btbox)
        
    def load_data(self):
        c = self.db.cursor()
        
        c.execute('''select uuid, name from weapons''')
                     
        for uuid, name in c.fetchall():
            self.cb_base_weap.addItem(name, uuid)
        
        c.close()

    def on_base_weap_change(self, text = ''):        
        selected = self.cb_base_weap.currentIndex()
        if selected < 0:
            return
            
        weap_uuid = self.cb_base_weap.itemData(selected)
        itm       = models.weapon_outfit_from_db(self.db, weap_uuid)
        
        self.tx_str    .setText( str(itm.strength) )
        self.tx_min_str.setText( str(itm.min_str)  )

        self.tx_dr     .setText( itm.dr     )
        self.tx_dr_alt .setText( itm.dr_alt )               
        self.tx_rng    .setText( itm.range  )
        self.tx_name   .setText( itm.name   )
        self.tx_notes  .setText( itm.rule   )
        
    def on_accept(self):
        self.item = models.WeaponOutfit()
        
        def _try_get_int(widget):            
            try: 
                return int(widget.text()) 
            except: 
                return 0
                
        def _try_get_dr(widget):
            text = widget.text()
            r, k = rules.parse_rtk(text)
            return rules.format_rtk(r,k)
        
        self.item.strength = _try_get_int(self.tx_str     )
        self.item.min_str  = _try_get_int(self.tx_min_str )

        self.item.dr     = _try_get_dr(self.tx_dr    )
        self.item.dr_alt = _try_get_dr(self.tx_dr_alt)
        self.item.range  = self.tx_rng  .text()      
        self.item.name   = self.tx_name .text()
        self.item.desc   = self.tx_notes.toPlainText()
        
        if self.item.name == '':
            QtGui.QMessageBox.warning(self, "Custom Weapon",
                                      "Please enter a name.")
            return
        
        self.pc.add_weapon( self.item )
        self.accept()
        