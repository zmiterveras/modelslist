import datetime

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

    def controller(self, income):
        query_up = ''' where '''
        query_len = len(income)
        for i in income:
            query_up =  query_up + '''%s%s"%s"''' % (i[0], i[1], i[2])
            if query_len > 1:
                query_up += ''' and '''
                query_len -= 1
        if self.classname == "MyModels":
            self.modelsSearch(query_up)
        elif self.classname == "MyPhotos":
            self.photosSearch(query_up + ''' order by p.publish_data''')
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
    def __init__(self, instance, param, what, names, date, extend, date_col):
        self.instance = instance
        self.param = param
        self.what = what
        self.names = names
        self.date = date
        self.extend = extend
        self.date_col = date_col
        self.extends = []
        self.extend_flag = True
        # self.cb = None

    def searcherWindow(self):
        def dateComboBox():
            cb = QtWidgets.QComboBox()
            cb.addItems(['=', '>', '<', '>=', '<=', '!='])
            return cb

        def calendarField():
            calendar = QtWidgets.QDateEdit()
            calendar.setCalendarPopup(True)
            calendar.setDisplayFormat("yyyy.MM.dd")
            calendar.setDate(datetime.date.today())
            return calendar


        def onFind():
            searcher = Searcher(self.instance)
            values = []
            if self.names:
                value = self.se.currentText()
            else:
                value = self.se.text()
            if value == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
            else:
                self.searchFlag = True
                sign = '='
                if self.date:
                    sign = self.cb.currentText()
                if self.extends:
                    values = onExtendFind()
                searcher.controller([(self.param, sign, value)] + values)
                srClose()

        def onExtendFind():
            sign = '='
            values = []
            for text in self.extends:
                match text:
                    case "Application":
                        value = self.cb_app.currentText()
                        col = 'a.name'
                    case "Location":
                        value = self.cb_loc.currentText()
                        col = 'l.name'
                    case "Date":
                        sign = self.cb_date.currentText()
                        value = self.calendar_field.text()
                        # if value == '':
                        #     QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введены значения')
                        col = self.date_col
                if value == 'any': continue
                values.append((col, sign, value))
            return values


        def clearSearchChoice():
            for i in reversed(range(choice_extend_search_box.count())):
                wt = choice_extend_search_box.itemAt(i).widget()
                wt.setParent(None)
                wt.deleteLater()

        def choiceSearchField():
            if self.extend and self.extend_flag:
                choice_extend_search_box.addWidget(QtWidgets.QLabel('Выберите критерий поиска:'))
                self.cb_choice = QtWidgets.QComboBox()
                self.cb_choice.addItems(self.extend)
                self.cb_choice.currentIndexChanged.connect(addSearchField)
                choice_extend_search_box.addWidget(self.cb_choice)
                self.extend_flag = False
            else:
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбрано поле дополнительного поиска')


        def addSearchField():
            text  = self.cb_choice.currentText()
            self.extend_flag = True
            self.extends.append(text)
            self.extend.remove(text)
            if len(self.extend) == 1:
                self.btn_add.setEnabled(False)
            clearSearchChoice()
            extend_search_box.addWidget(QtWidgets.QLabel(text + ':'))
            match text:
                case "Application":
                    self.cb_app.addItems([i[1] for i in self.instance.app_list])
                    extend_search_box.addWidget(self.cb_app)
                case "Location":
                    self.cb_loc.addItems([i[1] for i in self.instance.loc_list])
                    extend_search_box.addWidget(self.cb_loc)
                case "Date":
                    extend_search_box.addWidget(self.cb_date)
                    extend_search_box.addWidget(self.calendar_field)

        def srClose():
            sr.close()

        sr = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        sr.setWindowTitle('Поиск')
        sr.setWindowModality(QtCore.Qt.WindowModal)
        sr.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        srvbox = QtWidgets.QVBoxLayout()
        main_searhc_box = QtWidgets.QVBoxLayout()
        extend_search_box = QtWidgets.QVBoxLayout()
        choice_extend_search_box = QtWidgets.QVBoxLayout()
        button_box = QtWidgets.QVBoxLayout()
        searchword = 'Введите ' + self.what
        sl = QtWidgets.QLabel(searchword)
        main_searhc_box.addWidget(sl)
        if self.date:
            self.cb = dateComboBox()
            main_searhc_box.addWidget(self.cb)
            self.se = calendarField()
        elif self.names:
            self.se = QtWidgets.QComboBox()
            self.se.addItems(self.names)
        else:
            self.se = QtWidgets.QLineEdit()
        main_searhc_box.addWidget(self.se)
        if self.extend:
            self.btn_add = QtWidgets.QPushButton('Добавить критерий')
            self.btn_add.clicked.connect(choiceSearchField)
            button_box.addWidget(self.btn_add)
            self.calendar_field = calendarField()
            self.cb_app = QtWidgets.QComboBox()
            self.cb_loc = QtWidgets.QComboBox()
            self.cb_date = dateComboBox()
        srhbox = QtWidgets.QHBoxLayout()
        btn_find = QtWidgets.QPushButton('Найти')
        btn_close = QtWidgets.QPushButton('Закрыть')
        btn_find.clicked.connect(onFind)
        btn_close.clicked.connect(srClose)
        srhbox.addWidget(btn_find)
        srhbox.addWidget(btn_close)
        button_box.addLayout(srhbox)
        srvbox.addLayout(main_searhc_box)
        srvbox.addLayout(extend_search_box)
        srvbox.addLayout(choice_extend_search_box)
        srvbox.addLayout(button_box)
        sr.setLayout(srvbox)
        sr.show()




