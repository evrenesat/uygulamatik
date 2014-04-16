#!/bin/sh

cd webimages
wget -nc -i http://appserver.uygulamatik.com/pack_image_list/?dt=`date +%s`
rm index*
