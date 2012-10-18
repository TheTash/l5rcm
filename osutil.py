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

from subprocess import Popen
import os

from PySide import QtCore, QtGui

def detect_desktop_environment():
    desktop_environment = 'generic'
    if os.environ.get('KDE_FULL_SESSION') == 'true':
        desktop_environment = 'kde'
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        desktop_environment = 'gnome'
    else:
        pass
        #try:
        #    info = getoutput('xprop -root _DT_SAVE_MODE')
        #    if ' = "xfce4"' in info:
        #        desktop_environment = 'xfce'
        #except (OSError, RuntimeError):
        #    pass
    return desktop_environment

def portable_open(what):
    #print 'open ' + what
    if os.name == 'nt':
        #TODO ShellExec
        Popen(['explorer', what])
    elif os.name == 'posix':
        de = detect_desktop_environment()
        if de == 'gnome':
            Popen(['gnome-open', what])
        elif de == 'kde':
            Popen(['kde-open', what])
        elif de == 'xfce':
            Popen(['exo-open', what])
        else:
            Popen(['xdg-open', what])
            
def download_image(url, path, name):    
    import urllib2
    filename = name + url[-4:]
    filepath = os.path.join(path, filename)
    #print 'download image %s -> %s' % ( url, filepath )
    if os.path.exists(filepath):
        return filepath
        
    try:
        opener = urllib2.build_opener()
        page = opener.open(url)
        pic = page.read()
        fout = open(filepath, "wb")
        fout.write(pic)
        fout.close()        
    except:
        print 'image download failed %s' % (url)
        return None
        
    return filepath
    
def get_system_font():
    if os.name == 'posix':
        de = detect_desktop_environment()
        if de == 'gnome':
            try:
                import gconf
                client = gconf.client_get_default()
                font_name = client.get_string('/desktop/gnome/interface/font_name')
                t = font_name.rpartition()
                font_name = t[0]
                font_size = t[1]
                return QtGui.QFont(font_name, int(font_size))
            except:
                return QtGui.QApplication.font()            
    return QtGui.QApplication.font()
  
def get_user_data_path(rel_path = ''):
    user_data = '.'
    if os.name == 'posix':
        user_data = '%s/.config' % (os.environ['HOME'])
    elif os.name == 'nt':
        user_data = os.environ['APPDATA']
        
    user_data = os.path.join(user_data,\
        QtCore.QCoreApplication.organizationName(),\
        QtCore.QCoreApplication.applicationName())
        
    return os.path.join(user_data, rel_path)