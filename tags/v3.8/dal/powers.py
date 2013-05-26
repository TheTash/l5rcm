#!/usr/bin/python
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

from requirements import Requirement, RequirementOption
from xmlutils import read_attribute, read_attribute_int, read_sub_element_text, read_tag_list
class Kiho(object):

    @staticmethod
    def build_from_xml(elem):
        f = Kiho()
        f.id      = elem.attrib['id']
        f.name    = read_attribute(elem, 'name')        
        f.element = read_attribute(elem, 'element')
        f.type    = read_attribute(elem, 'type')
        f.mastery = read_attribute_int(elem, 'mastery')
        f.desc    = read_sub_element_text(elem, 'Description', "")
        
        f.tags  = read_tag_list(elem)
                
        return f        
        
    def __str__(self):
        return self.name or self.id
        
    def __unicode__(self):
        return self.name

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)
        
    def __hash__(self):
        return obj.id.__hash__()

class Kata(object):

    @staticmethod
    def build_from_xml(elem):
        f = Kata()
        f.id      = elem.attrib['id']
        f.name    = read_attribute(elem, 'name')                
        f.element = read_attribute(elem, 'element')
        f.mastery = read_attribute_int(elem, 'mastery')
        f.desc    = read_sub_element_text(elem, 'Description', "")
        # requirements
        f.require = []
       
        for se in elem.find('Requirements'):
            if se.tag == 'Requirement':
                f.require.append(Requirement.build_from_xml(se))        
            if se.tag == 'RequirementOption':
                f.require.append(RequirementOption.build_from_xml(se))
                
        f.tags  = read_tag_list(elem)             
                
        return f        
        
    def __str__(self):
        return self.name or self.id
        
    def __unicode__(self):
        return self.name

    def __eq__(self, obj):
        return obj and obj.id == self.id

    def __ne__(self, obj):
        return not self.__eq__(obj)
        
    def __hash__(self):
        return obj.id.__hash__()
