# -*-  coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *
#from fabric.contrib.console import confirm


'''
henüz yapmadıysan: pip install fabric

fab prepare => git commit -a -m '~' && git push

fab prepare:m="mesaj kaygisi" => git commit -a -m 'mesaj kaygisi' && git push

fab prepare:-A => git add -A && git commit -a && git push

fab prepare:-A, mesaj_metni => git add -A && git commit -a -m 'mesaj_metni' && git push

kısacası prepare: den sonra ne yazarsan "git add" komutuna ekleniyor, hiçbirşey yazmazsan git add komutu çalıştırılmıyor.


kullanacağımız diğer komut "fab deploy"

fab deploy

ya da eğer db göçü yapılacaksa:

fab deploy:1


'''

env.hosts = ['cnvar@elipsis.com.tr']

#site_list = ['weblonya',]
deploy_dir = '/home/cnvar/forum-server'


def prepare(add_this='-A', m='~'):
#    local("./manage.py test my_app")

    if add_this:
        local("git add %s" % add_this)
    local("git commit -a -m '%s'" % m)
    local("git push")


def full(goc=''):
    if goc == '2':
        localmigrate()
    prepare()
    deploy(goc)


def pull():
    prepare()
    justpull()


def localmigrate(what='umatik'):
    local("./manage.py schemamigration --auto %s" % what)
    local("./manage.py migrate --all")


def wsync():
    local("rsync -rzh   --progress --exclude-from=exclude.list client/www/* "
          "cnvar@s1.elipsis.com.tr:/home/cnvar/forum-server/client/www/")


def deploy(migrate=False):
    local("git push")
    with cd(deploy_dir):
        run("git fetch --all")
        run("git reset --hard origin/master")
        if migrate:
            remote_migrate()
        restart_sites()


def justpull():
    with cd(deploy_dir):
        run("git fetch --all")
        run("git reset --hard origin/master")


def restart_sites():
    run("supervisorctl restart forum-server")


def remote_migrate():
    with cd(deploy_dir):
        run("./manage.py migrate --all")



