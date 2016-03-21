#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup, Extension

module1 = Extension('CPlayer',
                    libraries=[
                        'avutil',
                        'avformat',
                        'avcodec',
                        'swscale',
                        'swresample',
                        'z',
                        'SDL2'
                    ],
                    sources=['player_py.c', 'player.c'])

setup(name='CPlayer',
      version='1.0',
      description='This is sound parse package',
      author='Marco Qin',
      author_email='qyyfy2009@gmail.com',
      url='https://marcoqin.github.io',
      long_description=''' This is SoundUtils ''',
      ext_modules=[module1]
)
