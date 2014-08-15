#! /usr/bin/bash
for i in $(seq 1 40);
do
 curl http://osp.constantvzw.org:9999/p/depliant-medor/export/txt > content.html
 curl http://osp.constantvzw.org:9999/p/depliant-medor-css/export/txt > typography.less

 sleep 15
done



