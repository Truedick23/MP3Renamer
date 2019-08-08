import os
import mutagen
from tinytag import TinyTag
from mutagen import flac


def songTitleFormat(oriTitle):
    if oriTitle[-1] == ')':
        i = oriTitle.find('(')
        _set = ['Remastered', 'Version', 'Remaster']
        if(oriTitle.find(_str) >= i for _str in _set):
            return oriTitle[0:i-1]
    return oriTitle


def acquireInfo(src):
    mu = mutagen.File(src)
    trackNum = str(mu.get("TRCK").text[0])  # 得到音轨号
    performer = str(mu.get("TPE1").text[0])  # 得到表演者
    songName = str(songTitleFormat(mu.get("TIT2").text[0]))  # 得到歌曲名称
    albumName = str(mu.get("TALB").text[0])
    if int(trackNum) < 10:
        trackNum = '0' + trackNum
    return trackNum, performer, songName, albumName


def acquireFlacInfo(src):
    mu = flac.FLAC(src)
    trackNum = mu.get("TRCK").text[0]  # 得到音轨号
    performer = mu.get("TPE1").text[0]  # 得到表演者
    songName = songTitleFormat(mu.get("TIT2").text[0])  # 得到歌曲名称
    albumName = mu.get("TALB").text[0]
    if int(trackNum) < 10:
        trackNum = '0' + trackNum
    # print(trackNum, performer, songName, albumName)
    return trackNum, performer, songName, albumName


def main():
    '''
    dir = "E:/CloudMusic/Television/Marquee Moon"  # 需要处理的歌曲目录，请根据实际情况替换
    os.chdir(dir)
    songsList = os.listdir(dir)
    for song in songsList:
        srcFile = dir + "/" + song
        trackNum, performer, songName, _ = acquireInfo(srcFile)
        newName = trackNum + ' - ' + songName + ' - ' + performer + '.mp3'
        print(newName)
        os.rename(song, newName)
    '''
    src = "E:/CloudMusic/The Allman Brothers Band\The Allman Brothers Band/01 - Don't Want You No More - The Allman Brothers Band.mp3"
    acquireInfo(src)
# main()