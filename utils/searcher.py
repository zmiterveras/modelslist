from PyQt5 import QtWidgets, QtCore


class Searcher:
    def __init__(self, instance):
        self.instance = instance
        self.classname = instance.__class__.__name__
        self.extend_result = []

    def printer(self):
        print("from searcher:")
        print(self.instance.__class__.__name__)
        self.instance.clear()

    def controller(self, param, value, sign):
        query_up = ''' where %s%s"%s"''' % (param, sign, value)
        if self.classname == "MyModels":
            self.modelsSearch(query_up)
        elif self.classname == "MyPhotos":
            self.photosSearch(query_up)
        else:
            self.sessionsSearch(query_up)

    def modelsSearch(self, query_up):
        self.instance.clear()
        self.instance.setModelListView(query_up)

    def photosSearch(self, query_up):
        self.instance.clear()
        self.instance.setPhotoListView(query_up)

    def sessionsSearch(self, query_up):
        self.instance.clear()
        self.instance.setSessionListView(query_up)


class SearcherController:
    def searcherWindow(self, instance, param, what, names, date, extend):
        def onFind():
            search_window_widget.findController()
            sr.close()
        #     if names:
        #         value = self.se.currentText()
        #     else:
        #         value = self.se.text()
        #     if value == '':
        #         QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
        #     else:
        #         self.searchFlag = True
        #         sign = '='
        #         print("mySearch")
        #         if date:
        #             sign = self.cb.currentText()
        #         self.controller(param, value, sign)
        #         srClose()

        def srClose():
            sr.close()

        sr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        srvbox = QtWidgets.QVBoxLayout()
        # searchword = 'Введите ' + what
        # sl = QtWidgets.QLabel(searchword)
        # srvbox.addWidget(sl)
        #############################################################
        search_window_widget = SearcherWindow(instance, param, what, names, date, extend)
        srvbox.addWidget(search_window_widget)
        #############################################################
        btn1 = QtWidgets.QPushButton('Найти')
        # if date:
        #     self.cb = QtWidgets.QComboBox()
        #     self.cb.addItems(['=', '>', '<', '>=', '<=', '!='])
        #     srvbox.addWidget(self.cb)
        # if names:
        #     self.se = QtWidgets.QComboBox()
        #     self.se.addItems(names)
        # else:
        #     self.se = QtWidgets.QLineEdit()
        #     self.se.returnPressed.connect(btn1.click)  # enter
        srhbox = QtWidgets.QHBoxLayout()
        btn2 = QtWidgets.QPushButton('Закрыть')
        btn1.clicked.connect(onFind)
        btn2.clicked.connect(srClose)
        # btn1.setAutoDefault(True)  # enter
        srhbox.addWidget(btn1)
        srhbox.addWidget(btn2)
        # srvbox.addWidget(self.se)
        srvbox.addLayout(srhbox)
        sr.setLayout(srvbox)
        sr.show()


########################################################################################################################
class SearcherWindow(QtWidgets.QWidget):
    def __init__(self, instance, search_column, what, names, date, extend, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.instance = instance
        self.search_column = search_column
        self.what = what
        self.names = names
        self.date = date
        self.extend = extend
        self.makeWidget()

    def makeWidget(self):
        self.main_box = QtWidgets.QVBoxLayout()
        what_search = 'Введите ' + self.what
        what_search_label = QtWidgets.QLabel(what_search)
        self.main_box.addWidget(what_search_label)
        if self.date:
            self.cb = self.dateComboBox()
            self.main_box.addWidget(self.cb)
        if self.names:
            self.search_item = QtWidgets.QComboBox()
            self.search_item.addItems(self.names)
        else:
            self.search_item = QtWidgets.QLineEdit()
        self.check_btn_extend = QtWidgets.QCheckBox('Расширенный поиск')
        self.check_box = QtWidgets.QVBoxLayout()
        self.check_btn_extend.clicked.connect(self.chooseExtendBox)
        self.main_box.addWidget(self.search_item)
        if self.extend:
            self.main_box.addWidget(self.check_btn_extend)
            self.main_box.addLayout(self.check_box)
        self.setLayout(self.main_box)

    def dateComboBox(self):
        cb = QtWidgets.QComboBox()
        cb.addItems(['=', '>', '<', '>=', '<=', '!='])
        return cb

    def addExtendBox(self):
        if self.check_btn_extend:
            pass

    def chooseExtendBox(self):
        if self.check_btn_extend.checkState():
            def get():
                choosed_lookup_item = []
                for n, ch_btn in enumerate(self.checkbtn_list):
                    if ch_btn.checkState():
                        choosed_lookup_item.append(self.extend[n])
                self.setExtendedLookup(choosed_lookup_item)

            self.checkbtn_list = []
            for i in self.extend:
                checkbtn = QtWidgets.QCheckBox('Поиск по: ' + i)
                self.check_box.addWidget(checkbtn)
                self.checkbtn_list.append(checkbtn)
            btn_get = QtWidgets.QPushButton('Ok')
            self.check_box.addWidget(btn_get)
            btn_get.clicked.connect(get)
        else:
            self.clearCheckBox()

    def setExtendedLookup(self, items):
        if not items:
            self.commonLookup()
        else:
            self.clearCheckBox()

    def clearCheckBox(self):
        for i in reversed(range(self.check_box.count())):
            wt = self.check_box.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()

    def findController(self):
        if self.check_btn_extend.checkState():
            self.extendLookup()
        else:
            self.commonLookup()

    def commonLookup(self):
        if self.names:
            value = self.search_item.currentText()
        else:
            value = self.search_item.text()
        if value == '':
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
        else:
            self.searchFlag = True
            sign = '='
            print("mySearch")
            if self.date:
                sign = self.cb.currentText()
            searcher = Searcher(self.instance)
            searcher.controller(self.search_column, value, sign)
        print("not check")


    def extendLookup(self):
        print("check")












"""
    def searcherWindow__(self, param, what, names, date, extend):
        def addExtend():
            if checkbtn.checkState():
                extendWindow()


        def extendWindow():
            def get():
                for n, btn in enumerate(checkbtn_list):
                    if btn.checkState():
                        self.extend_result.append(extend[i])
                        if self.extend_result:
                            groupBox()


            extend_search_window = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
            extend_search_window.setWindowTitle('Расширенный поиск')
            box = QtWidgets.QVBoxLayout()
            checkbtn_list = []
            for i in extend:
                checkbtn = QtWidgets.QCheckBox('Поиск по: ' + i)
                checkbtn_list.append(checkbtn)
            hbox = QtWidgets.QHBoxLayout()
            btn_get = QtWidgets.QPushButton('Ok')
            btn_close = QtWidgets.QPushButton('Close')
            hbox.addWidget(btn_get)
            hbox.addWidget(btn_close)
            btn_get.clicked.connect()
            btn_close.clicked.connect(extend_search_window.close)
            box.addLayout(hbox)
            extend_search_window.setLayout(box)
            extend_search_window.show()

        def groupBox():
            box = QtWidgets.QGroupBox('Расширенный поиск')
            vbox = QtWidgets.QVBoxLayout()
            for i in self.extend_result:
                if i == "Application":
                    cb_app = QtWidgets.QComboBox()
                    cb_app.addItems(self.instance.app_list)
                    vbox.addWidget(cb_app)
                elif i == "Location":
                    cb_loc = QtWidgets.QComboBox()
                    cb_loc.addItems(self.instance.loc_list)
                    vbox.addWidget(cb_loc)
                else:
                    label = QtWidgets.QLabel('Date [yyyy.mm.dd]')
                    cb_date = dateComboBox()
                    vbox.addWidget(cb_date)
                    date_line = QtWidgets.QLineEdit()
                    vbox.addWidget(date_line)
            box.setLayout(vbox)
            svrbox.addWidget(box)


        def dateComboBox():
            cb = QtWidgets.QComboBox()
            cb.addItems(['=', '>', '<', '>=', '<=', '!='])
            return cb



        def onFind():
            if names:
                value = self.se.currentText()
            else:
                value = self.se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
            else:
                self.searchFlag = True
                sign = '='
                print("mySearch")
                if date:
                    sign = self.cb.currentText()
                self.controller(param, value, sign)
                srClose()

        def srClose():
            sr.close()

        sr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        srvbox = QtWidgets.QVBoxLayout()
        searchword = 'Введите ' + what
        sl = QtWidgets.QLabel(searchword)
        srvbox.addWidget(sl)
        btn1 = QtWidgets.QPushButton('Найти')
        checkbtn = QtWidgets.QCheckBox('Расширенный поиск')
        checkbtn.clicked.connect(addExtend)
        if date:
            self.cb = dateComboBox()
            srvbox.addWidget(self.cb)
        if names:
            self.se = QtWidgets.QComboBox()
            self.se.addItems(names)
        else:
            self.se = QtWidgets.QLineEdit()
            self.se.returnPressed.connect(btn1.click)  # enter
        srhbox = QtWidgets.QHBoxLayout()
        btn2 = QtWidgets.QPushButton('Закрыть')
        btn1.clicked.connect(onFind)
        btn2.clicked.connect(srClose)
        btn1.setAutoDefault(True)  # enter
        srhbox.addWidget(btn1)
        srhbox.addWidget(btn2)
        srvbox.addWidget(self.se)
        if extend:
            srvbox.addWidget(checkbtn)
        srvbox.addLayout(srhbox)
        sr.setLayout(srvbox)
        sr.show()
"""





