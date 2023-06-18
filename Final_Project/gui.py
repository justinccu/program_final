from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QMessageBox, QApplication, QWidget, QPushButton, QLabel
import subprocess
from PyQt5.QtGui import QFont,  QPalette, QBrush, QPixmap
import sys
import numpy as np
#from gensim.models import Word2Vec    Do "NOT" use it, only if you have downloaded our word embedding package
#model = Word2Vec.load('word2vec.model')
data = []


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(818, 500)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(100, 30, 211, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.listwidget = QListWidget(Form)
        self.listwidget.setGeometry(QtCore.QRect(20, 80, 291, 331))
        self.listwidget.setObjectName("listWidget")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 16))
        self.label.setObjectName("label")

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(350, 70, 401, 361))
        self.textBrowser.setObjectName("textBrowser")

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(340, 30, 361, 25))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.button_0 = QtWidgets.QPushButton(Form)
        self.button_0.setGeometry(QtCore.QRect(450, 450, 225, 25))  # modify
        self.button_0.setObjectName("button_0")

        self.button = QtWidgets.QPushButton(self.widget)
        self.button.setObjectName("button")

        self.horizontalLayout.addWidget(self.button)

        self.button_2 = QtWidgets.QPushButton(self.widget)
        self.button_2.setObjectName("button_2")

        self.horizontalLayout.addWidget(self.button_2)

        self.button_3 = QtWidgets.QPushButton(self.widget)
        self.button_3.setObjectName("button_3")

        self.horizontalLayout.addWidget(self.button_3)

        self.button_4 = QtWidgets.QPushButton(self.widget)
        self.button_4.setObjectName("button_4")

        self.horizontalLayout.addWidget(self.button_4)
        self.button.raise_()

        self.button_6 = QtWidgets.QPushButton(self.widget)
        self.button_6.setObjectName("button_6")

        self.horizontalLayout.addWidget(self.button_6)

        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(60, 430, 201, 25))
        self.widget1.setObjectName("widget1")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.button_5 = QtWidgets.QPushButton(self.widget1)
        self.button_5.setObjectName("button_5")
        self.horizontalLayout_2.addWidget(self.button_5)

        self.button_7 = QtWidgets.QPushButton(self.widget)
        self.button_7.setObjectName("button_7")

        self.horizontalLayout_2.addWidget(self.button_7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def generate_list_items(self, output):

        self.listwidget.clear()  # 清空原有的項目

        if output == '-1':
            QMessageBox.information(None, "提示", "找不到課程")
        else:
            outputs = output.split('\n')
            dictionary = {}  # 建立一個空的字典
            i = 0
            for item in outputs:

                if item.strip():  # 確保非空白輸出
                    dictionary[f"key{i+1}"] = item  # 將輸入字串加入字典
                    i = i+1
                    if(i == 11):
                        data.append(dictionary)  # 將字典加入列表
                        dictionary = {}  # 重新建立一個空的字典
                        i = 0

            for x in data:
                value1 = QtWidgets.QListWidgetItem(x.get("key5")).text()
                value2 = QtWidgets.QListWidgetItem(x.get("key4")).text()
                value3 = QtWidgets.QListWidgetItem(x.get("key3")).text()
                temp1 = value1.split(":", 1)
                temp2 = value2.split(":")
                temp3 = value3.split(":")
                listItem = temp1[1].strip() + "/" + \
                    temp3[1].strip() + "/" + temp2[1].strip()
                self.listwidget.addItem(listItem)

        self.listwidget.setCurrentRow(0)  # 設置預設選擇第一個項目

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate(
            "Form", "Course selection assistance system"))
        self.label.setText(_translate("Form", "在此輸入:"))
        self.button.setText("搜尋課程")
        self.button.clicked.connect(self.run_searching)
        self.button_2.setText("推薦課程")
        self.button_2.clicked.connect(self.run_recommand)
        self.button_3.setText("預覽課表")
        self.button_3.clicked.connect(self.run_classtable)
        self.button_4.setText("匯出課表")
        self.button_4.clicked.connect(self.run_exportfile)
        self.button_5.setText("加入選課")
        self.button_5.clicked.connect(self.run_addclass)
        self.button_0.setText("結束選課")
        self.button_0.clicked.connect(self.exit_sys)
        self.button_6.setText("列出課程")
        self.button_6.clicked.connect(self.run_listclass)
        self.button_7.setText("刪除課程")
        self.button_7.clicked.connect(self.run_deleteclass)

        self.listwidget.itemClicked.connect(self.show_selected_item)
        self.second_window = SecondWindow()

    def run_deleteclass(self):
        selected_item = self.listwidget.currentItem()
        selected_text = selected_item.text()

        split_text = selected_text.split("/")
        value1 = split_text[0].strip()
        value2 = split_text[2].strip()
        value3 = split_text[1].strip()
        for x in data:
            if ("Course Title: "+value1 == x.get("key5")) and ("Class Type: "+value2 == x.get("key4")) and ("Course ID: "+value3 == x.get("key3")):
                a = x.get("key3")
                split_key1 = a.split(":")

                result = subprocess.run(
                    ["./test.out", "6", split_key1[1], value2], capture_output=True, text=True)
                output = result.stdout.strip()
                QMessageBox.information(None, "提示", output)

        self.run_listclass()

    def run_listclass(self):
        result = subprocess.run(["./test.out", "5"],
                                capture_output=True, text=True)
        output = result.stdout

        data.clear()  # 清空 data 列表
        self.generate_list_items(output)

    def exit_sys(self):
        sys.exit()

    def run_recommand(self):
        # 轉換課程向量
        course_vector = np.zeros(100)
        i = 0
        with open('out.txt', 'r') as f:
            for line in f:
                words = line.strip().split()  # 去除每行前後的空白字符
                total_vectors = np.zeros(100)
                for word in words:
                    try:
                        vector = model.wv.get_vector(word)
                        total_vectors += vector
                    except KeyError:
                        continue
                course_vector = np.vstack(
                    (course_vector, total_vectors))  # 垂直堆疊行
                i += 1
        word_vectors = np.zeros(100)
        line = self.plainTextEdit.toPlainText()
        words = line.split
        for word in words():
            try:
                vector = model.wv.get_vector(word)
                word_vectors += vector
            except KeyError:
                continue

        array = ""
        course_count = 0
        for i in range(1, 1854):
            if (np.linalg.norm(word_vectors) == 0):
                continue
            if (np.linalg.norm(course_vector[i]) == 0):
                continue
            w2v_similarity = np.dot(word_vectors, course_vector[i]) / (
                np.linalg.norm(word_vectors)*np.linalg.norm(course_vector[i]))
            if(w2v_similarity >= 0.60):
                array = array + str(i-1) + ' ' + str(w2v_similarity) + ' '
                course_count += 1

        result = subprocess.run(
            ["./test.out", "4", str(course_count), array], capture_output=True, text=True)
        output = result.stdout
        #QMessageBox.information(None, "推薦", output)
        data.clear()  # 清空data列表
        self.generate_list_items(output)

    def run_classtable(self):
        # 創建並顯示第二個視窗
        self.second_window = SecondWindow()
        self.second_window.show()

    def run_exportfile(self):
        self.b_instance = SecondWindow()
        self.b_instance.grab_screenshot()

    def run_addclass(self):
        selected_item = self.listwidget.currentItem()
        if selected_item is None:
            QMessageBox.information(None, "提示", "請先選擇一項")
            return

        selected_text = selected_item.text()

        self.textBrowser.clear()  # 清空原有内容

        split_text = selected_text.split("/")
        value1 = split_text[0].strip()
        value2 = split_text[2].strip()
        value3 = split_text[1].strip()
        for x in data:
            if ("Course Title: "+value1 == x.get("key5")) and ("Class Type: "+value2 == x.get("key4")) and ("Course ID: "+value3 == x.get("key3")):
                a = x.get("key3")
                split_key1 = a.split(":")
                b = x.get("key4")
                split_key2 = b.split(":")
                c = x.get("key6")
                split_key4 = c.split(": ")
                result = subprocess.run(
                    ["./test.out", "2", split_key1[1], split_key2[1], split_key4[1]], capture_output=True, text=True)
                output = result.stdout.strip()
                QMessageBox.information(None, "提示", output)

    def run_searching(self):
        input_text = self.plainTextEdit.toPlainText()

        result = subprocess.run(
            ["./test.out", "1", input_text], capture_output=True, text=True)
        output = result.stdout

        data.clear()  # 清空 data 列表
        self.generate_list_items(output)

    def show_selected_item(self):
        selected_item = self.listwidget.currentItem()
        if selected_item:

            selected_text = selected_item.text()
            self.textBrowser.clear()  # 清空原有内容

            split_text = selected_text.split("/")
            value1 = split_text[0].strip()
            value2 = split_text[1].strip()
            value3 = split_text[2].strip()

            for x in data:
                if ("Course Title: "+value1 == x.get("key5")) and ("Class Type: "+value3 == x.get("key4")) and ("Course ID: "+value2 == x.get("key3")):

                    for key, value in x.items():
                        font = QFont()
                        font.setPointSize(13)  # 設置字體大小
                        self.textBrowser.setFont(font)
                        self.textBrowser.append(
                            f"{value}\n")  # 匹配的字印到textBrowser上


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('預覽課表')
        self.setGeometry(700, 150, 700, 700)
        # 創建QLabel作為背景圖片容器
        self.background_label = QLabel(self)
        self.background_label.setGeometry(self.rect())

        # 加載圖片
        pixmap = QPixmap('time_table.jpg')
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

        # 創建顯示框
        self.display_Mon_AB = QLabel(self)
        self.display_Mon_AB.setGeometry(97, 47, 138, 127)
        self.display_Mon_AB.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')  # 設置背景色
        self.display_Mon_AB.setWordWrap(True)  # 啟用自動換行
        self.display_Mon_AB.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Mon_CD = QLabel(self)
        self.display_Mon_CD.setGeometry(97, 178, 138, 127)
        self.display_Mon_CD.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Mon_CD.setWordWrap(True)  # 啟用自動換行
        self.display_Mon_CD.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Mon_EF = QLabel(self)
        self.display_Mon_EF.setGeometry(97, 310, 138, 127)
        self.display_Mon_EF.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Mon_EF.setWordWrap(True)  # 啟用自動換行
        self.display_Mon_EF.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Mon_GH = QLabel(self)
        self.display_Mon_GH.setGeometry(97, 441, 138, 127)
        self.display_Mon_GH.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Mon_GH.setWordWrap(True)  # 啟用自動換行
        self.display_Mon_GH.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Mon_IJ = QLabel(self)
        self.display_Mon_IJ.setGeometry(97, 572, 138, 127)
        self.display_Mon_IJ.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Mon_IJ.setWordWrap(True)  # 啟用自動換行
        self.display_Mon_IJ.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Tue_AB = QLabel(self)
        self.display_Tue_AB.setGeometry(240, 47, 102, 127)
        self.display_Tue_AB.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Tue_AB.setWordWrap(True)  # 啟用自動換行
        self.display_Tue_AB.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Tue_CD = QLabel(self)
        self.display_Tue_CD.setGeometry(240, 178, 102, 127)
        self.display_Tue_CD.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Tue_CD.setWordWrap(True)  # 啟用自動換行
        self.display_Tue_CD.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Tue_EF = QLabel(self)
        self.display_Tue_EF.setGeometry(240, 310, 102, 127)
        self.display_Tue_EF.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Tue_EF.setWordWrap(True)  # 啟用自動換行
        self.display_Tue_EF.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Tue_GH = QLabel(self)
        self.display_Tue_GH.setGeometry(240, 441, 102, 127)
        self.display_Tue_GH.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Tue_GH.setWordWrap(True)  # 啟用自動換行
        self.display_Tue_GH.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Tue_IJ = QLabel(self)
        self.display_Tue_IJ.setGeometry(240, 572, 102, 127)
        self.display_Tue_IJ.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Tue_IJ.setWordWrap(True)  # 啟用自動換行
        self.display_Tue_IJ.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Wed_AB = QLabel(self)
        self.display_Wed_AB.setGeometry(346, 45, 120, 129)
        self.display_Wed_AB.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Wed_AB.setWordWrap(True)  # 啟用自動換行
        self.display_Wed_AB.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Wed_CD = QLabel(self)
        self.display_Wed_CD.setGeometry(346, 178, 120, 129)
        self.display_Wed_CD.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Wed_CD.setWordWrap(True)  # 啟用自動換行
        self.display_Wed_CD.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Wed_EF = QLabel(self)
        self.display_Wed_EF.setGeometry(346, 310, 120, 129)
        self.display_Wed_EF.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Wed_EF.setWordWrap(True)  # 啟用自動換行
        self.display_Wed_EF.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Wed_GH = QLabel(self)
        self.display_Wed_GH.setGeometry(346, 441, 120, 129)
        self.display_Wed_GH.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Wed_GH.setWordWrap(True)  # 啟用自動換行
        self.display_Wed_GH.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Wed_IJ = QLabel(self)
        self.display_Wed_IJ.setGeometry(346, 572, 120, 129)
        self.display_Wed_IJ.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Wed_IJ.setWordWrap(True)  # 啟用自動換行
        self.display_Wed_IJ.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Thu_AB = QLabel(self)
        self.display_Thu_AB.setGeometry(469, 45, 104, 129)
        self.display_Thu_AB.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Thu_AB.setWordWrap(True)  # 啟用自動換行
        self.display_Thu_AB.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Thu_CD = QLabel(self)
        self.display_Thu_CD.setGeometry(469, 178, 104, 129)
        self.display_Thu_CD.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Thu_CD.setWordWrap(True)  # 啟用自動換行
        self.display_Thu_CD.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Thu_EF = QLabel(self)
        self.display_Thu_EF.setGeometry(469, 310, 104, 129)
        self.display_Thu_EF.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Thu_EF.setWordWrap(True)  # 啟用自動換行
        self.display_Thu_EF.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Thu_GH = QLabel(self)
        self.display_Thu_GH.setGeometry(469, 441, 104, 129)
        self.display_Thu_GH.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Thu_GH.setWordWrap(True)  # 啟用自動換行
        self.display_Thu_GH.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Thu_IJ = QLabel(self)
        self.display_Thu_IJ.setGeometry(469, 572, 104, 129)
        self.display_Thu_IJ.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Thu_IJ.setWordWrap(True)  # 啟用自動換行
        self.display_Thu_IJ.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Fri_AB = QLabel(self)
        self.display_Fri_AB.setGeometry(576, 45, 120, 130)
        self.display_Fri_AB.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Fri_AB.setWordWrap(True)  # 啟用自動換行
        self.display_Fri_AB.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Fri_CD = QLabel(self)
        self.display_Fri_CD.setGeometry(576, 178, 120, 130)
        self.display_Fri_CD.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Fri_CD.setWordWrap(True)  # 啟用自動換行
        self.display_Fri_CD.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Fri_EF = QLabel(self)
        self.display_Fri_EF.setGeometry(576, 310, 120, 130)
        self.display_Fri_EF.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Fri_EF.setWordWrap(True)  # 啟用自動換行
        self.display_Fri_EF.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Fri_GH = QLabel(self)
        self.display_Fri_GH.setGeometry(576, 441, 120, 130)
        self.display_Fri_GH.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Fri_GH.setWordWrap(True)  # 啟用自動換行
        self.display_Fri_GH.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        self.display_Fri_IJ = QLabel(self)
        self.display_Fri_IJ.setGeometry(576, 572, 120, 130)
        self.display_Fri_IJ.setStyleSheet(
            'background-color: rgba(255, 255, 255, 0.5);')
        self.display_Fri_IJ.setWordWrap(True)  # 啟用自動換行
        self.display_Fri_IJ.setFont(QtGui.QFont("Arial", 10))  # 設定字體大小

        result = subprocess.run(
            ["./test.out", "3"], capture_output=True, text=True)
        output = result.stdout

        classes = output.split("\n")

        count = 0
        for item in classes:
            if count == 0:
                className = item
                count += 1
            elif count == 1:
                time = item.split(' ')
                count -= 1

                for times in time:
                    sessions = times.split('.')

                    session_ = sessions[1].split(',')

                    for session in session_:
                        # (sessions[0],session, "~~")

                        if sessions[0] == "Mon" and (session == "1" or session == "2" or session == "3" or session == "A" or session == "B"):
                            current_text = self.display_Mon_AB.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Mon_AB.setText(updated_text)
                        elif sessions[0] == "Mon" and (session == "4" or session == "5" or session == "6" or session == "C" or session == "D"):
                            current_text = self.display_Mon_CD.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Mon_CD.setText(updated_text)
                        elif sessions[0] == "Mon" and (session == "7" or session == "8" or session == "9" or session == "E" or session == "F"):
                            current_text = self.display_Mon_EF.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Mon_EF.setText(updated_text)
                        elif sessions[0] == "Mon" and (session == "10" or session == "11" or session == "12" or session == "G" or session == "H"):
                            current_text = self.display_Mon_GH.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Mon_GH.setText(updated_text)
                        elif sessions[0] == "Mon" and (session == "13" or session == "14" or session == "15" or session == "I" or session == "J"):
                            current_text = self.display_Mon_IJ.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Mon_IJ.setText(updated_text)

                        elif sessions[0] == "Tue" and (session == "1" or session == "2" or session == "3" or session == "A" or session == "B"):
                            current_text = self.display_Tue_AB.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Tue_AB.setText(updated_text)
                        elif sessions[0] == "Tue" and (session == "4" or session == "5" or session == "6" or session == "C" or session == "D"):
                            current_text = self.display_Tue_CD.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Tue_CD.setText(updated_text)
                        elif sessions[0] == "Tue" and (session == "7" or session == "8" or session == "9" or session == "E" or session == "F"):
                            current_text = self.display_Tue_EF.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Tue_EF.setText(updated_text)
                        elif sessions[0] == "Tue" and (session == "10" or session == "11" or session == "12" or session == "G" or session == "H"):
                            current_text = self.display_Tue_GH.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Tue_GH.setText(updated_text)
                        elif sessions[0] == "Tue" and (session == "13" or session == "14" or session == "15" or session == "I" or session == "J"):
                            current_text = self.display_Tue_IJ.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Tue_IJ.setText(updated_text)

                        elif sessions[0] == "Wed" and (session == "1" or session == "2" or session == "3" or session == "A" or session == "B"):
                            current_text = self.display_Wed_AB.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Wed_AB.setText(updated_text)
                        elif sessions[0] == "Wed" and (session == "4" or session == "5" or session == "6" or session == "C" or session == "D"):
                            current_text = self.display_Wed_CD.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Wed_CD.setText(updated_text)
                        elif sessions[0] == "Wed" and (session == "7" or session == "8" or session == "9" or session == "E" or session == "F"):
                            current_text = self.display_Wed_EF.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Wed_EF.setText(updated_text)
                        elif sessions[0] == "Wed" and (session == "10" or session == "11" or session == "12" or session == "G" or session == "H"):
                            current_text = self.display_Wed_GH.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Wed_GH.setText(updated_text)
                        elif sessions[0] == "Wed" and (session == "13" or session == "14" or session == "15" or session == "I" or session == "J"):
                            current_text = self.display_Wed_IJ.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Wed_IJ.setText(updated_text)

                        elif sessions[0] == "Thu" and (session == "1" or session == "2" or session == "3" or session == "A" or session == "B"):
                            current_text = self.display_Thu_AB.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Thu_AB.setText(updated_text)
                        elif sessions[0] == "Thu" and (session == "4" or session == "5" or session == "6" or session == "C" or session == "D"):
                            current_text = self.display_Thu_CD.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Thu_CD.setText(updated_text)
                        elif sessions[0] == "Thu" and (session == "7" or session == "8" or session == "9" or session == "E" or session == "F"):
                            current_text = self.display_Thu_EF.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Thu_EF.setText(updated_text)
                        elif sessions[0] == "Thu" and (session == "10" or session == "11" or session == "12" or session == "G" or session == "H"):
                            current_text = self.display_Thu_GH.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Thu_GH.setText(updated_text)
                        elif sessions[0] == "Thu" and (session == "13" or session == "14" or session == "15" or session == "I" or session == "J"):
                            current_text = self.display_Thu_IJ.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Thu_IJ.setText(updated_text)

                        elif sessions[0] == "Fri" and (session == "1" or session == "2" or session == "3" or session == "A" or session == "B"):
                            current_text = self.display_Fri_AB.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Fri_AB.setText(updated_text)
                        elif sessions[0] == "Fri" and (session == "4" or session == "5" or session == "6" or session == "C" or session == "D"):
                            current_text = self.display_Fri_CD.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Fri_CD.setText(updated_text)
                        elif sessions[0] == "Fri" and (session == "7" or session == "8" or session == "9" or session == "E" or session == "F"):
                            current_text = self.display_Fri_EF.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Fri_EF.setText(updated_text)
                        elif sessions[0] == "Fri" and (session == "10" or session == "11" or session == "12" or session == "G" or session == "H"):
                            current_text = self.display_Fri_GH.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Fri_GH.setText(updated_text)
                        elif sessions[0] == "Fri" and (session == "13" or session == "14" or session == "15" or session == "I" or session == "J"):
                            current_text = self.display_Fri_IJ.text()
                            new_text = className + '(' + session + ')'
                            updated_text = f"{current_text}\n{new_text}"
                            self.display_Fri_IJ.setText(updated_text)

    def grab_screenshot(self):
        # 截圖並保存到指定文件
        pixmap = self.grab()
        pixmap.save("courses.jpg", "JPG")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
