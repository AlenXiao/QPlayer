#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import sys
sys.path.append("..")

import requests
from utils.xml_to_dict import xml_to_dict


class Bilibili(object):

    def __init__(self):
        self.comment_uri = 'http://comment.bilibili.cn/{cid}.xml'
        self.appkey = '0a99fa1d87fdd38c'
        self.video_uri = 'http://interface.bilibili.tv/playurl?cid={cid}&appkey={appkey}'
        self.base_uri = 'http://www.bilibili.com/video/av{av_id}/'

    def get_cid(self, av_id):
        html = self.get(self.base_uri.format(av_id=av_id))
        result = html[html.find('cid'): html.find('aid')].strip()
        return result.split('=')[-1].replace('&', '')

    def get_video_addr(self, cid):
        result = self.get(self.video_uri.format(cid=cid, appkey=self.appkey))
        result = xml_to_dict(result)
        print result
        if result['result'] == 'suee':
            return result['durl']['url']

    def get(self, uri):
        return requests.get(uri).text


if __name__ == '__main__':
    b = Bilibili()
    cid = b.get_cid(2977110)
    print b.get_video_addr(cid)
