#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# inheriting branch

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys, sqlite3, random, os, time, datetime
from handleSql import HandleSql


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.version = '''1'''
        QtWidgets.QMainWindow.__init__(self, parent)
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        # self.wp = os.path.join(self.app_dir, 'images')
        # ico_path = os.path.join(self.wp, 'dic.png')
        # ico = QtGui.QIcon(ico_path)
        # self.setWindowIcon(ico)
        # self.view = MyView(self.app_dir)
        self.view = CentralWidget(self.app_dir)
        self.setCentralWidget(self.view)
        menuBar = self.menuBar()
        myNotes = menuBar.addMenu('&Notes')
        # action = myNotes.addAction('Add Model')
        action = myNotes.addAction('Add Application', self.view.addLocApp)
        action = myNotes.addAction('Add Location', lambda x="Location": self.view.addLocApp(x))
        # action = myNotes.addAction('Add Photo')
        #action = myMenu.addAction('Test',  self.test)
        myEdit = menuBar.addMenu('&Edit notes')
        action = myEdit.addAction('Delete application')
        action = myEdit.addAction('Delete Location')
        action = myEdit.addAction('Change Application')
        action = myEdit.addAction('Change Location')
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе') #, self.aboutProgramm)
        action = myAbout.addAction('Обо мне') #, self.aboutMe)
        self.statusBar = self.statusBar()
        self.view.btn_close.clicked.connect(self.close)

    def closeEvent(self, e):
        e.accept()
        QtWidgets.QWidget.closeEvent(self, e)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, root_path, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.root_path = root_path
        self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.handlersql = HandleSql()
        self.models = []
        self.names = []
        if not os.path.exists("bases/models.sqlite"):
            print("Not database")
            self.createDataBase()
        else:
            print("There is database")
        self.makeWidget()

    def createDataBase(self):
        conn, query = self.handlersql.connectBase(self.database)
        if 'Models' not in conn.tables():
            querystr1 = '''create table Models (id integer primary key autoincrement,
            name text, origin text, ed_work text)'''
            query.exec(querystr1)
            query.clear()
        if 'Application' not in conn.tables():
            querystr2 = """create table Application (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr2)
            query.clear()
            query.prepare("insert into Application values (null, ?)")
            query.addBindValue('any')
            query.exec_()
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
            query.prepare("insert into Location values (null, ?)")
            query.addBindValue('any')
            query.exec_()
            query.clear()
        if 'Photos' not in conn.tables():
            querystr4 = """create table Photos (id integer primary key autoincrement,
            name text, model_id integer, application_id integer, location_id integer, publish_data text)"""
            query.exec(querystr4)
            query.clear()
        if 'Sessions' not in conn.tables():
            querystr5 = """create table Sessions (id integer primary key autoincrement,
            model_id integer, location_desc text, equipment text, session_date text)"""
            query.exec(querystr5)
            query.clear()
        if 'Contacts' not in conn.tables():
            querystr6 = '''create table Contacts (id integer primary key autoincrement,
            model_id integer, phone text, email text, ref_s text)'''
            query.exec(querystr6)
            query.clear()
        conn.close()

    def makeWidget(self):
        self.main_box = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.bottom_box = QtWidgets.QHBoxLayout()
        self.viewWidget = MyView(self.database, self.handlersql)
        self.setControlButtons()
        # self.vbox.addWidget(self.viewWidget)
        # self.main_box.addLayout(self.vbox)
        self.main_box.addWidget(self.viewWidget)
        self.main_box.addLayout(self.bottom_box)
        self.setLayout(self.main_box)
        self.models = self.viewWidget.modelslist
        self.names = self.viewWidget.modelnames

    def setControlButtons(self):
        for i, f in (('Models', self.viewModels), ('Photos', self.viewPhotos), ('Sessions', self.viewSessions)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.bottom_box.addWidget(btn)
        self.btn_close = QtWidgets.QPushButton('Close')
        self.bottom_box.addWidget(self.btn_close)

    def clearVBox(self):
        wt = self.main_box.itemAt(0).widget()
        wt.setParent(None)
        wt.deleteLater()
        # for i in reversed(range(self.vbox.count())):
        #     wt = self.vbox.itemAt(i).widget()
        #     print("wt: ", wt)
        #     wt.setParent(None)
        #     wt.deleteLater()

    def viewModels(self):
        print("viewModels")
        if self.viewWidget.__class__.__name__ == "MyView":
            print("In MyView")
        else:
            self.clearVBox()
            self.viewWidget = MyView(self.database, self.handlersql)
            self.main_box.insertWidget(0, self.viewWidget)

    def viewPhotos(self):
        print("viewPhotos")
        if self.viewWidget.__class__.__name__ == "MyPhotos":
            print("In MyPhotos")
        else:
            self.clearVBox()
            self.viewWidget = MyPhotos(self.database, self.handlersql, self.models, self.names)
            self.main_box.insertWidget(0, self.viewWidget)

    def viewSessions(self):
        print("viewSessions")
        if self.viewWidget.__class__.__name__ == "MySessions":
            print("In MySessions")
        else:
            self.clearVBox()
            self.viewWidget = MySessions(self.database, self.handlersql, self.models, self.names)
            self.main_box.insertWidget(0, self.viewWidget)

    def addLocApp(self, alias="Application"):
        print("addLocApp")
        if self.viewWidget.__class__.__name__ == "LocAppHandler" and self.viewWidget.alias == alias:
                print("from widget", self.viewWidget.alias)
                print("here", alias)
                print("In LocAppHandler")
        else:
            self.clearVBox()
            self.viewWidget = LocAppHandler(self.database, self.handlersql, alias)
            self.main_box.insertWidget(0, self.viewWidget)


class Viewer(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

    def makeWidget(self):
        self.top_box = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.top_box.addLayout(self.vbox)
        self.top_box.addLayout(self.hbox)
        self.setLayout(self.top_box)

    def clear(self):
        for i in reversed(range(self.vbox.count())):
            wt = self.vbox.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()
        for i in reversed(range(self.hbox.count())):
            wb = self.hbox.itemAt(i).widget()
            wb.setParent(None)
            wb.deleteLater()

    def setListView(self, query, names, database, handlersql, columns):
        self.clear()
        handlersql.connectBase(database)
        self.stm = QtSql.QSqlQueryModel(parent=None)
        self.stm.setQuery(query)
        self.stm.sort(1, QtCore.Qt.AscendingOrder)
        for (i, n) in names:
            self.stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        self.tv = QtWidgets.QTableView()
        self.tv.setModel(self.stm)
        self.tv.hideColumn(0)
        for i, n in columns:
            self.tv.setColumnWidth(i, n)
        self.vbox.addWidget(self.tv)

    def getRow(self, col):
        row_number = self.tv.currentIndex().row()
        row = []
        for i in range(col):
            index = self.stm.index(row_number, i)
            row.append(self.stm.data(index))
        print('Selected row: ', row)
        return row

    def change(self, datalist, nameslist, col, flag='change'):
        if not datalist:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Отсутствуют данные для изменения')
            return
        row = self.getRow(col)
        if None in row:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не выбраны данные для изменения')
            return 1, row
        if flag == 'change':
            text = 'Вы действительно хотите изменить запись:\n'
        else:
            text = 'Вы действительно хотите удалить запись:\n'
        for name, data in zip(nameslist, row[1:]):
            text += name + ": " + data + "\n"
        result = QtWidgets.QMessageBox.question(None, 'Предупреждение', text,
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        return result, row

    def getLocApp(self, handlersql, database):
        query_loc = "select * from Location"
        query_app = "select * from Application"
        conn, query = handlersql.connectBase(database)  # connectBase(self.database)
        query.exec(query_loc)
        if query.isActive():
            query.first()
            while query.isValid():
                self.loc_list.append((query.value('id'), query.value('name')))
                query.next()
        query.clear()
        query.exec(query_app)
        if query.isActive():
            query.first()
            while query.isValid():
                self.app_list.append((query.value('id'), query.value('name')))
                query.next()
        conn.close()
        print("App: ", self.app_list)
        print("Loc: ", self.loc_list)


class LocAppHandler(Viewer):
    def __init__(self, database, handlersql, alias):
        Viewer.__init__(self)
        self.database = database
        self.handlersql = handlersql
        self.alias = alias
        self.newitem = []
        self.changeditem = []
        self.app_list = []
        self.loc_list = []
        self.getLocApp(self.handlersql, self.database)
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        self.setLocAppListView(self.alias)

    def setLocAppListView(self, alias):
        if alias == "Application":
            query = "select id, name from Application"
            names = [(1, "Приложение")]
        else:
            query = "select id, name from Location"
            names = [(1, "Тип локации")]
        columns = [(1, 150)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setEditButton()

    def setEditButton(self):
        for i, f in (('Add', self.addItem), ('Change', self.changeItem), ('Delete', self.deleteItem)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addItem(self, a, new=('', ''), flag=None):
        def getName():
            value1 = lE_name.text()
            if value1 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введено имя')
            else:
                if self.alias == "Application":
                    if value1 in [x[1] for x in self.app_list]:
                        QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данное приложение уже существует')
                        return
                else:
                    if value1 in [x[1] for x in self.loc_list]:
                        QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Данная локация уже существует')
                        return
                if flag == 1:
                    txt = 'Изменена запись о ' + self.alias +': '
                    self.changeditem = [new[0], value1]
                    print("Changed:\n", self.changeditem)
                    if self.alias == "Application":
                        self.app_list.pop(int(new[0])-1)
                        self.app_list.insert(int(new[0])-1, (int(new[0]), value1))
                    else:
                        self.loc_list.pop(int(new[0]) - 1)
                        self.loc_list.insert(int(new[0]) - 1, (int(new[0]), value1))
                    self.saveChangedItem()
                else:
                    txt = 'Добавлено ' + self.alias + ': '
                    if self.alias == "Application":
                        self.app_list.append((self.app_list[-1][0]+1, value1))
                    else:
                        self.loc_list.append((self.loc_list[-1][0] + 1, value1))
                    self.newitem = [value1]
                    print("Newitem:\n", self.newitem)
                    self.saveItem()
                # print("Refreshed modelslist:\n", self.modelslist)
                # print("Refreshed modelnames:\n", self.modelnames)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.setLocAppListView(self.alias)
                tladd_model.close()
        tladd_model = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tladd_model.setWindowTitle('Добавить')
        tladd_model.setWindowModality(QtCore.Qt.WindowModal)
        tladd_model.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_name = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        lE_name.setText(new[1])
        if flag == 1:
            tladd_model.setWindowTitle('Изменить')
        form.addRow('Имя:*', lE_name)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_model.close)
        tladd_model.setLayout(form)
        tladd_model.show()

    def saveItem(self):
        if self.alias == "Application":
            self.handlersql.insertQuery(self.database, "Application", [":name"], self.newitem)
        else:
            self.handlersql.insertQuery(self.database, "Location", [":name"], self.newitem)

    def changeItem(self):
        if self.alias == "Application":
            nameslist = ['Приложение']
            item_list = self.app_list
        else:
            nameslist = ['Локация']
            item_list = self.loc_list
        result, row = Viewer.change(self, item_list, nameslist, 2)
        if result == 16384:
            self.addItem(None, row, 1)
        else:
            return
        pass

    def saveChangedItem(self):
        if self.alias == "Application":
            self.handlersql.updateQuery(self.database, "Application", ["name", "id"], self.changeditem[1:] +
                                        self.changeditem[:1])
        else:
            self.handlersql.updateQuery(self.database, "Location", ["name", "id"], self.changeditem[1:] +
                                        self.changeditem[:1])

    def deleteItem(self):
        if self.alias == "Application":
            nameslist = ['Приложение']
            item_list = self.app_list
        else:
            nameslist = ['Локация']
            item_list = self.loc_list
        result, row = Viewer.change(self, item_list, nameslist, 2, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, self.alias, "id", row[0])
            self.clear()
            self.setLocAppListView(self.alias)
        else:
            return


class MyView(Viewer): #(QtWidgets.QWidget):
    def __init__(self, database, handlersql): #, parent=None):
        Viewer.__init__(self)
        # self.root_path = root_path
        # self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.database = database
        self.modelslist = []
        self.modelnames = []
        self.newmodel = []
        self.changedmodel = []
        self.handlersql = handlersql
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        if self.checkModelsList():
            self.setModelListView()
        else:
            label = QtWidgets.QLabel('Models List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setModelsEditButton()

    def checkModelsList(self):
        models_count = False
        querystr = "select id, name from Models"
        conn, query = self.handlersql.connectBase(self.database) #connectBase(self.database)
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            while query.isValid():
                self.modelslist.append((query.value('id'), query.value('name')))
                self.modelnames.append(query.value('name'))
                query.next()
        if len(self.modelslist):
            models_count = True
            print("Valid")
            print("Start modellist:\n", self.modelslist)
            print("Start modelnames:\n", self.modelnames)
        else:
            print("not valid")
        conn.close()
        return models_count

    def setModelListView(self):
        query = """select m.id, m.name, m.origin, m.ed_work, c.phone, c.email, c.ref_s 
        from Models m inner join Contacts c on m.id = c.model_id"""
        names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа'), (4, 'Phone'), (5, 'Email'), (6, 'References')]
        columns = [(1, 220), (2, 130), (3, 250), (4, 120), (5, 165), (6, 165)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setModelsEditButton()

    def setModelsEditButton(self):
        for i, f in (('AddModel', self.addModel), ('ChangeModel', self.changeModel), ('DeleteModel', self.deleteModel)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addModel(self,  a, new=('', '', '', '', '', '', ''), flag=None):
        def getName():
            value1 = lE_name.text()
            value2 = lE_origin.text()
            value3 = lE_ed_work.text()
            value4 = lE_phone.text()
            value5 = lE_email.text()
            value6 = lE_references.text()
            if value1 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не введено имя')
            else:
                if value1 in list(self.modelnames) and not flag:
                    result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                            'Модель с похожим именем есть в списке.\n' +
                                                            'Хотите продолжить?',
                                                            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            defaultButton=QtWidgets.QMessageBox.No)
                    if result == 16384:
                        pass
                    else:
                        return
                if flag == 1:
                    txt = 'Изменена запись о модели: '
                    self.changedmodel = [new[0], value1, value2, value3, value4, value5, value6]
                    print("Changed model:\n", self.changedmodel)
                    self.modelslist.pop(int(new[0])-1)
                    self.modelslist.insert(int(new[0])-1, (int(new[0]), value1))
                    self.saveChangedModel()
                else:
                    txt = 'Добавлена модель: '
                    if self.modelslist:
                        self.modelslist.append((self.modelslist[-1][0] + 1, value1)) # adedd(id, name)
                    else:
                        self.modelslist.append((1, value1))
                    self.modelnames.append(value1)
                    self.newmodel = [value1, value2, value3, value4, value5, value6]
                    print("Newmodel:\n", self.newmodel)
                    self.saveModel()
                print("Refreshed modelslist:\n", self.modelslist)
                print("Refreshed modelnames:\n", self.modelnames)
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value1)
                self.clear()
                self.setModelListView()
                tladd_model.close()
        tladd_model = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tladd_model.setWindowTitle('Добавить')
        tladd_model.setWindowModality(QtCore.Qt.WindowModal)
        tladd_model.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        lE_name = QtWidgets.QLineEdit()
        lE_origin = QtWidgets.QLineEdit()
        lE_ed_work = QtWidgets.QLineEdit()
        lE_phone = QtWidgets.QLineEdit()
        lE_email = QtWidgets.QLineEdit()
        lE_references = QtWidgets.QLineEdit()
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        k = 1
        for i in (lE_name, lE_origin, lE_ed_work, lE_phone, lE_email, lE_references):
            i.setText(new[k])
            k += 1
        if flag == 1:
            tladd_model.setWindowTitle('Изменить')

        form.addRow('Имя модели:*', lE_name)
        form.addRow('Откуда:', lE_origin)
        form.addRow('Учеба/Работа:', lE_ed_work)
        form.addRow('Телефон:', lE_phone)
        form.addRow('Email:', lE_email)
        form.addRow('Ссылки:', lE_references)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_model.close)
        tladd_model.setLayout(form)
        tladd_model.show()

    def changeModel(self):
        nameslist = ['Имя', 'Откуда', 'Учеба/Работа', 'Телефон', 'Email', 'Ссылки']
        result, row = Viewer.change(self, self.modelslist, nameslist, 7)
        if not row: return
        if result == 16384:
            self.addModel(None, row, 1)
        else:
            return

    def saveModel(self):
        self.handlersql.insertQuery(self.database, "Models", [":name", ":origin", ":ed_work"], self.newmodel[:3])
        args = self.newmodel[3:]
        args.insert(0, self.modelslist[-1][0])
        self.handlersql.insertQuery(self.database, "Contacts", [":model_id", ":phone", ":email", ":ref_s"], args)

    def saveChangedModel(self):
        self.handlersql.updateQuery(self.database, "Models", ["name", "origin", "ed_work", "id"],
                                    self.changedmodel[1:4] + self.changedmodel[:1])
        self.handlersql.updateQuery(self.database, "Contacts", ["phone", "email", "ref_s", "model_id"],
                                    self.changedmodel[4:] + self.changedmodel[:1])

    def deleteModel(self):
        nameslist = ['Имя', 'Откуда', 'Учеба/Работа', 'Телефон', 'Email', 'Ссылки']
        result, row = Viewer.change(self, self.modelslist, nameslist, 7, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Contacts", "model_id", row[0])
            self.handlersql.deleteQuery(self.database, "Models", "id", row[0])
            self.clear()
            self.setModelListView()
        else:
            return

    def test(self):
        print('test')


class MyPhotos(Viewer):
    def __init__(self, database, handlersql, models, names):
        Viewer.__init__(self)
        self.database = database
        self.photoslist = []
        self.newphoto = []
        self.changedphoto = []
        self.handlersql = handlersql
        self.models = models
        self.names = names
        self.loc_list = []
        self.app_list = []
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        self.getLocApp(self.handlersql, self.database)
        if self.checkPhotosList():
            self.setPhotoListView()
        else:
            label = QtWidgets.QLabel('Photos List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setPhotosEditButton()

    # def getLocApp(self):
    #     query_loc = "select * from Location"
    #     query_app = "select * from Application"
    #     conn, query = self.handlersql.connectBase(self.database)  # connectBase(self.database)
    #     query.exec(query_loc)
    #     if query.isActive():
    #         query.first()
    #         while query.isValid():
    #             self.loc_list.append((query.value('id'), query.value('name')))
    #             query.next()
    #     query.clear()
    #     query.exec(query_app)
    #     if query.isActive():
    #         query.first()
    #         while query.isValid():
    #             self.app_list.append((query.value('id'), query.value('name')))
    #             query.next()
    #     conn.close()
    #     print("App: ", self.app_list)
    #     print("Loc: ", self.loc_list)

    def checkPhotosList(self):
        photos_count = False
        querystr = "select id, name, model_id from Photos"
        conn, query = self.handlersql.connectBase(self.database) #connectBase(self.database)
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            while query.isValid():
                self.photoslist.append((query.value('id'), query.value('name'), query.value('model_id')))
                query.next()
        if len(self.photoslist):
            photos_count = True
            print("Valid")
            print("Start photoslist:\n", self.photoslist)
        else:
            print("not valid")
        conn.close()
        return photos_count

    def setPhotoListView(self):
        query = """select p.id, m.name, p.name, a.name, p.publish_data, l.name 
        from Photos p inner join Models m on p.model_id = m.id
        inner join Application a on p.application_id = a.id
        inner join Location l on p.location_id = l.id """
        names = [(1, 'Модель'), (2, 'Фото'), (3, 'Приложение'), (4, 'Дата публикации'),  (5, 'Тип локации')]
        columns = [(1, 250), (2, 100), (3, 150), (4, 90), (5, 150)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setPhotosEditButton()

    def setPhotosEditButton(self):
        for i, f in (('AddPhoto', self.addPhoto), ('ChangePhoto', self.changePhoto), ('DeletePhoto', self.deletePhoto)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addPhoto(self, a, new=('', '', '', '', '', ''), flag=None):
        def getName():
            value1 = cb_modelsname.currentIndex()
            value2 = lE_photo.text()
            value3 = cb_app.currentIndex()
            value4 = cb_loc.currentIndex()
            value5 = calendar.text()
            if value2 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Не задано фото')
            else:
                if flag == 1:
                    txt = 'Изменено слово: '
                    self.changedphoto = [new[0], value2, self.models[value1][0], self.app_list[value3][0],
                                         self.loc_list[value4][0], value5]
                    print("Changed photo:\n", self.changedphoto)
                    self.photoslist.pop(int(new[0]) - 1)
                    self.photoslist.insert(int(new[0]) - 1, (int(new[0]), value2, self.models[value1][0]))
                    self.saveChangedPhoto()
                else:
                    txt = 'Добавлено фото: '
                    if self.photoslist:
                        self.photoslist.append((self.photoslist[-1][0] + 1, value2, self.models[value1][0]))  # adedd(id, name, model_id)
                    else:
                        self.photoslist.append((1, value2, self.models[value1][0]))
                    self.newphoto = [value2, self.models[value1][0], self.app_list[value3][0],
                                     self.loc_list[value4][0], value5]
                    print("Newphoto:\n", self.newphoto)
                    self.savePhoto()
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value2)
                self.clear()
                self.setPhotoListView()
                tladd_photo.close()

        if not self.names:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Отсутствуют модели для связи с фото.\n' +
                                          'Добавте моделей!')
            return
        tladd_photo = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tladd_photo.setWindowTitle('Добавить')
        # tladd_photo.setWindowModality(QtCore.Qt.WindowModal)
        # tladd_photo.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        cb_modelsname = QtWidgets.QComboBox()
        cb_modelsname.addItems(self.names)
        lE_photo = QtWidgets.QLineEdit()
        cb_app = QtWidgets.QComboBox()
        cb_app.addItems([i[1] for i in self.app_list]) #[i[1] for i in self.app_list]
        cb_loc = QtWidgets.QComboBox()
        cb_loc.addItems([i[1] for i in self.loc_list])
        calendar = QtWidgets.QDateEdit()
        calendar.setCalendarPopup(True)
        calendar.setDisplayFormat("dd.MM.yyyy")
        calendar.setDate(datetime.date.today())
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        lE_photo.setText(new[1])
        if flag == 1:
            tladd_photo.setWindowTitle('Изменить')
            for i, n in (zip((cb_modelsname, cb_app, cb_loc), [new[1], new[3], new[-1]])):
                i.setCurrentText(n)
            lE_photo.setText(new[2])
            datelist = new[-2].split('.')
            calendar.setDate(QtCore.QDate(int(datelist[2]), int(datelist[1]), int(datelist[0])))
        form.addRow('Имя модели:', cb_modelsname)
        form.addRow('Фото:', lE_photo)
        form.addRow('Приложение:', cb_app)
        form.addRow('Вид локации:', cb_loc)
        form.addRow('Дата публикации:', calendar)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_photo.close)
        tladd_photo.setLayout(form)
        tladd_photo.show()

    def savePhoto(self):
        self.handlersql.insertQuery(self.database, "Photos", [":name", ":model_id", ":application_id",
                                                              ":location_id", ":publish_data"], self.newphoto)

    def changePhoto(self):
        nameslist = ['Имя модели', 'Фото', 'Приложение', 'Дата публикации', 'Вид локации']
        result, row = Viewer.change(self, self.photoslist, nameslist, 6)
        if result == 16384:
            self.addPhoto(None, row, 1)
        else:
            return

    def saveChangedPhoto(self):
        self.handlersql.updateQuery(self.database, "Photos", ["name", "model_id", "application_id", "location_id",
                                                              "publish_data", "id"],
                                    self.changedphoto[1:] + self.changedphoto[:1])

    def deletePhoto(self):
        nameslist = ['Имя модели', 'Фото', 'Приложение', 'Дата публикации', 'Вид локации']
        result, row = Viewer.change(self, self.photoslist, nameslist, 6, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Photos", "id", row[0])
            self.clear()
            self.setPhotoListView()
        else:
            return


class MySessions(Viewer):
    def __init__(self, database, handlersql, models, names):
        Viewer.__init__(self)
        self.database = database
        self.sessionslist = []
        self.newsession = []
        self.changedsession = []
        self.handlersql = handlersql
        self.models = models
        self.names = names
        self.makeWidget()

    def makeWidget(self):
        Viewer.makeWidget(self)
        if self.checkSessionsList():
            self.setSessionListView()
        else:
            label = QtWidgets.QLabel('Sessions List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setSessionsEditButton()

    def checkSessionsList(self):
        sessions_count = False
        querystr = "select id, model_id from Sessions"
        conn, query = self.handlersql.connectBase(self.database)
        query.exec(querystr)
        # print(query.isSelect())
        if query.isActive():
            query.first()
            while query.isValid():
                self.sessionslist.append((query.value('id'), query.value('model_id')))
                query.next()
        if len(self.sessionslist):
            sessions_count = True
            print("Valid")
            print("Start sessionslist:\n", self.sessionslist)
        else:
            print("not valid")
        conn.close()
        return sessions_count

    def setSessionListView(self):
        query = """select s.id, m.name, s.location_desc, s.equipment, s.session_date
        from Sessions s inner join Models m on s.model_id = m.id"""
        names = [(1, 'Модель'), (2, 'Локация'), (3, 'Оборудование'), (4, 'Дата')]
        columns = [(1, 250), (2, 450), (3, 250), (4, 90)]
        Viewer.setListView(self, query, names, self.database, self.handlersql, columns)
        self.setSessionsEditButton()

    def setSessionsEditButton(self):
        for i, f in (('AddSession', self.addSession), ('ChangeSession', self.changeSession),
                     ('DeleteSession', self.deleteSession)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.hbox.addWidget(btn)

    def addSession(self, a, new=('', '', '', '', ''), flag=None): # разобраться с id в ...лист.апенд
        def getName():
            value1 = cb_modelsname.currentIndex()
            value2 = lE_location.text()
            value3 = le_equipment.text()
            value4 = calendar.text()
            if value2 == '':
                QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Нет локации')
            else:
                if flag == 1:
                    txt = 'Изменена сессия от: '
                    self.changedsession = [new[0], self.models[value1][0], value2, value3, value4]
                    print("Changed session:\n", self.changedsession)
                    self.sessionslist.pop(int(new[0]) - 1)
                    self.sessionslist.insert(int(new[0]) - 1, (int(new[0]), self.models[value1][0]))
                    self.saveChangedSession()
                else:
                    txt = 'Добавлено сессия от: '
                    if self.sessionslist:
                        self.sessionslist.append((self.sessionslist[-1][0] + 1, self.models[value1][0]))  # adedd(id, model_id)
                    else:
                        self.sessionslist.append((1, self.models[value1][0]))
                    self.newsession = [self.models[value1][0], value2, value3, value4]
                    print("Newsession:\n", self.newsession)
                    self.saveSession()
                QtWidgets.QMessageBox.information(None, 'Инфо', txt + value4)
                self.clear()
                self.setSessionListView()
                tladd_photo.close()

        if not self.names:
            QtWidgets.QMessageBox.warning(None, 'Предупреждение', 'Отсутствуют модели для связи с фото.\n' +
                                          'Добавте моделей!')
            return
        tladd_photo = QtWidgets.QWidget(parent=window, flags=QtCore.Qt.Window)
        tladd_photo.setWindowTitle('Добавить')
        # tladd_photo.setWindowModality(QtCore.Qt.WindowModal)
        # tladd_photo.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        cb_modelsname = QtWidgets.QComboBox()
        cb_modelsname.addItems(self.names)
        lE_location = QtWidgets.QLineEdit()
        le_equipment = QtWidgets.QLineEdit()
        calendar = QtWidgets.QDateEdit()
        calendar.setCalendarPopup(True)
        calendar.setDisplayFormat("dd.MM.yyyy")
        calendar.setDate(datetime.date.today())
        btn_add = QtWidgets.QPushButton('Добавить')
        btn_close = QtWidgets.QPushButton('Закрыть')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_close)
        form = QtWidgets.QFormLayout()
        for i, n in (zip((lE_location, le_equipment), (new[2], new[3]))):
            i.setText(n)
        if flag == 1:
            tladd_photo.setWindowTitle('Изменить')
            cb_modelsname.setCurrentText(new[1])
            datelist = new[-1].split('.')
            calendar.setDate(QtCore.QDate(int(datelist[2]), int(datelist[1]), int(datelist[0])))
        form.addRow('Имя модели:', cb_modelsname)
        form.addRow('Описание локации:', lE_location)
        form.addRow('Оборудование:', le_equipment)
        form.addRow('Дата съёмки:', calendar)
        form.addRow(hbox)
        btn_add.clicked.connect(getName)
        btn_close.clicked.connect(tladd_photo.close)
        tladd_photo.setLayout(form)
        tladd_photo.show()

    def saveSession(self):
        self.handlersql.insertQuery(self.database, "Sessions", [":model_id", ":location_desc", ":equipment",
                                                                ":session_date"], self.newsession)

    def changeSession(self):
        nameslist = ['Имя модели', 'Описание локации', 'Оборудование', 'Дата съёмки']
        result, row = Viewer.change(self, self.sessionslist, nameslist, 5)
        if result == 16384:
            self.addSession(None, row, 1)
        else:
            return

    def saveChangedSession(self):
        self.handlersql.updateQuery(self.database, "Sessions", ["model_id", "location_desc", "equipment","session_date",
                                                            "id"], self.changedsession[1:] + self.changedsession[:1])

    def deleteSession(self):
        nameslist = ['Имя модели', 'Описание локации', 'Оборудование', 'Дата съёмки']
        result, row = Viewer.change(self, self.sessionslist, nameslist, 5, flag='delete')
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Sessions", "id", row[0])
            self.clear()
            self.setSessionListView()
        else:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Modelslist')
    window.resize(1100, 400)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
