#QPlayer
==========

Music player with ffmpeg\SDL2.0\PyQt\Python C-API surpport

####Lib Dependence:

- SDL2.0
- ffmpeg
    - make and install the latest ffmpeg:
        - (maby need: sudo apt-get install yasm)
        - ./configure --enable-shared
        - make
        - sudo make install
        - if can't find lib*.so:

            sudo vi /etc/ld.so.conf
            add follow lines:
                include ld.so.conf.d/*.conf
                /usr/local/libevent-1.4.14b/lib
                /usr/local/lib

            then:
                sudo ldconfig


###Uasage:

- goto core/player_core/, run`python setup.py build`.
- copy core/player_core/build/lib.linux-x86_64-2.7/CPlayer.so to core/
- python QPlayer.py


###Old versions:

- 1.2 [releases](https://github.com/MarcoQin/QPlayer/releases)
    - need mplayer surpport


##展示

![Qmp3player][test]

[test]: https://github.com/MarcoQin/gallery/blob/master/Qmp3player/Qplayer.png

