# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrderTable.app'
        db.add_column(u'at_shop_order_ordertable', 'app',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=4, to=orm['umatik.Application']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrderTable.app'
        db.delete_column(u'at_shop_order_ordertable', 'app_id')


    models = {
        u'at_shop_order.localorderitem': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'LocalOrderItem'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'order_head': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['at_shop_order.OrderHead']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Product']"}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'at_shop_order.orderhead': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'OrderHead'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_table': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['at_shop_order.OrderTable']"}),
            'ptime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'})
        },
        u'at_shop_order.ordertable': {
            'Meta': {'ordering': "['name']", 'object_name': 'OrderTable'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'explanation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'umatik.application': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Application'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'background_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'css': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'default_language': ('django.db.models.fields.CharField', [], {'default': "'tr'", 'max_length': '2'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'header_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'header_type': ('django.db.models.fields.CharField', [], {'default': "'icon'", 'max_length': '10'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jmt': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '2'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'logo_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name_long': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_short': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'splash_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ApplicationStatus']", 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Theme']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.AppType']"})
        },
        u'umatik.applicationstatus': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'ApplicationStatus'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('ckeditor.fields.RichTextField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'umatik.apptype': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'AppType'},
            'codename': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'iconb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['umatik.Module']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.iconcategory': {
            'Meta': {'ordering': "['sort']", 'object_name': 'IconCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        u'umatik.map': {
            'Meta': {'object_name': 'Map'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'offset': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'umatik.matrix': {
            'Meta': {'object_name': 'Matrix'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'distance': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frm'", 'to': u"orm['umatik.Node']"}),
            'node2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to'", 'to': u"orm['umatik.Node']"})
        },
        u'umatik.module': {
            'Meta': {'ordering': "['order']", 'object_name': 'Module'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'umatik.node': {
            'Meta': {'object_name': 'Node'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Map']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nbhds': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['umatik.Node']", 'through': u"orm['umatik.Matrix']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'umatik.place': {
            'Meta': {'object_name': 'Place', 'db_table': "'places'"},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'authorized_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'background': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '7', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('ckeditor.fields.RichTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'gsm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'llogo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['umatik.Node']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'place_details'", 'max_length': '100'})
        },
        u'umatik.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'products'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'cut_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'discount_rate': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'showcase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'store_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.StoreProductCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'umatik.productcategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProductCategory', 'db_table': "'product_category'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'umatik.storeproductcategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'StoreProductCategory', 'db_table': "'store_product_category'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '100'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']", 'null': 'True', 'blank': 'True'})
        },
        u'umatik.theme': {
            'Meta': {'ordering': "['order']", 'object_name': 'Theme'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'iconset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.IconCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jmt': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'processed_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'web_processed_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['at_shop_order']