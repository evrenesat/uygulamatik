# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Photo.photo'
        db.alter_column(u'umatik_photo', 'photo', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100))

    def backwards(self, orm):

        # Changing field 'Photo.photo'
        db.alter_column(u'umatik_photo', 'photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'umatik.application': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Application'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'avail_langs': ('django.db.models.fields.CharField', [], {'default': "'tr,'", 'max_length': '255'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'background_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'header_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'header_type': ('django.db.models.fields.CharField', [], {'default': "'icon'", 'max_length': '10'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'tr'", 'max_length': '2'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'logo_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name_long': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_short': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Theme']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.AppType']"})
        },
        u'umatik.apptype': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'AppType'},
            'codename': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['umatik.Module']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.baseorder': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'BaseOrder'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ptime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'})
        },
        u'umatik.block': {
            'Meta': {'ordering': "['type']", 'object_name': 'Block'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'umatik.blocktranslation': {
            'Meta': {'ordering': "['lang']", 'object_name': 'BlockTranslation'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']", 'null': 'True', 'blank': 'True'}),
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Block']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'translation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'umatik.campaign': {
            'Meta': {'object_name': 'Campaign', 'db_table': "'campaigns'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'no_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Product']", 'null': 'True', 'blank': 'True'}),
            'special_background': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'thumb_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'umatik.customer': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.delegate': {
            'Meta': {'object_name': 'Delegate', 'db_table': "'delegate'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {})
        },
        u'umatik.elog': {
            'Meta': {'object_name': 'Elog'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.event': {
            'Meta': {'object_name': 'Event', 'db_table': "'event'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Node']", 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['umatik.Speaker']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.exhibitor': {
            'Meta': {'object_name': 'Exhibitor', 'db_table': "'exhibitor'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['umatik.Node']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'profile': ('django.db.models.fields.TextField', [], {})
        },
        u'umatik.exhibitorfiles': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'ExhibitorFiles'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']", 'blank': 'True'}),
            'exhibitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Exhibitor']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'umatik.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'called': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Customer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forhost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'umatik.icon': {
            'Meta': {'unique_together': "(('module', 'primary'),)", 'object_name': 'Icon'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hdimage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_icons'", 'null': 'True', 'to': u"orm['umatik.Module']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Theme']"})
        },
        u'umatik.map': {
            'Meta': {'object_name': 'Map'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        u'umatik.moduleselection': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('module', 'app'),)", 'object_name': 'ModuleSelection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'customicon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Icon']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Module']"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.news': {
            'Meta': {'ordering': "['sort', 'timestamp']", 'object_name': 'News'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'detail': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
        u'umatik.orderitem': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'OrderItem'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'baseorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.BaseOrder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Product']"}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'storeorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.StoreOrder']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.page': {
            'Meta': {'ordering': "['sort']", 'object_name': 'Page'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'detail': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.photo': {
            'Meta': {'ordering': "['sort', 'id']", 'object_name': 'Photo'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.place': {
            'Meta': {'object_name': 'Place', 'db_table': "'places'"},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'authorized_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'background': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '7', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
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
        u'umatik.profile': {
            'Meta': {'ordering': "['timestamp']", 'unique_together': "(('user', 'node'),)", 'object_name': 'Profile'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['umatik.Application']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Node']", 'null': 'True', 'blank': 'True'}),
            'super': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'umatik.speaker': {
            'Meta': {'object_name': 'Speaker', 'db_table': "'speaker'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'umatik.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.SponsorType']"})
        },
        u'umatik.sponsortype': {
            'Meta': {'ordering': "['sort']", 'object_name': 'SponsorType'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'umatik.storeorder': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'StoreOrder'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'baseorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.BaseOrder']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Customer']"}),
            'ept': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']"}),
            'ptime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'})
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
            'css': ('django.db.models.fields.TextField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'preview': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'umatik.version': {
            'Meta': {'object_name': 'Version', 'db_table': "'version'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'current_version': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '8', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['umatik']