# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import BasicSongsOperator as bso
import sys
import os


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def rename_song(song_path, format):
    (dir, song_name) = os.path.split(song_path)
    newName = ''
    try:
        trackNum, performer, songName, albumName = bso.acquireInfo(song_path)
        '''
            tn: Track - Title
            tnp: Track - Title - Performer
            tpn: Track - Performer - Title
            tnpa: Track - Title - Performer - Album
            tpan: Track - Performer - Album - Title
            tpna: Track - Performer - Title - Album
        '''
        if format == 'tn':
            newName = trackNum + ' - ' + songName + '.mp3'
        elif format == 'tnp':
            newName = trackNum + ' - ' + songName + ' - ' + performer + '.mp3'
        elif format == 'tpn':
            newName = trackNum + ' - ' + performer + ' - ' + songName + '.mp3'
        elif format == 'tnpa':
            newName = trackNum + ' - ' + songName + ' - ' + performer +  ' - ' + albumName + '.mp3'
        elif format == 'tpan':
            newName = trackNum + ' - ' + performer +  ' - ' + albumName + ' - ' + songName + '.mp3'
        elif format == 'tpna':
            newName = trackNum + ' - ' + performer + ' - ' + songName + ' - ' + albumName + '.mp3'

        if newName != songName and newName != '':
            os.chdir(dir)
            os.rename(song_name, newName)
        return (1, newName)
    except:
        print(newName)
        return (2, newName)

def rename_performer(performer_path, format):
    succeed = 0
    failed = 0
    new_names_dict = {}
    for album in os.listdir(performer_path):
        new_album_songs = []
        album_name = album
        album = performer_path + '/' + album
        for song in os.listdir(album):
            song_path = album + '/' + song
            if os.path.splitext(song_path)[1] == '.mp3':
                (result, new_name) = rename_song(song_path, format)
                if result == 1:
                    succeed = succeed + 1
                    new_album_songs.append(new_name)
                else:
                    failed = failed + 1
        new_names_dict[album_name] = new_album_songs

    return (succeed, failed, new_names_dict)

class MultiFileDialog(QFileDialog):
    def __init__(self, *args):
        QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.DirectoryOnly)
        for view in self.findChildren((QListView, QTreeView)):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(QAbstractItemView.MultiSelection)


class Renamer(QWidget):

    def __init__(self):
        super().__init__()
        self.format = 'tnp'
        self.formNum = -3
        self.formatDict = {
            '-2': 'tn',
            '-3': 'tnp',
            '-4': 'tpn',
            '-5': 'tnpa',
            '-6': 'tpan',
            '-7': 'tpna'
        }
        self.chooseFileBtnSheet = 'QPushButton{background-color:#EEE8CD; color:#8B4C39; font-size:16px; height: 50px; width: 70px;}' \
                                  'QPushButton:hover{background-color:#8B7355; color:#FFE7BA; font-size:16px; height: 50px; width: 70px;}' \
                                  'QPushButton:pressed{font-weight:bold;background-color:#FFEC8B; color: #8B814C; font-size:16px; height: 50px; width: 70px;}'

        self.setWindowIcon(QIcon('headphone.png'))
        self.setWindowTitle('Just a simple mp3 renamer.')
        self.initUI()

    def initUI(self):
        self.wholeLayout = QVBoxLayout()
        self.btnLayout = QHBoxLayout()

        self.LbtnLayout = QVBoxLayout()
        self.LbtnLayout.setContentsMargins(5, 10, 10, 5)

        self.chooseSongBtn = QPushButton("Choose songs")
        self.chooseSongBtn.setStyleSheet(self.chooseFileBtnSheet)
        self.chooseSongBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.chooseSongBtn.clicked.connect(self.getSongFiles)
        self.LbtnLayout.addWidget(self.chooseSongBtn)

        self.choosePerformerBtn = QPushButton("Choose performers")
        self.choosePerformerBtn.setStyleSheet(self.chooseFileBtnSheet)
        self.choosePerformerBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.choosePerformerBtn.clicked.connect(self.getPerformerDirs)
        self.LbtnLayout.addWidget(self.choosePerformerBtn)

        self.formatSelectLayout = QHBoxLayout()

        self.formBtnGroup = QButtonGroup()
        self.RbtnLayout = QVBoxLayout()

        self.tpBtn = QRadioButton(text="Track - Title")
        self.formBtnGroup.addButton(self.tpBtn)
        self.RbtnLayout.addWidget(self.tpBtn)

        self.tnpBtn = QRadioButton(text="Track - Title - Performer")
        self.tnpBtn.setChecked(True)
        self.formBtnGroup.addButton(self.tnpBtn)
        self.RbtnLayout.addWidget(self.tnpBtn)

        self.tpnBtn = QRadioButton(text="Track - Performer - Title")
        self.formBtnGroup.addButton(self.tpnBtn)
        self.RbtnLayout.addWidget(self.tpnBtn)

        self.tnpaBtn = QRadioButton(text="Track - Title - Performer - Album")
        self.formBtnGroup.addButton(self.tnpaBtn)
        self.RbtnLayout.addWidget(self.tnpaBtn)

        self.tpanBtn = QRadioButton(text="Track - Performer - Album - Title")
        self.formBtnGroup.addButton(self.tpanBtn)
        self.RbtnLayout.addWidget(self.tpanBtn)

        self.tpnaBtn = QRadioButton(text="Track - Performer - Title - Album")
        self.formBtnGroup.addButton(self.tpnaBtn)
        self.RbtnLayout.addWidget(self.tpnaBtn)

        self.RbtnLayout.setContentsMargins(15, 3, 3, 5)
        self.formBtnGroup.buttonClicked.connect(self.formatBtnClicked)

        self.output = QTextEdit()
        self.output.setStyleSheet('{background: #F5F5DC')
        self.output.setTextColor(QColor('#8B4513'))
        self.output.setText('Thanks for using mp3 simple renamer. '
                            '\nPlease choose your desired rename format from the right and then select your files or directories from the left.'
                            '\nMake sure that the directories are pointed to some performers, which contains album directories that contains mp3 files.'
                            '\nHave fun using it!')

        self.btnLayout.addLayout(self.LbtnLayout)
        self.btnLayout.addLayout(self.RbtnLayout)
        self.btnLayout.setStretch(0, 40)
        self.btnLayout.setStretch(1, 54)

        self.wholeLayout.addLayout(self.btnLayout)
        self.wholeLayout.addWidget(self.output)
        self.wholeLayout.setSpacing(10)

        self.setLayout(self.wholeLayout)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor('#E8E8E8'))
        self.setPalette(self.palette)
        self.resize(640, 400)
        self.show()

    def formatBtnClicked(self):
        checkedId = self.formBtnGroup.checkedId()
        self.formNum = checkedId
        self.format = self.formatDict[str(self.formNum)]

    def getSongFiles(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, r'Please choose songs or performers to rename',
                                                     r'E:\CloudMusic', 'Music Files (*.mp3)')

        total_num = len(file_names)
        succeed = 0
        failed = 0
        new_names = []
        for file in file_names:
            (result, new_name) = rename_song(file, self.format)
            if result == 1:
                succeed = succeed + 1
                new_names.append(new_name)
            else:
                failed = failed + 1

        songs_str = '\n'.join([new_name for new_name in new_names])
        self.output.setText(songs_str + '\n\n' + str(total_num) + " songs in total, " + str(succeed) + " succeeded, " + str(failed) + " failed.")


    def getPerformerDirs(self):

        dlg = MultiFileDialog()
        dlg.setDirectory('E:\CloudMusic')
        dlg.show()
        dlg.exec_()

        dir_names = dlg.selectedFiles()
        performer_names = [os.path.split(dir)[1] for dir in dir_names]
        performer_num = len(dir_names)

        info = ''

        for performer_dir in dir_names:
            (succeed, failed, new_names_dict) = rename_performer(performer_dir, self.format)
            performer_name = os.path.split(performer_dir)[1]
            info = info + performer_name + " -- " + str(succeed) + ' succeed, ' + str(failed) + ' failed.\n'
            for album_name in new_names_dict.keys():
                info = info + '\n<<' + album_name + '>>:\n'
                album_songs = new_names_dict[album_name]
                info = info + '\n'.join(album_songs)
                info = info + '\n'
            info = info + '\n\n'

        self.output.setText(info)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Renamer()
    ex.setWindowOpacity(0.95)
    sys.exit(app.exec_())