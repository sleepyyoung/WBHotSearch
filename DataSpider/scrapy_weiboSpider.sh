#! /bin/sh
export PATH=$PATH:/usr/local/bin

echo $PATH
cd /home/sleepyyoung/wblsrs/DataSpider
/usr/bin/scrapy crawl weiboSpider >> weiboSpider.log 2>&1 &

