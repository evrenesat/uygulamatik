# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OrderTable.qrcode'
        db.alter_column(u'at_shop_order_ordertable', 'qrcode_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['qurl.QRcode'], unique=True, null=True))
        # Adding unique constraint on 'OrderTable', fields ['qrcode']
        db.create_unique(u'at_shop_order_ordertable', ['qrcode_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'OrderTable', fields ['qrcode']
        db.delete_unique(u'at_shop_order_ordertable', ['qrcode_id'])


        # Changing field 'OrderTable.qrcode'
        db.alter_column(u'at_shop_order_ordertable', 'qrcode_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qurl.QRcode'], null=True))

    models = {
        u'at_shop_order.localorderitem': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'LocalOrderItem'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'order_head': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['at_shop_order.OrderHead']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.MenuItem']"}),
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
            'Meta': {'ordering': "['sort', 'name']", 'object_name': 'OrderTable'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'explanation': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'qrcode': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['qurl.QRcode']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        u'at_shop_order.ordertabletranslation': {
            'Meta': {'unique_together': "(('lang', 'source'),)", 'object_name': 'OrderTableTranslation'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'explanation': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.AppLang']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['at_shop_order.OrderTable']"})
        },
        u'qurl.qrcode': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'QRcode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'umatik.applang': {
            'Meta': {'unique_together': "(('app', 'code'),)", 'object_name': 'AppLang'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pul': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.application': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Application'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'app_bg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'logo_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name_long': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_short': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_qrcode_button': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'splash_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ApplicationStatus']", 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.SlugField', [], {'max_length': '25', 'blank': 'True'}),
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
        u'umatik.menucategory': {
            'Meta': {'ordering': "['sort']", 'object_name': 'MenuCategory'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        u'umatik.menuitem': {
            'Meta': {'ordering': "['category', 'sort']", 'object_name': 'MenuItem'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.MenuCategory']"}),
            'cut_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'prepare_time': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'showcase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
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
        u'umatik.theme': {
            'Meta': {'ordering': "['order']", 'object_name': 'Theme'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'iconset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.IconCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'processed_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transparent_background': ('django.db.models.fields.CharField', [], {'default': "'rgba(0,0,0, 0.60)'", 'max_length': '25'}),
            'transparent_background2': ('django.db.models.fields.CharField', [], {'default': "'rgba(0,0,0, 0.30)'", 'max_length': '25'}),
            'web_processed_css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['at_shop_order']