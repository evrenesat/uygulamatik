# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Module'
        db.create_table(u'umatik_module', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Module'])

        # Adding model 'ModuleSelection'
        db.create_table(u'umatik_moduleselection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Module'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Icon'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('customicon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['ModuleSelection'])

        # Adding model 'AppType'
        db.create_table(u'umatik_apptype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('codename', self.gf('django.db.models.fields.SlugField')(max_length=30)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['AppType'])

        # Adding M2M table for field modules on 'AppType'
        db.create_table(u'umatik_apptype_modules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('apptype', models.ForeignKey(orm[u'umatik.apptype'], null=False)),
            ('module', models.ForeignKey(orm[u'umatik.module'], null=False))
        ))
        db.create_unique(u'umatik_apptype_modules', ['apptype_id', 'module_id'])

        # Adding model 'Theme'
        db.create_table(u'umatik_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('css', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('preview', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Theme'])

        # Adding model 'Icon'
        db.create_table(u'umatik_icon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Theme'])),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='related_icons', null=True, to=orm['umatik.Module'])),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('hdimage', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'umatik', ['Icon'])

        # Adding model 'Application'
        db.create_table(u'umatik_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.AppType'])),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Theme'])),
            ('name_short', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('name_long', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('logo_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('logo_big', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('header_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('header_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('background_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('background_color', self.gf('django.db.models.fields.CharField')(max_length=14, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(default='tr', max_length=2)),
            ('avail_langs', self.gf('django.db.models.fields.CharField')(default='tr,', max_length=255)),
            ('lat', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('lon', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Application'])

        # Adding model 'Block'
        db.create_table(u'umatik_block', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'], null=True, blank=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'umatik', ['Block'])

        # Adding model 'BlockTranslation'
        db.create_table(u'umatik_blocktranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'], null=True, blank=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Block'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('translation', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'umatik', ['BlockTranslation'])

        # Adding model 'ProductCategory'
        db.create_table('product_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.ProductCategory'], null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['ProductCategory'])

        # Adding model 'StoreProductCategory'
        db.create_table('store_product_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'], null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['StoreProductCategory'])

        # Adding model 'Place'
        db.create_table('places', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.ProductCategory'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='place_details', max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('authorized_person', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=10, null=True, blank=True)),
            ('gsm', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('llogo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('background', self.gf('django.db.models.fields.CharField')(default='#ffffff', max_length=7, blank=True)),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['umatik.Node'], unique=True, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Place'])

        # Adding model 'Node'
        db.create_table(u'umatik_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'umatik', ['Node'])

        # Adding model 'Map'
        db.create_table(u'umatik_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('map', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Map'])

        # Adding model 'Matrix'
        db.create_table(u'umatik_matrix', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('node1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='frm', to=orm['umatik.Node'])),
            ('node2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to', to=orm['umatik.Node'])),
            ('distance', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'umatik', ['Matrix'])

        # Adding model 'Profile'
        db.create_table(u'umatik_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'], null=True, blank=True)),
            ('super', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Profile'])

        # Adding unique constraint on 'Profile', fields ['user', 'place']
        db.create_unique(u'umatik_profile', ['user_id', 'place_id'])

        # Adding model 'Product'
        db.create_table('products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.ProductCategory'], null=True, blank=True)),
            ('store_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.StoreProductCategory'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cut_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('discount_rate', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('showcase', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'umatik', ['Product'])

        # Adding model 'Campaign'
        db.create_table('campaigns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.ProductCategory'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Product'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('momentary_campaign', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_text', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumb_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('special_background', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Campaign'])

        # Adding model 'Page'
        db.create_table('pages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Page'])

        # Adding model 'Version'
        db.create_table('version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('current_version', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=8, decimal_places=2)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Version'])

        # Adding model 'Customer'
        db.create_table(u'umatik_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Customer'])

        # Adding model 'Feedback'
        db.create_table(u'umatik_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Customer'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('msg', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('forhost', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('called', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Feedback'])

        # Adding model 'BaseOrder'
        db.create_table(u'umatik_baseorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Customer'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ptime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['BaseOrder'])

        # Adding model 'StoreOrder'
        db.create_table(u'umatik_storeorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('ept', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Customer'])),
            ('baseorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.BaseOrder'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ptime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['StoreOrder'])

        # Adding model 'OrderItem'
        db.create_table(u'umatik_orderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('storeorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.StoreOrder'], null=True, blank=True)),
            ('baseorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.BaseOrder'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Place'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('qty', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('line_total', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['OrderItem'])

        # Adding model 'Elog'
        db.create_table(u'umatik_elog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umatik', ['Elog'])

        # Adding model 'Speaker'
        db.create_table('speaker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Speaker'])

        # Adding model 'Delegate'
        db.create_table('delegate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Delegate'])

        # Adding model 'Exhibitor'
        db.create_table('exhibitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['umatik.Node'], unique=True, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('profile', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=10, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Exhibitor'])

        # Adding model 'Event'
        db.create_table('event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['umatik.Application'])),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['umatik.Node'], unique=True, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'umatik', ['Event'])

        # Adding M2M table for field speakers on 'Event'
        db.create_table('event_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'umatik.event'], null=False)),
            ('speaker', models.ForeignKey(orm[u'umatik.speaker'], null=False))
        ))
        db.create_unique('event_speakers', ['event_id', 'speaker_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Profile', fields ['user', 'place']
        db.delete_unique(u'umatik_profile', ['user_id', 'place_id'])

        # Deleting model 'Module'
        db.delete_table(u'umatik_module')

        # Deleting model 'ModuleSelection'
        db.delete_table(u'umatik_moduleselection')

        # Deleting model 'AppType'
        db.delete_table(u'umatik_apptype')

        # Removing M2M table for field modules on 'AppType'
        db.delete_table('umatik_apptype_modules')

        # Deleting model 'Theme'
        db.delete_table(u'umatik_theme')

        # Deleting model 'Icon'
        db.delete_table(u'umatik_icon')

        # Deleting model 'Application'
        db.delete_table(u'umatik_application')

        # Deleting model 'Block'
        db.delete_table(u'umatik_block')

        # Deleting model 'BlockTranslation'
        db.delete_table(u'umatik_blocktranslation')

        # Deleting model 'ProductCategory'
        db.delete_table('product_category')

        # Deleting model 'StoreProductCategory'
        db.delete_table('store_product_category')

        # Deleting model 'Place'
        db.delete_table('places')

        # Deleting model 'Node'
        db.delete_table(u'umatik_node')

        # Deleting model 'Map'
        db.delete_table(u'umatik_map')

        # Deleting model 'Matrix'
        db.delete_table(u'umatik_matrix')

        # Deleting model 'Profile'
        db.delete_table(u'umatik_profile')

        # Deleting model 'Product'
        db.delete_table('products')

        # Deleting model 'Campaign'
        db.delete_table('campaigns')

        # Deleting model 'Page'
        db.delete_table('pages')

        # Deleting model 'Version'
        db.delete_table('version')

        # Deleting model 'Customer'
        db.delete_table(u'umatik_customer')

        # Deleting model 'Feedback'
        db.delete_table(u'umatik_feedback')

        # Deleting model 'BaseOrder'
        db.delete_table(u'umatik_baseorder')

        # Deleting model 'StoreOrder'
        db.delete_table(u'umatik_storeorder')

        # Deleting model 'OrderItem'
        db.delete_table(u'umatik_orderitem')

        # Deleting model 'Elog'
        db.delete_table(u'umatik_elog')

        # Deleting model 'Speaker'
        db.delete_table('speaker')

        # Deleting model 'Delegate'
        db.delete_table('delegate')

        # Deleting model 'Exhibitor'
        db.delete_table('exhibitor')

        # Deleting model 'Event'
        db.delete_table('event')

        # Removing M2M table for field speakers on 'Event'
        db.delete_table('event_speakers')


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
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'header_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'header_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'tr'", 'max_length': '2'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'logo_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name_long': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
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
            'momentary_campaign': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['umatik.Node']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['umatik.Speaker']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'umatik.exhibitor': {
            'Meta': {'object_name': 'Exhibitor', 'db_table': "'exhibitor'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['umatik.Node']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'profile': ('django.db.models.fields.TextField', [], {})
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
            'Meta': {'object_name': 'Icon'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hdimage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_icons'", 'null': 'True', 'to': u"orm['umatik.Module']"}),
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
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'umatik.moduleselection': {
            'Meta': {'ordering': "['order']", 'object_name': 'ModuleSelection'},
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
        u'umatik.node': {
            'Meta': {'object_name': 'Node'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'object_name': 'Page', 'db_table': "'pages'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
            'Meta': {'ordering': "['timestamp']", 'unique_together': "(('user', 'place'),)", 'object_name': 'Profile'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['umatik.Place']", 'null': 'True', 'blank': 'True'}),
            'super': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'umatik.speaker': {
            'Meta': {'object_name': 'Speaker', 'db_table': "'speaker'"},
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
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'css': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
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