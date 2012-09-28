#!/usr/bin/python

from PySide import QtCore, QtGui
import rules
import models

class ChooseItemDialog(QtGui.QDialog):
    def __init__(self, pc, tag, conn, parent = None):
        super(ChooseItemDialog, self).__init__(parent)
        self.tag = tag
        self.adv = None
        self.pc  = pc
        self.dbconn = conn
        self.item = None
        self.build_ui()
        self.load_data()

    def build_ui(self):    
        # depending on the tag ( armor or weapon )
        # we build a different interface
        
        self.bt_accept = QtGui.QPushButton('Ok'    , self)
        self.bt_cancel = QtGui.QPushButton('Cancel', self)
        
        self.bt_cancel.clicked.connect( self.close     )
        self.bt_accept.clicked.connect( self.on_accept )       
        
        grid = QtGui.QGridLayout(self)
        grid.setColumnStretch(0, 2)
        
        if self.tag == 'armor':
            self.setWindowTitle("Wear Armor")
            grp     = QtGui.QGroupBox("Select Armor", self)
            vbox    = QtGui.QVBoxLayout(grp)
            self.cb = QtGui.QComboBox(self)
            self.cb.currentIndexChanged.connect( self.on_armor_select )
            vbox.addWidget(self.cb)           
            grid.addWidget(grp, 0, 0)
            
            grp     = QtGui.QGroupBox("Stats", self)
            vbox    = QtGui.QVBoxLayout(grp)
            self.stats = QtGui.QLabel(self)
            self.stats.setWordWrap(True)
            vbox.addWidget(self.stats)
                                
            grid.setRowStretch(1, 2)    
            grid.addWidget(grp, 1, 0, 1, 4)
            grid.addWidget(self.bt_accept, 2, 2)
            grid.addWidget(self.bt_cancel, 2, 3)
        elif self.tag == 'weapon':
            self.setWindowTitle("Add Weapon")
            grp     = QtGui.QGroupBox("Weapon Skill", self)
            vbox    = QtGui.QVBoxLayout(grp)
            self.cb1 = QtGui.QComboBox(self)
            self.cb1.currentIndexChanged.connect( self.on_weap_skill_select )
            vbox.addWidget(self.cb1)           
            grid.addWidget(grp, 0, 0)

            grp     = QtGui.QGroupBox("Weapon", self)
            vbox    = QtGui.QVBoxLayout(grp)
            self.cb2 = QtGui.QComboBox(self)
            self.cb2.currentIndexChanged.connect( self.on_weap_select )
            vbox.addWidget(self.cb2)           
            grid.addWidget(grp, 1, 0)
            
            grp     = QtGui.QGroupBox("Stats", self)
            vbox    = QtGui.QVBoxLayout(grp)
            self.stats = QtGui.QLabel(self)
            self.stats.setWordWrap(True)
            vbox.addWidget(self.stats)
            
            grid.setRowStretch(2, 2)
            grid.addWidget(grp, 2, 0, 1, 4)
            grid.addWidget(self.bt_accept, 3, 2)
            grid.addWidget(self.bt_cancel, 3, 3)            
        
    def load_data(self):
        c = self.dbconn.cursor()
        if self.tag == 'armor':
            c.execute('''select uuid, name from armors''')
            for uuid, name in c.fetchall():
                self.cb.addItem(name, uuid)
        elif self.tag == 'weapon':
            c.execute('''select skills.uuid, name, tag from skills
                         inner join tags on tags.uuid=skills.uuid
                         where tag="weapon"''')
            for uuid, name, tag in c.fetchall():
                self.cb1.addItem(name, uuid)
                
    def on_armor_select(self, text = ''):
        # list stats
        selected = self.cb.currentIndex()
        if selected < 0:
            return
        armor_uuid = self.cb.itemData(selected)
        self.item  = models.armor_outfit_from_db(self.dbconn, armor_uuid)
        
        stats_text = '''<p><pre>%-20s %s</pre></p>
                        <p><pre>%-20s %s</pre></p>
                        <p><pre>%-20s %s</pre></p>
                        <p><i>%s</i></p>''' % \
                        ( 'Armor TN ', self.item.tn,
                          'Reduction', self.item.rd,
                          'Cost     ', self.item.cost,
                          self.item.rule )
        self.stats.setText(stats_text)            
        
        self.stats.setSizePolicy( QtGui.QSizePolicy.Minimum,            
                                  QtGui.QSizePolicy.Minimum )
    
    def on_weap_skill_select(self, text = ''):
        self.cb2.clear()
        selected = self.cb1.currentIndex()
        if selected < 0:
            return
        sk_uuid = self.cb1.itemData(selected)
        
        c = self.dbconn.cursor()
        c.execute('''select uuid, name from weapons
                     where skill_uuid=?''', [sk_uuid])
                     
        for uuid, name in c.fetchall():
            self.cb2.addItem(name, uuid)
        
    def on_weap_select(self, text = ''):
        # list stats
        self.stats.setText('')
        
        selected = self.cb2.currentIndex()
        if selected < 0:
            return
        weap_uuid = self.cb2.itemData(selected)
        self.item = models.weapon_outfit_from_db(self.dbconn, weap_uuid)
        lines = []
                    
        if self.item.dr is not None:
            lines.append( '<pre>%-24s %s</pre>' % ('Primary DR  ',self.item.dr) )
        if self.item.dr_alt is not None:
            lines.append( '<pre>%-24s %s</pre>' % ('Secondary DR',self.item.dr_alt) )
        if self.item.range is not None:               
           lines.append( '<pre>%-24s %s</pre>' % ('Range        ',self.item.range) )
        if self.item.strength is not None:
           lines.append( '<pre>%-24s %s</pre>' % ('Strength     ',self.item.strength) )
        if self.item.min_str is not None:
           lines.append( '<pre>%-24s %s</pre>' % ('Min. Strength',self.item.min_str) )
        if self.item.cost is not None:
           lines.append( '<pre>%-24s %s</pre>' % ('Cost         ',self.item.cost) )
        if self.item.rule is not None:
           lines.append( '<i>%s</i>' % self.item.rule )
            
        self.stats.setText( '<p>' + '\n'.join(lines) + '</p>' )
            
        self.stats.setSizePolicy( QtGui.QSizePolicy.Minimum,            
                                  QtGui.QSizePolicy.Minimum )                       

  
    def on_accept(self):
        done = True

        if self.tag == 'armor' and self.item is not None:
            self.pc.armor = self.item
        elif self.tag == 'weapon' and self.item is not None:
            self.pc.add_weapon( self.item )

        self.accept()