# -- coding: utf-8 --
#************#
# Importación Clientes y Proveedores #
#************#

import os
import csv
import xmlrpclib
import re
from urlparse import urlparse
import base64
import urllib2
import requests


HOST='127.0.0.1'
PORT=8069
DB='mh'
USER='admin'
PASS='admin'
path_file = 'productos.csv'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

# archive = csv.DictReader(open(path_file))

def get_image(url):
    if not url:
        return False
    try:
        image = base64.b64encode(requests.get(url).content)
    except Exception as exc:
        image = False
    return image

def _create(estado):
    if estado is True:
        archive = csv.DictReader(open(path_file))
        cont = 1

        for field in archive:
            vals = {}
            vals['barcode'] = field['barcode']
            vals['name'] = field['name']
            vals['default_code'] = field['default_code']
            vals['list_price'] = field['lst_price']
            full_path = field['image_medium']

            vals['image_medium'] = get_image(full_path)

            product_id = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)
            if product_id:
                print str(cont) + "--" + str(field['barcode']) + "--> Insertado"
            cont += 1


def main():
    print 'Ha comenzado el proceso'
    _create(True)
    print 'Ha finalizado la carga tabla'
main()





