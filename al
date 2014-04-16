#!/bin/sh


rsync -rz  --progress --exclude-from=exclude.list  cnvar@s1.elipsis.com.tr:/home/cnvar/forum-server/media/uploads/* media/uploads/
