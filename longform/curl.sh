#! /usr/bin/env bash

css="http://osp.constantvzw.org:9999/p/medor-css/export/txt"
html="http://osp.constantvzw.org:9999/p/medor-html/export/txt"

curl -o "static/css/styles.less" "${css}"
curl -o "index.html" "${html}"
