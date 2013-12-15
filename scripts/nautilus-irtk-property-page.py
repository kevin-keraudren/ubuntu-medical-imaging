#!/usr/bin/python
"""
http://saravananthirumuruganathan.wordpress.com/2010/08/29/extending-nautilus-context-menus-using-nautilus-actions-scripts-and-python-extensions/
https://saravanant.googlecode.com/svn/trunk/blog/nautilusScripts/imdb-property-page.py

https://projects.gnome.org/nautilus-python/documentation/html/nautilus-python-overview-example.html

https://projects.gnome.org/nautilus-python/documentation/html/class-nautilus-python-property-page-provider.html

Writing Nautilus Python Extensions
----------------------------------

You can write Nautilus extensions in Python using the Nautilus-Python
extension. The scripts you write has to be placed in
$HOME/.nautilus/python-extensions. If you have admin rights, you can also place
them at /usr/lib/nautilus/extensions-2.0/python-extensions. Usually I prefer my
scripts to be in my home folder.

The development process is very similar Nautilus scripts. The steps are :

1. Create a python file in $HOME/.nautilus/python-extensions .
mkdir -p /home/$USER/.nautilus/python-extensions
mkdir -p ~/.local/share/nautilus-python/extensions/

2. Extend one or more of the interfaces and code the relevant functions in the interfaces. 

3. Make the script file as executable. 

4. Kill all instances of Nautilus using "nautilus -q" .

5. Restart Nautilus. During development, using "nautilus --no-desktop" as it
starts without reading profile preferences.

6. Test your extension. This will be extension specific due to the various
capabilities of the nautilus python extensions.

Debug:
nautilus -q
cp nautilus-irtk-property-page.py ~/.local/share/nautilus-python/extensions/
nautilus --no-desktop /home/kevin/Imperial/PhD/fetal_brain/all_reconstructions/2493

"""

import sys
# add the irtk module to PYTHONPATH
# (when run in the background, nautilus will not benefit from .bashrc)
sys.path.insert(0,"/home/kevin/Imperial/PhD/irtk.untouched/build/lib")

import irtk
import re
import os
import urllib

from gi.repository import Nautilus, GObject, Gtk

IRTK_MIMES = ['.nii']

class IRTKPropertyPageExtension(GObject.GObject,Nautilus.PropertyPageProvider):
    def __init__(self):
        return

    def getAttrFromArray(self,elemArray,nameOfAttr):
        result = ",".join( [el[nameOfAttr] for el in elemArray])
        return result

    def getIRTKDtls( self, fileName ):
        header, dtype = irtk._irtk.get_header( fileName )
        img = irtk.imread( fileName, dtype='float32' )
        
        irtkDtls = []
        irtkDtls.append( ("Image Size",
                          str(header['dim'][0]) + "\t" +
                          str(header['dim'][1]) + "\t" +
                          str(header['dim'][2]) + "\t" +
                          str(header['dim'][3]) + "\t" ) )
        irtkDtls.append( ("Voxel Size (mm)",
                          format(header['pixelSize'][0],'.3f') + "\t" +
                          format(header['pixelSize'][1],'.3f') + "\t" +
                          format(header['pixelSize'][2],'.3f') + "\t" +
                          format(header['pixelSize'][3],'.3f') + "\t" ) )
        irtkDtls.append( ("Origin",
                          format(header['origin'][0],'.3f') + "\t" +
                          format(header['origin'][1],'.3f') + "\t" +
                          format(header['origin'][2],'.3f') + "\t" +
                          format(header['origin'][3],'.3f') + "\t" ) )
        irtkDtls.append( ( "X Axis",
                           format(header['orientation'][0,0],'.3f') + "\t" +
                           format(header['orientation'][0,1],'.3f') + "\t" +
                           format(header['orientation'][0,2],'.3f') ) )
        irtkDtls.append( ( "Y Axis",
                           format(header['orientation'][1,0],'.3f') + "\t" +
                           format(header['orientation'][1,1],'.3f') + "\t" +
                           format(header['orientation'][1,2],'.3f') ) )
        irtkDtls.append( ("Z Axis",
                          format(header['orientation'][2,0],'.3f') + "\t" +
                          format(header['orientation'][2,1],'.3f') + "\t" +
                          format(header['orientation'][2,2],'.3f') ) )

        irtkDtls.append( ( "Ordering", img.order() ) )
        orientation = img.orientation()
        irtkDtls.append( ( "Orientation",
                           orientation[0] + "\t" +
                           orientation[1] + "\t" +
                           orientation[2] ) )
        irtkDtls.append( ( "Data Type", dtype ) )

        
        irtkDtls.append( ( "Min-Max",
                           format(float(img.min()),'.3f') + "\t" +
                           format(float(img.max()),'.3f') ) )
        irtkDtls.append( ( "Image to World",
                           format(img.I2W[0,0],'.3f') + "\t" +
                           format(img.I2W[0,1],'.3f') + "\t" +
                           format(img.I2W[0,2],'.3f') + "\t" +
                           format(img.I2W[0,3],'.3f') + "\n" +
                           format(img.I2W[1,0],'.3f') + "\t" +
                           format(img.I2W[1,1],'.3f') + "\t" +
                           format(img.I2W[1,2],'.3f') + "\t" +
                           format(img.I2W[1,3],'.3f') + "\n" +
                           format(img.I2W[2,0],'.3f') + "\t" +
                           format(img.I2W[2,1],'.3f') + "\t" +
                           format(img.I2W[2,2],'.3f') + "\t" +
                           format(img.I2W[2,3],'.3f') + "\n" +
                           format(img.I2W[3,0],'.3f') + "\t" +
                           format(img.I2W[3,1],'.3f') + "\t" +
                           format(img.I2W[3,2],'.3f') + "\t" +
                           format(img.I2W[3,3],'.3f') ) )
        irtkDtls.append( ( "World to Image",
                           format(img.W2I[0,0],'.3f') + "\t" +
                           format(img.W2I[0,1],'.3f') + "\t" +
                           format(img.W2I[0,2],'.3f') + "\t" +
                           format(img.W2I[0,3],'.3f') + "\n" +
                           format(img.W2I[1,0],'.3f') + "\t" +
                           format(img.W2I[1,1],'.3f') + "\t" +
                           format(img.W2I[1,2],'.3f') + "\t" +
                           format(img.W2I[1,3],'.3f') + "\n" +
                           format(img.W2I[2,0],'.3f') + "\t" +
                           format(img.W2I[2,1],'.3f') + "\t" +
                           format(img.W2I[2,2],'.3f') + "\t" +
                           format(img.W2I[2,3],'.3f') + "\n" +
                           format(img.W2I[3,0],'.3f') + "\t" +
                           format(img.W2I[3,1],'.3f') + "\t" +
                           format(img.W2I[3,2],'.3f') + "\t" +
                           format(img.W2I[3,3],'.3f') ) )
        return irtkDtls

    def getHBoxForAttr(self,attrName, text):
        hbox = Gtk.HBox(homogeneous=False, spacing=0)
        hbox.show()

        label = Gtk.Label()
        label.set_markup( " <b>" + attrName + ":</b>  " )
        label.show()
        hbox.pack_start(label, False, False, 0)

        value_label = Gtk.Label()
        value_label.set_text( text )
        value_label.show()
        hbox.pack_start(value_label, False, False, 0)
        return hbox
    
    def get_property_pages(self,files):
        if len(files) != 1:
            return
        
        fileObj = files[0]
        if fileObj.get_uri_scheme() != 'file':
            return

        if fileObj.is_directory():
            return

        fileName = urllib.unquote(fileObj.get_uri()[7:])
        
        #Stripping extension
        root, extension = os.path.splitext(fileName)
        if extension == ".gz":
            root, extension = os.path.splitext(root)
        if extension not in IRTK_MIMES:
            return
        
        irtkDtls = self.getIRTKDtls(fileName)

        self.property_label = Gtk.Label('IRTK info')
        self.property_label.show()

        self.hbox = Gtk.HBox(homogeneous=False, spacing=0)
        self.hbox.show()

        self.vbox = Gtk.VBox(homogeneous=False, spacing=0)
        self.vbox.show()

        for attribute, text in irtkDtls:
            self.vbox.pack_start(self.getHBoxForAttr(attribute, text),
                                 expand=False, fill=False, padding=4 )

        self.hbox.pack_start(self.vbox, False, False, 0)
        
        return Nautilus.PropertyPage( name="NautilusPython::irtk_dtls",
                                      label=self.property_label,
                                      page=self.hbox ),
