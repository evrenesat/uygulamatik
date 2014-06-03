#!/usr/bin/python
#-*- coding:utf-8 -*-

import argparse
import codecs, glob, os, re, shelve
from pprint import pprint
import shutil

import subprocess as sp
from random import random
from shutil import move
from os.path import join
from time import sleep, time
#import logging
import sys
import traceback

#log = logging.getLogger('scss')

try:
    import pynotify
except:
    from xnotify import pynotify


#import scss

#Custom tags for precomplation of html templates
TAGS = {'head-left': [], 'head-right': [], 'head-extras': [], 'page-extras': [], 'footer': [],
        'title': ['<h1>&nbsp;</h1>']}

PROJ_DIR = join(os.path.dirname(os.path.abspath(__file__)), '../')
BASE_DIR = join(os.path.dirname(os.path.abspath(__file__)), '../client/')
WWW_DIR = join(BASE_DIR, 'www')

CLOSURE_COMPILER_PATH = "/home/evren/bin/compiler.jar"
COMPILE_CMD = 'java -jar %s  --js uygulamatik.js  --compilation_level ADVANCED_OPTIMIZATIONS ' \
              '--js_output_file u.js --charset UTF-8 --third_party --externs externs.js' % (
    CLOSURE_COMPILER_PATH, )
COMPRESS_LIB_CMD = 'java -jar %s  --js lib.js  --compilation_level WHITESPACE_ONLY ' \
                   '--js_output_file lib_out.js --charset UTF-8 --third_party' % (
                       CLOSURE_COMPILER_PATH, )
# COMPRESS_LIB_CMD = 'java -jar %s  --js lib.js  --compilation_level WHITESPACE_ONLY ' \
EXTERNS_CMD = "cat %s/*.js >%s/externs.js   " % (join(BASE_DIR, 'externs'), join(WWW_DIR, 'js'))

PACKAGES_DIR = join(BASE_DIR, 'apppackages')
REMOTE_WWW_DIR = "/home/cnvar/forum-server/client/www/"



#RESOLUTIONS = [] #editor execfiledan anlamiyor.
#execfile("%scoffee/resolutions.coffee" % BASE_DIR)

#TODO: bu liste sadece once yuklenmesi gereken ana kutuphaneleri icersin, gerisini dizinden kendi bulsun.
VENDOR_JS = [
    'cordova-2.2.0.js',
    'jquery-1.8.1.min.js',
    #             'jquery.mobile.transition-handler-simple.js',
    #             'jquery.mobile.simultaneous-transitions-replace-simple.js',
    'persistence/persistence.js',
    'persistence/persistence.store.sql.js',
    'persistence/persistence.store.websql.js',
    'persistence/persistence.store.memory.js',
    'settings.js',
    'bios.js',
    #burdan sonrasi otomatik yuklenebilir
    'json-serialization.js',
    'ratchet.js',
    # 'jquery.mobile.min.js',
    'less-1.3.0.min.js',
    'jed.js',
    'klass.min.js',
    #    'photoswipe.jquery-3.0.5.min.js',
    #    'code.photoswipe.jquery-3.0.5.js',
    'share.js',
    'softkeyboard.js',
    'barcodescanner.js',
    'mobiscroll-2.0.1.full.min.js',
    'iscroll.js',
    'jquery.jsPlumb-1.3.3-all.js',
    'dijkstra.js',
    'doT.js'
]
if sys.platform == 'darwin':
    ADB = '/Users/elipsis/Downloads/android-sdk-macosx/platform-tools/adb push %s %s'
else:
    ADB = 'adb push %s %s'
SCP = 'scp -r %s root@droid:%s'


class Builder:
    """
    i'm da project builder!

    compiles coffeescript, scss and html templates
    compiles and syncs only modified files/dirs

    joins vendor_js libraries
    syncs with an adb or scp target
    pyScss used for scss

    with "prod" argument:
        comment outs console.log statements
        yuicompressor used for js minifaction
        "fab pull" command called for syncing with git and web server

    with "sync_all" argument:
        syncs whole www folder (primarly used for "images" folder)

    """

    def __init__(self):
        self.title = "Uygulamatik Builder"
        pynotify.init(self.title)
        self.res = {}
        self.args = {}
        self.re_clear_header = re.compile(r"<div data-role='header.*?</div>")
        self.db = shelve.open("%s/build_times" % BASE_DIR)
        self.sync_list = [join(WWW_DIR, 'index.html')]
        self.daemon = False
        for t in TAGS:
            self.res[t] = re.compile(r"<%s>(.*?)</%s>" % (t, t))
        self.include_re = re.compile(r"{% *?include (\w*?) *?%}")

        self.current_process = None
        self.at_least_one_built = None
        self.sync_target = ADB
        self.base_sync_path = '/sdcard/www/'
        self.current = None
        self.build_failured_at = ''
        self.reload_index = False
        self.build_for_production = False
        self.template_cache = {}
        self.messages = []
        self.buildtime = time()
        self.test_mode = False
        self.keep_logs = False
        self.notify = None
        self.build_functions = {
            #paths should be relative to base_dir
            #metod_name: ['source file or dir name', 'target dir path  ', 'will reload index.html', 'optional local dir path' ]
            'fix_index': ['index.html', 'index.html', False, ''],
            #            'compile_scss': ['scss/layout.scss', 'css/', True, ''],
            'sync_layout': ['www/css/layout.less', 'css/', True, ''],
            'compile_coffee': ['coffee', 'js/uygulamatik.js', True, ''],
            'compile_templates': ['templates', 'tmpl.html', False, ''],
            'join_vendor_js': ['js_vendors', 'js/lib.js', False, ''],
        }


    def parse_path(self, process):
        source, target, reload_index, local_path = self.build_functions[process]
        #            print "www_dir", BASE_DIR
        self.current = {
            'source': join(BASE_DIR, source),
            'source_path': join(BASE_DIR, local_path or source if os.path.isdir(join(BASE_DIR, source)) else ''),
            'www_path': join(WWW_DIR, target),
            'sync_path': join(self.base_sync_path, target),
            'reload_index': reload_index,
        }

    #        print self.current

    def build_package(self):
        shutil.copytree(WWW_DIR, PACKAGES_DIR + '/' + self.args.appid)

    def build(self):
        """
        once en son guncellenenden baslayarak derleme metodlarini calistirir
        """
        try:
            build_functions = self.build_functions.keys()
            if self.db.get('last_rebuild_target'):
                self._run_process(self.db['last_rebuild_target'])
                build_functions.remove(self.db['last_rebuild_target'])

            for f in build_functions:
                if not self._run_process(f):
                    print "broke at %s" % self.current_process
                    break
            if self.reload_index:
                self._run_process('fix_index', True)
        except Exception, e:
            print traceback.format_exc()
            raise
        finally:
            if not self.at_least_one_built:
                if not self.args.daemon:
                    self._show_message("Nothing to compile!", 5)
                if self.notify:
                    self.notify.set_timeout(pynotify.EXPIRES_DEFAULT)
            elif self.args.daemon:
                print "%s done" % self.at_least_one_built


    def _run_process(self, process, force=False):
        """
        ortam degiskenlerini ayarlar, ilgili dizine girer, gerekli metodu calistirir
        @param process: str, Builder method
        @param force: Boolean, forces to run process, overrides self._is_rebuild_required()
        @return: Boolean
        """
        self.parse_path(process)
        force = force or self.args.runonce
        self.current_process = process
        if self._is_rebuild_required() or force or self.build_for_production:
            os.chdir(self.current['source_path'])
            success = getattr(self, process)()
            if success:
                self._mark_rebuild(True)
                self.reload_index = self.current['reload_index']
            else:
                self.build_failured_at = self.current_process
                return False
        return True


    def sync(self, sync_list=None):
        """
        @type sync_list: path list
        """
        #        print 'sync'
        if not self.sync_target:
            return
        if not sync_list:
            sync_list = [self.current['www_path']]
        elif not isinstance(sync_list, list):
            sync_list = [sync_list]
        for f in sync_list:
            cmd = self.sync_target % (f, self.current['sync_path'])
            print "sync cmd: %s" % cmd
            isok, out = self._sh(cmd)
            #            print cmd, out[:50]Builder
        #        if self.current_process != 'fix_index':
        self._show_message("%s SYNC  OK" % self.current_process)


    def sync_www(self):
        sync_cmd = self.sync_target % (WWW_DIR, self.base_sync_path)
        print "full sync cmd: %s" % sync_cmd
        result = self._sh(sync_cmd)[1].replace('\\n', "\n")
        pprint(result)

    def _sh(self, cmd):
        k = sp.Popen(cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, close_fds=True)
        error = k.stderr.read()
        output = k.stdout.read().strip()
        if error:
            output = error + output
        k.wait()
        return not error, (output or 'OK')


    def _get_build_date(self, path=None):
        if not path:
            path = self.current['source']
        mdates = 0.0
        files = glob.glob(path)
        for node in files:
            path_ = path if path[:-1] != '/' else path[:1]
            if os.path.isdir(path_):
                mdates += self._get_build_date(join(node, '*'))
            else:
                mdates += os.path.getmtime(node)
        return mdates

    def _show_message(self, msg, timeout=10, clean=False, show=False):
        try:
            msg = msg.replace("_", " ")
            #        print msg
            if clean:
                self.messages = []
            self.messages.append(msg)
            msgs = " :: ".join(self.messages)
            error = msgs.find('error') > -1 or msgs.find('Err') > -1
            print msg
            if not self.notify:
                self.notify = pynotify.Notification(self.title, msgs)
                self.notify.set_timeout(1000 * timeout)
            else:
                self.notify.update(self.title, msgs)
            if not self.args.daemon or error or show:
                self.notify.show()
            if error:
                sleep(5)
        except:
            print msg
            pass

    def _hide_message(self):
        self.messages = []
        self.notify.close()

    #        self.notify.set_hint("x", -100)
    #        self.notify.set_hint("y", -700)
    #        self._sh("kdialog --title 'Da Builder' --passivepopup '%s' %s" % (msg, timeout))
    #        self._sh("notify-send -t %s 'Da Builder' '%s' " % (timeout * 1000, msg))


    def _is_rebuild_required(self):
        self.current['last_build'] = self._get_build_date()
        if self.args.runonce:
            return True
        req = self.db.get(self.current_process) != self._get_build_date()
        return req


    def _mark_rebuild(self, needed):
        if needed:
            self.db[self.current_process] = self.current['last_build']
            #print  "after mark", self.current_process, self.current['last_build'], self.db[self.current_process]
            self.db['last_rebuild_target'] = self.current_process
            self.at_least_one_built = self.current_process

    def sync_layout(self):
        """less kodunda yazim hatasi olunca tarayici icinde calisan less compiler hicbir hata vermiyor.
        bu yuzden layout.less dosyasini lessc ile yazim hatalarina karsi denetliyoruz.
        """

        lessc_compiler_installed, output = self._sh("which lessc")
        if lessc_compiler_installed:
            self._sh("echo '@semitransbg:rgba(0,0,0,0.6); @verytransbg:rgba(0,0,0,0.3); @doc_height :800; @doc_width:480;' > /tmp/t.less; "
                     "cat %s >> /tmp/t.less;" % self.current['source'])
            less_file_ok, output = self._sh("lessc /tmp/t.less > /dev/null")
            if not less_file_ok:
                self._show_message("LESS ERROR %s" % output, 10, 1, 1)
                return False
        else:
            less_file_ok = True
            print "lessc not installed, layout.less not checked for syntax errors"
        if less_file_ok:
            self.sync()
        return True


    def _render_tags(self, template):
        self.template = template
        self.template = self.template.replace("\n", "").replace('IMG_PTH',
                                                                '/sdcard/forumbornova')#.replace(' href=', ' data-href=')

        if 'headless' in self.template:
            self.template = self.re_clear_header.sub("", self.template).replace('[[headless]]', '')

        for t, extra in TAGS.items():
            contents = self.res[t].findall(self.template)
            if contents:
                self.template = self.res[t].sub('', self.template)
                self.template = self.template.replace("[[%s]]" % t, contents[0])
            else:
                self.template = self.template.replace("[[%s]]" % t, "")
                if extra:
                    self.template = self.template.replace(extra[0], "")
        return self.template + "\n\n"


    def fix_index(self):
        """
        gelistirme surecinde istemdisi onbellekleme sorunlarindan kurtulmak icin
        index.html'deki pathlere rasgele parametre ilavesi
        """
        index_icerik = codecs.open(self.current['source'], 'r', 'utf-8').read()
        index_yaz = codecs.open(self.current['www_path'], 'w', 'utf-8')
        index_icerik = index_icerik.replace("[[surum]]", unicode(random()))
        if not self.args.native:
            script = '<script src="http://appserver.uygulamatik.com/getappid/"></script>'
        else:
            script = ''
        index_icerik = index_icerik.replace("[[WEB_SCRIPT]]", script)
        index_yaz.write(index_icerik.replace("[[surum]]", unicode(random())))
        index_yaz.close()
        self.sync()
        return True

    def do_settings(self):
        isok, stout = self._sh("cat settings.tpl.js > settings.js")
        tsettings_file = open('settings.tpl.js', 'r')
        base_settings = tsettings_file.read()
        tsettings_file.close()
        settings_file = open('settings.js', 'w')
        settings_file.write(base_settings)
        settings_file.write('settings.STORAGE_DIRNAME="uygulamatik";')
        if self.args.appid:
            settings_file.write('settings.APPID= "%s";' % self.args.appid)
        if self.args.serverurl:
            settings_file.write('settings.SERVER_URL= "http://%s/";' % self.args.serverurl)
            settings_file.write('settings.STATIC_SERVER_URL= "http://%s/";' % self.args.serverurl)
        settings_file.write('settings.BUILDTIME= "%s";' % self.buildtime)

        self.current['last_build'] = self._get_build_date()

    def join_vendor_js(self):
        self.do_settings()
        isok, stout = self._sh("cat %s > %s" % (' '.join(VENDOR_JS), self.current['www_path']))
        os.chdir(join(WWW_DIR, 'js'))
        #BYPASS LIB COMPRESS
        # compile_result = self._sh(COMPRESS_LIB_CMD)
        # if compile_result[0]:
        #     os.remove('lib.js')
        #     move('lib_out.js', 'lib.js')
        #     result = 'SUCCESS'
        # else:
        #     result = compile_result[1][:100]
        #     print compile_result
        # self._show_message("compress lib.js %s" % result, 10, 1, 1)

        self._mark_rebuild(isok)
        self.sync()
        #        print "join v", isok
        if not isok:
            print stout
        return isok


    def _remove_console_logs(self):
    #        clean = "\n".join([l for l in open('uygulamatik.coffee','r')  if not l.strip().startswith("console.log")])
        uc = open('uygulamatik.coffee', 'r')
        clean = uc.read().replace("console.log", "#console.log")
        uc.close()
        with open('uygulamatik.coffee', 'w') as cf:
            cf.write(clean)


    # def make_ucoffee(self):
    #     with codecs.open('_base/template.html', 'r', 'utf-8') as tmpf:
    #         base_template = tmpf.read()
    #     tmpl = codecs.open(self.current['www_path'], 'w', 'utf-8')
    #
    def compile_coffee(self):
        try:
            os.remove("uygulamatik.coffee")
        except:
            pass
        self._sh("cat *.coffee > uygulamatik.coffee")
        if (self.build_for_production and not self.args.keeplogs) or self.args.clearlogs:
            self._remove_console_logs()
        bare = '' if self.build_for_production or self.args.nobare else ' -b '
        isok, stout = self._sh("coffee -c %s uygulamatik.coffee" % bare)
        #        isok, stout = self._sh("coffee --js -i uygulamatik.coffee -o uygulamatik.js")
        #        print isok,stout
        if 'err' not in stout:
            move("uygulamatik.js", self.current['www_path'])
            os.remove("uygulamatik.coffee")
            if self.args.ccompile:
                self.compile_js()

            self.sync()
            return True
        else:
            for l in stout.split("\n"):
                print l
                if l.find('Error') > -1:
                    self._show_message(l, 10)
            return False

    def rsync(self):
        cmd = "rsync -hrz  --progress  %s/* cnvar@elipsis.com.tr:%s" % (WWW_DIR, REMOTE_WWW_DIR)
        print cmd
        rso = self._sh(cmd)[1].split("\n")
        return rso[-2][:15] + " / " + rso[-1][-6:]

    #        return "\n".join(rso[-1:])

    def commit(self):
        os.chdir(PROJ_DIR)
        self._sh("fab deploy")[1]

    def product(self):
        self.build_for_production = True
        self.build()
        if not self.build_failured_at:
            self.compress_lib_js()
            self.compile_js()
        #            rsync_output = self.rsync()
        #            self._show_message("RSYNC:: %s" % rsync_output, clean=1)


    def compress_lib_js(self):
        self._show_message("Compress lib js", clean=1)
        os.chdir(join(WWW_DIR, 'js'))
        # print self._sh("yuicompressor -o '.js$:.js' *.js")
        print self._sh("yuicompressor -o lib.js lib.js")

    def compile_js(self):
        self._show_message("compile & compress js", clean=1)
        os.chdir(join(WWW_DIR, 'js'))

        CMD = COMPILE_CMD  + '  --formatting PRETTY_PRINT --debug' if self.args.ccdebug else COMPILE_CMD

        # print self._sh("yuicompressor -o '.js$:.js' *.js")
        print self._sh(EXTERNS_CMD)
        compile_result =  self._sh(CMD)
        #bu uyari coffescript'i -b (bare) parametresiyle calistirdigimiz icin cikiyor. productionda sorun yok
        devel_only_warning = "dangerous use of the global this object" in compile_result[1]
        if compile_result[0] or devel_only_warning:
            os.remove('uygulamatik.js')
            move('u.js', 'uygulamatik.js')
            result = 'SUCCESS'
        else:
            result = compile_result[1][:100]
        self._show_message("Closure compile %s" % result, 10, 1, 1)


    def compile_templates(self):
        """

        templates dizinindeki sablonlari on islemdden gecirip tek dosyaya derler.
        _base dizini altinda temel sablonlar bulunur.
        apptype  parametresiyle verilen dizindeki sablonlarin _base'e onceligi vardir.
        _ altcizgi ile baslayan sablonlar parcacik olarak kullanilir.


        """
        with codecs.open('_base/template.html', 'r', 'utf-8') as tmpf:
            base_template = tmpf.read()
        tmpl = codecs.open(self.current['www_path'], 'w', 'utf-8')
        self.template_dict = {}
        #once uygulama tipine ozel templateleri okuyoruz
        for file in glob.glob('%s/*.html' % self.args.apptype):
            filename = os.path.splitext(os.path.basename(file))[0]
            with codecs.open(file, 'r', 'utf-8') as tmpf:
                self.template_dict[filename] = tmpf.read()
            #                print ">>", filename
            #base template dizinini okuyoruz. ayni isimde bi template yukarida tanimlandiysa pas geciyoruz
        #apptype templateleri _base dekileri override ediyor
        for f in glob.glob('_base/*.html'):
            filename = os.path.splitext(os.path.basename(f))[0]
            if filename == 'template':
                continue
            if filename not in self.template_dict:
            #                print ">>>>>>", filename
                with codecs.open(f, 'r', 'utf-8') as tmpf:
                    self.template_dict[filename] = tmpf.read()
                #            else:
                #                print "pass >>>", filename
        for template_name, template_content in self.template_dict.items():
            tmpl.write('[[--]]%s+|+' % template_name)
            if template_name[0] != '_':
                template_content = base_template.replace('[[page_id]]', template_name).replace('[[page_container]]',
                                                                                               template_content)
            try:
                template_content = self.include_re.sub(self.get_template, template_content)
                template_content = self._render_tags(template_content)
            except:
                print template_name, "islenirken beklenmeyen hata"
                raise
            tmpl.write(template_content)
        tmpl.close()
        self._mark_rebuild(True)
        self.sync()
        return True


    def get_template(self, teplate_match):
        tn = teplate_match.group(1)
        return self.template_dict.get(tn, self.load_template(tn))


    def load_template(self, teplate_name):
        self.template_dict[teplate_name] = self.include_re.sub(self.get_template, self.template_dict[teplate_name])
        return self.template_dict[teplate_name]


if __name__ == "__main__":
    b = Builder()
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--runonce", action="store_true",
                        help="Bir kerelik calisir. Dosyalarda degisiklik olmasa bile calisir")

    parser.add_argument("-d", "--daemon", action="store_true",
                        help="İzleyici sunucu modu, dosyalarda degisiklik olunca otomatikman yeniden derlenir.")

    parser.add_argument("-s", "--sync", action="store_true",
                        help="Tum dosyalari uzak sunucuyla ve -varsa- test cihaziyla senkronize et")

    parser.add_argument("-p", "--product", action="store_true",
                        help="Üretim modu, dosyalari compile eder, keeplogs yoksa loglari kapatir.")

    parser.add_argument("-n", "--native", action="store_true",
                        help="Web surumune ozel islevleri kapatir, native ozel islevleri acar.")

    parser.add_argument("-k", "--keeplogs", action="store_true",
                        help="Üretim modunda bile loglarin acik kalmasini saglar.")
    #
    #    parser.add_argument("-t", "--test", action="store_true",
    #        help="Test modu. Sunucu adresi olarak http://127.0.0.1:8000 kullanilir.")
    #
    parser.add_argument("-b", "--nobare", action="store_true",
                        help="Gelistirici modunda coffeescripti 'bare' bayragi olmadan calistirir")

    parser.add_argument("-cd", "--ccdebug", action="store_true",
                        help="Closure Compiler'i pretty_print ve debug parametreleriyle calistirir.")

    parser.add_argument("-cc", "--ccompile", action="store_true",
                        help="Uygulamayi Closure Compiler ile derler. Bu secenek product (-p) modunda zaten  aciktir.")

    parser.add_argument("-cl", "--clearlogs", action="store_true",
                        help="console.log'larını temizler.")

    parser.add_argument("-u", "--serverurl", default='',
                        help="Test modunda kullanılacak uygulama sunucu adresi.")

    parser.add_argument("-at", "--apptype", default='expo',
                        help="Uygulama tipi. expo, avm, kafe degerlerinden biri girilmelidir.Varsayilan expo dur.")

    parser.add_argument("-id", "--appid", default='',
                        help="Uygulama IDsi.")

    b.args = parser.parse_args()

    #    b._run_process('compile_scss',1)
    #    b.sync_target = None
    #    argv.append('prod')
    if b.args.runonce:
        b.build()
        if b.args.appid:
            b.build_package()

    elif b.args.daemon:
        try:
            while 1:
                b.buildtime = time()
                b.build()
                if b.at_least_one_built:
                    b.at_least_one_built = False
                    t = time() - b.buildtime
                    print "build started at %s took %s ms" % (b.buildtime, t)
                b.messages = []
                sleep(1)
        except Exception, e:
            print traceback.format_exc()
        finally:
            b.db.close()

    elif b.args.sync:
        b.sync_www()

    elif b.args.product:
        b.product()
    b.db.close()
    b._show_message("Process Complete", show=True)
    if b.notify:
        b.notify.set_timeout(6000)
#    print "sleeping..."
#    sleep(4)
