# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'App'
        db.create_table(u'weixin_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64, null=True, blank=True)),
            ('app_url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('app_token', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('app_key', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'weixin', ['App'])

        # Adding model 'Rule'
        db.create_table(u'weixin_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('response', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'weixin', ['Rule'])

        # Adding model 'SubscribeItem'
        db.create_table(u'weixin_subscribe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.App'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.Rule'])),
        ))
        db.send_create_signal(u'weixin', ['SubscribeItem'])

        # Adding model 'MenuItem'
        db.create_table(u'weixin_menu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('secondary', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.App'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.Rule'], null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'weixin', ['MenuItem'])

        # Adding model 'Photo'
        db.create_table(u'weixin_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64, null=True, db_index=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'weixin', ['Photo'])

        # Adding model 'RichText'
        db.create_table(u'weixin_richtext', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weixin.Photo'])),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('html', self.gf('applications.ueditor.fields.UEditorField')(default=u'', null=True, blank=True)),
        ))
        db.send_create_signal(u'weixin', ['RichText'])

        # Adding M2M table for field rules on 'RichText'
        m2m_table_name = db.shorten_name(u'weixin_richtext_rules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('richtext', models.ForeignKey(orm[u'weixin.richtext'], null=False)),
            ('rule', models.ForeignKey(orm[u'weixin.rule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['richtext_id', 'rule_id'])


    def backwards(self, orm):
        # Deleting model 'App'
        db.delete_table(u'weixin_app')

        # Deleting model 'Rule'
        db.delete_table(u'weixin_rule')

        # Deleting model 'SubscribeItem'
        db.delete_table(u'weixin_subscribe')

        # Deleting model 'MenuItem'
        db.delete_table(u'weixin_menu')

        # Deleting model 'Photo'
        db.delete_table(u'weixin_photo')

        # Deleting model 'RichText'
        db.delete_table(u'weixin_richtext')

        # Removing M2M table for field rules on 'RichText'
        db.delete_table(db.shorten_name(u'weixin_richtext_rules'))


    models = {
        u'weixin.app': {
            'Meta': {'object_name': 'App'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'app_key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'app_token': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'app_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'weixin.menuitem': {
            'Meta': {'object_name': 'MenuItem', 'db_table': "u'weixin_menu'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'main': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.Rule']", 'null': 'True', 'blank': 'True'}),
            'secondary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'weixin.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'md5': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'weixin.richtext': {
            'Meta': {'ordering': "[u'-priority']", 'object_name': 'RichText'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'html': ('applications.ueditor.fields.UEditorField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.Photo']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['weixin.Rule']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'weixin.rule': {
            'Meta': {'object_name': 'Rule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'weixin.subscribeitem': {
            'Meta': {'object_name': 'SubscribeItem', 'db_table': "u'weixin_subscribe'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weixin.Rule']"})
        }
    }

    complete_apps = ['weixin']