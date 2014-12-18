# -*- coding: utf-8 -*-
# Python 2.7

'''
ID3v1.0 reader.
API:        import Mediainfo
For help:   Mediainfo.py -h
Main features:
  *parseAllSongs    read all songs'id3 tag from files
  *getFileInfo      get one song's info by index
'''

__author__ = "MarcoQin <qyyfy2009@gmail.com>"
__version__ = "None"

import os
import sys


def stripFunc(data):
    return data.replace("\00", "").strip()

def stripFunc2(data):
    return data

class MediaInfo(object):
    def __init__(self):
        self.allsongsinfo = []
        self.metadict = {}
        self.tagDataMap = {"title": (3, 33, stripFunc),
                  "artist": (33, 63, stripFunc),
                  "album": (63, 93, stripFunc),
                  "year": (93, 97, stripFunc),
                  "comment": (97, 126, stripFunc),
                  "genre": (127, 128, ord)}
        self.genres = [
                       'Blues', 'Classic Rock', 'Country', 'Dance', 'Disco', 'Funk', 'Grunge', 'Hip - Hop', 'Jazz', 'Metal',
                       'New Age', 'Oldies', 'Other', 'Pop', 'R&B', 'Rap', 'Reggae', 'Rock', 'Techno', 'Industrial',
                       'Alternative', 'Ska', 'Death Metal', 'Pranks', 'Soundtrack', 'Euro - Techno', 'Ambient', 'Trip - Hop', 'Vocal', 'Jazz + Funk',
                       'Fusion', 'Trance', 'Classical', 'Instrumental', 'Acid', 'House', 'Game', 'Sound Clip', 'Gospel', 'Noise',
                       'Alt Rock', 'Bass', 'Soul', 'Punk', 'Space', 'Meditative', 'Instrumental Pop', 'Instrumental Rock', 'Ethnic', 'Gothic',
                       'Darkwave', 'Techno - Industrial', 'Electronic', 'Pop - Folk', 'Eurodance', 'Dream', 'Southern Rock', 'Comedy', 'Cult', 'Gangsta Rap',
                       'Top 40', 'Christian Rap', 'Pop / Funk', 'Jungle', 'Native American', 'Cabaret', 'New Wave', 'Psychedelic', 'Rave', 'Showtunes',
                       'Trailer', 'Lo - Fi', 'Tribal', 'Acid Punk', 'Acid Jazz', 'Polka', 'Retro', 'Musical', 'Rock & Roll', 'Hard Rock',
                       'Folk', 'Folk / Rock', 'National Folk', 'Swing', 'Fast - Fusion', 'Bebob', 'Latin', 'Revival', 'Celtic', 'Bluegrass',
                       'Avantgarde', 'Gothic Rock', 'Progressive Rock', 'Psychedelic Rock', 'Symphonic Rock', 'Slow Rock', 'Big Band', 'Chorus', 'Easy Listening', 'Acoustic',
                       'Humour', 'Speech', 'Chanson', 'Opera', 'Chamber Music', 'Sonata', 'Symphony', 'Booty Bass', 'Primus', 'Porn Groove',
                       'Satire', 'Slow Jam', 'Club', 'Tango', 'Samba', 'Folklore', 'Ballad', 'Power Ballad', 'Rhythmic Soul', 'Freestyle',
                       'Duet', 'Punk Rock', 'Drum Solo', 'A Cappella', 'Euro - House', 'Dance Hall', 'Goa', 'Drum & Bass', 'Club - House', 'Hardcore',
                       'Terror', 'Indie', 'BritPop', 'Negerpunk', 'Polsk Punk', 'Beat', 'Christian Gangsta Rap', 'Heavy Metal', 'Black Metal', 'Crossover',
                       'Contemporary Christian', 'Christian Rock', 'Merengue', 'Salsa', 'Thrash Metal', 'Anime', 'JPop', 'Synthpop'
                       ]


    def parse(self, filename):
        self.metadict = {}
        try:
            songmeta = open(filename, 'rb', 0)
            try:
                songmeta.seek(-128, 2)
                tagdata = songmeta.read(128)
                #print tagdata
            finally:
                songmeta.close()
            if tagdata[:3] == 'TAG':
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    self.metadict[tag] = parseFunc(tagdata[start:end])
                    #print self.metadict
        except:
            pass
        self.allsongsinfo.append(self.metadict)

    def parseAllSongs(self, files):
        self.allsongsinfo = []
        for file in files:
            file = unicode(file)
            self.parse(file)

    def getFileInfo(self,index):
        DECODE = sys.getfilesystemencoding()
        filemetadata = self.allsongsinfo[index]
        if filemetadata:
            title = filemetadata.get('title', 'N/A').decode(DECODE)
            artist = filemetadata.get('artist', 'N/A').decode(DECODE)
            album = filemetadata.get('album', 'N/A').decode(DECODE)
            genre = filemetadata.get('genre', '7')
            if genre < 147:
                genre = self.genres[genre].decode(DECODE)
            else:
                genre = 'Other'
            return 'Title:' + title + '\n' + 'Artist:' + artist + '\n' + 'Album:' + album + '\n' + 'Genre:' + genre
        else:
            return None


if __name__ == "__main__":
    print "RUN ERROR!!"
    raw_input('press enter to exit->')