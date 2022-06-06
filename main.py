# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QTextEdit, QFormLayout, QDialog# gui needing modules
import sys# for sys.argv in app.exec__
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioEncoderSettings, QMultimedia, QMediaPlaylist # to play media
from PyQt5.QtMultimediaWidgets import QVideoWidget # to play video
from PyQt5.QtGui import QIcon, QPalette # to style
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import *
from termcolor import cprint
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import threading # for threading
from PyQt5.QtGui import QFont as qtf
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import unittest
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

start_time = time.time() # calculating time
le_link = ""
link = ""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__() # getting functions from Qwidget

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))# setting things like icon size and name

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)# here we set the style of the window
        self.setPalette(p)
        self.dw_permission = False

        self.init_ui()# calling the function that initializes the UI
        self.show()
        # signals for later
        self.click = 0
    def init_ui(self):

        # create media player object

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object

        self.videowidget = QVideoWidget()
        # create open button
        openBtn = QPushButton('Open Video')
        openBtn.setFont(qtf("Arial"))
        openBtn.clicked.connect(self.open_file)
        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        # sound label
        self._soundicon = QPushButton()
        self._soundicon.setIcon(QIcon(self.style().standardIcon(QStyle.SP_MediaVolume)))
        self._soundicon.setEnabled(False)
        self._soundicon.setStyleSheet("background-color : black")
        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)

        self.slider.sliderMoved.connect(self.set_position)
        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # soudn adjusted
        self._slider = QSlider(minimum=0, maximum=100, sliderPosition=75, orientation=Qt.Horizontal,
                               sliderMoved=self.mediaPlayer.setVolume)


        #list layout
        self.listlayout = QVBoxLayout()
        self.list = QListWidget()
        self.list.setFont(qtf("Calibri", 12))
        self.listlayout.addWidget(self.list)
        # create download btn


        # checkbOX
        self.check = QCheckBox()
        self.check.setText("Loop")
        self.check.setFont(qtf("Arial"))
        self.check.setEnabled(False)
        self.check.stateChanged.connect(self.Loop)
        self.check.setStyleSheet("color : white")

        # set widgets to the hbox layout


        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.addWidget(openBtn)
        self.hboxLayout.addWidget(self.playBtn)
        self.hboxLayout.addWidget(self.slider)
        #self.hboxLayout.addWidget(self.downBtn)
        self.hboxLayout.addWidget(self.label)
        self.hboxLayout.addWidget(self.check)

        # intermediary layout
        self.hbox = QHBoxLayout()
        self.hboxLayout2_ = QHBoxLayout()
        self.hboxLayout2_.addWidget(self._soundicon)

        self.hboxLayout2_.addWidget(self._slider)
        self.hboxLayout.addLayout(self.hboxLayout2_)
        self.hboxLayout.addLayout(self.hbox)

        # create vbox layout
        self.vboxLayout = QVBoxLayout() ##########################
        self.vboxLayout.addWidget(self.videowidget)
        self.vboxLayout.addWidget(self.label)



        ############
        self._vboxLayout = QVBoxLayout()
        self._1vboxLayout = QVBoxLayout()
        self._vboxLayout.addLayout(self.hboxLayout)
        self.hbox = QHBoxLayout()

        self._vboxLayout.addLayout(self.vboxLayout)
        self._1vboxLayout.addLayout(self._vboxLayout)
        ################
        self.setLayout(self._1vboxLayout)
        self.mediaPlayer.setVideoOutput(self.videowidget)
        ##text edit
        self.downloadTextEdit = QLineEdit()

        #download init

        self.downloadbutton = QPushButton()
        self.downloadbutton.setIcon(QIcon(fr"{os.getcwd()}/downloadicon.jpg"))


        #making same size
        self.downloadbutton.setFixedHeight(22)
        self.downloadTextEdit.setFixedHeight(22)


        self.downloadFORMLAYOUT = QFormLayout()
        self.downloadFORMLAYOUT.minimumSize()
        self.downloadbutton.clicked.connect(self.download_signal)
        #########################

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        #singals

        self.list.itemSelectionChanged.connect(self.selectionChanged)
        self.list_with_the_items = []
        self.tmp_first_time = True
        self.thread_variable  = False

        MainWindow.tmp_first_time22 = True
        self.click2 = 0
    def selectionChanged(self):
        item = int(self.list.currentRow())
        object = self.list_with_the_items[item]
        self.path = f"{os.getcwd()}/data/{self.list_with_the_items[item]}"
        path = self.path
        if self.path != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.playBtn.setEnabled(True)
    def Loop(self):  # func that autoplays the video aka calling mediaplayer.play continuosly
        self.checkstatus = self.check.checkState()
        print(self.checkstatus)
        self.thread = threading.Thread(target=self.Loop_)
        self.thread.start();
    def Loop_(self):
        while True:
            try:
                time.sleep(1)
                value = int(self.slider.value())
                if value == self.duration:
                    while self.checkstatus == 2:
                        time.sleep(1)
                        self.mediaPlayer.play()  # if yes hten we call it ....
            except:
                cprint("durationERROR , failed in self.Loop_ EXCEPTION , uncheck box pls" , "red")
                break
    def open_file(self):
        first_time = True
        if self.click == 0 and first_time==True:

            self.vboxLayout.addLayout(self.downloadFORMLAYOUT)
            self.downloadFORMLAYOUT.addRow(self.downloadbutton, self.downloadTextEdit)
            self.downloadFORMLAYOUT.addRow(self.list)



            ######

            self.qti = QListWidgetItem
            files = os.listdir(fr"{os.getcwd()}/data/")
            for file in files:
                if self.tmp_first_time == True:
                    icon = QIcon(fr"{os.getcwd()}/icon.jpg")
                    self.list_widget = self.qti(icon , f"{str(file)}", self.list)
                    self.list_widget.setBackground(QColor('#A9A9A9'))
                    self.list_with_the_items.append(file)


            self.tmp_first_time = False
            self.click = self.click +1
            first_time =False
        if self.click == 1 and first_time == True:

            self.list.setParent(None)
            self.downloadTextEdit.setParent(None)
            self.downloadbutton.setParent(None)
            self.click = self.click -1
    def play_video(self):
        self.check.setEnabled(True)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()


        else:

            self.mediaPlayer.play()
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )
            ''' Here we have things that make the video play without errors ... nothing
            more to explain'''

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )
    def position_changed(self, position):
        self.slider.setValue(position)
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        self.duration = duration
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
    le_link = ""
    def download_signal(self):
        global link # working
        link = ""
        self.download_extract()
    def download_thread(self):
        word = r"https://www.youtube.com/watch?"
        global link
        if str(word) in str(link):
            print("link contains youtube video link (link)")
        else:
            self.runner = unittest.runner.TextTestRunner()
            try:
                unittest.main()
            finally:
                self.download_extract()

        self._download_thread_target_()
    def _download_thread_target_(self):# python injection XDD

        script_to_download_videos = rf'''
        import pytube
        for i in range(10):
            i = i + 1
            yt = pytube.YouTube(r"{str(link)}")
            yt.streams.first().download(fr"{os.getcwd()}")
        '''
        try:
            data_cache_for_links = open(fr"{os.getcwd()}/cache/data_cache_for_links.py", "x")
        except:
            pass
        
        with open(fr"{os.getcwd()}/cache/data_cache_for_links.py" , "w") as tar:
            tar.write(script_to_download_videos)

        tar.close()
        try:

           os.system(fr"cd {os.getcwd()}/cache/data_cache_for_links.py && python -m data_cache_for_links")
        except:
           os.system(rf"cd {os.getcwd()}/cache/data_cache_for_links.py && python -m data_cache_for_links")
    def download_extract(self):
        global link
        cprint("dialog initialized", "green")
        word = r"https://www.youtube.com/watch?"
        # here we write things that we run when we want to go in unittest search engine
        if word not in self.le_link:
            print("word doesnt contain youtube link")
            self.le_link = self.downloadTextEdit.text()
            global le_link
            le_link = self.le_link
        # download thread

        self.download_thread()
class SearchEngine(unittest.TestCase):
    @classmethod
    def setUpClass(self):         
        # init seach engine
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        #self.chrome_options.headless = True

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
    def test_Search_with_VideoName(self):
        link_for_driver = "https://www.youtube.com/results?search_query=" + str(le_link)
        self.driver.get(link_for_driver)
        try:
          main = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'thumbnail')))
        except:
            print('thumbnail" --- not found')
        youtube_first_video_renderer = self.driver.find_element(By.ID , 'thumbnail')
        global link
        link = youtube_first_video_renderer.get_attribute('href')
        return link
    def tearDown(self):
        super().tearDown()
        self.driver.close()
        time.sleep(5)
if __name__ == "__main__":  # gotta not be in the unittest class
    print("--- %s seconds ---" % (time.time() - start_time))
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

