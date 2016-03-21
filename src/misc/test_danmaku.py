#!/usr/bin/env python
# encoding: utf-8

from xml.etree import ElementTree


def int_to_rgb(num):
    return tuple((num >> Val) & 255 for Val in (0, 8, 16))


def xml_to_dict(xml_string):
    d = []
    element = ElementTree.XML(xml_string)
    for et in element:
        attr = et.attrib
        if 'p' in attr:
            p = attr['p'].split(',')
            base = {
                'time': float(p[0]),
                'text': et.text,
                'size': int(p[2]),
                'color': 'rgb({0}, {1}, {2})'.format(*int_to_rgb(int(p[3]))),
                'mode': ['', 'R2L', 'R2L', 'R2L', 'BOTTOM', 'TOP'][int(p[1])]
            }
            d.append(base)
    d.sort(key=lambda x: x['time'])
    return d


def get_danmaku():
    with open('4824299.xml') as f:
        result = xml_to_dict(f.read())
        return result
