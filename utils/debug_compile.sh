#!/bin/bash

cd ~/Works/uygulamatik/client
cat externs/*.js > ./extern.js;  
java -jar /home/evren/bin/compiler.jar --js  ~/Works/uygulamatik/client/www/js/uygulamatik.js  --compilation_level ADVANCED_OPTIMIZATIONS \
--js_output_file ~/Works/uygulamatik/client/www/js/u.js --charset UTF-8 --third_party --formatting PRETTY_PRINT --externs \
~/Works/uygulamatik/client/extern.js --debug
