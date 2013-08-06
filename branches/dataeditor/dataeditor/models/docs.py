# -*- coding: utf-8 -*-
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

from PySide import QtCore

DOC_STATUS_CLEAN = 0
DOC_STATUS_DIRTY = 1

class DocumentItem(QtCore.QObject):

    doc_status_change = QtCore.Signal(int)

    obj    = None
    path   = None
    status = DOC_STATUS_CLEAN

    def __init__(self, path, obj, parent = None):
        super(DocumentItem, self).__init__(parent)

        self.path = path
        self.obj  = obj

    def set_dirty(self, flag):
        st = DOC_STATUS_DIRTY if flag else DOC_STATUS_CLEAN
        if st != self.status:
            self.status = st
            self.doc_status_change.emit(st)

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def __hash(self):
        return hash(self.path)

class OpenedDocuments(QtCore.QObject):

    doc_added         = QtCore.Signal(object     )
    doc_removed       = QtCore.Signal(object     )
    doc_status_change = QtCore.Signal(object, int)

    items = []

    def __init__(self, parent = None):
        super(OpenedDocuments, self).__init__(parent)

    def add_document(self, doc_path, doc_obj):
        di = DocumentItem(doc_path, doc_obj, self)
        if di not in self.items:
            self.items.append(di)
            di.doc_status_change.connect( self.on_document_status_change )
            self.doc_added.emit(di)
            return di
        return None

    def rem_document(self, doc_item):
        if doc_item in self.items:
            self.items.remove(doc_item)
            self.doc_removed.emit(doc_item)
            return True
        return False

    def on_document_status_change(self, st):
        self.doc_status_change.emit(self.sender(), st)