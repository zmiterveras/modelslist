#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# inheriting branch

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
import sys, sqlite3, random, os, time
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
        action = myNotes.addAction('Add Model')
        action = myNotes.addAction('Add Application')
        action = myNotes.addAction('Add Location')
        action = myNotes.addAction('Add Photo')
        #action = myMenu.addAction('Test',  self.test)
        myEdit = menuBar.addMenu('&Edit notes')
        action = myEdit.addAction('Delete model')
        action = myEdit.addAction('Delete photo')
        action = myEdit.addAction('Change photo')
        action = myEdit.addAction('Change model')
        myAbout = menuBar.addMenu('О...')
        action = myAbout.addAction('О программе') #, self.aboutProgramm)
        action = myAbout.addAction('Обо мне') #, self.aboutMe)
        self.statusBar = self.statusBar()


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, root_path, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.root_path = root_path
        self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        self.handlersql = HandleSql()
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
            query.exec("insert into Application (id, name) values (null, 'any')")
            query.clear()
        if 'Location' not in conn.tables():
            querystr3 = """create table Location (id integer primary key autoincrement,
            name text)"""
            query.exec(querystr3)
            query.clear()
            query.exec("insert into Location (id, name) values (null, 'any')")
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
        self.vbox.addWidget(self.viewWidget)
        self.main_box.addLayout(self.vbox)
        self.main_box.addLayout(self.bottom_box)
        self.setLayout(self.main_box)

    def setControlButtons(self):
        for i, f in (('Models', self.viewModels), ('Photos', self.viewPhotos), ('Sessions', self.viewSessions),
                     ('Close', self.test)):
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(f)
            self.bottom_box.addWidget(btn)

    def clearVBox(self):
        for i in reversed(range(self.vbox.count())):
            wt = self.vbox.itemAt(i).widget()
            wt.setParent(None)
            wt.deleteLater()

    def test(self):
        pass

    def viewModels(self):
        pass

    def viewPhotos(self):
        pass

    def viewSessions(self):
        pass


class Viewer(QtWidgets.QWidget):
    def __init__(self, database):
        QtWidgets.QWidget.__init__(self,parent=None)
        self.database = database
        # self.handlersql = handlersql

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

    def setListView(self, query, names, handlersql):
        self.clear()
        handlersql.connectBase(self.database)
        # query = """select m.id, m.name, m.origin, m.ed_work, c.phone, c.email, c.ref_s
        # from Models m inner join Contacts c on m.id = c.model_id"""
        self.stm = QtSql.QSqlQueryModel(parent=None)
        self.stm.setQuery(query)
        self.stm.sort(1, QtCore.Qt.AscendingOrder)
        # names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа'), (4, 'Phone'), (5, 'Email'), (6, 'References')]
        for (i, n) in names:
            self.stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        self.tv = QtWidgets.QTableView()
        self.tv.setModel(self.stm)
        self.tv.hideColumn(0)
        self.vbox.addWidget(self.tv)
        # self.setModelsEditButton()


class MyView(Viewer): #(QtWidgets.QWidget):
    def __init__(self, database, handlersql): #, parent=None):
        Viewer.__init__(self, database)
        # self.root_path = root_path
        # self.database = os.path.join(self.root_path, 'bases/models.sqlite')
        # self.database = database
        self.modelslist = []
        self.modelnames = []
        self.newmodel = []
        self.changedmodel = []
        # self.handlersql = HandleSql()
        self.handlersql = handlersql
        self.query_models = """select m.id, m.name, m.origin, m.ed_work, c.phone, c.email, c.ref_s 
        # from Models m inner join Contacts c on m.id = c.model_id"""
        self.col_names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа'), (4, 'Phone'), (5, 'Email'),
                          (6, 'References')]
        # if not os.path.exists("bases/models.sqlite"):
        #     print("Not database")
        #     self.createDataBase()
        # else:
        #     print("There is database")
        self.makeWidget()

    # def createDataBase(self):
    #     conn, query = self.handlersql.connectBase(self.database)
    #     if 'Models' not in conn.tables():
    #         querystr1 = '''create table Models (id integer primary key autoincrement,
    #         name text, origin text, ed_work text)'''
    #         query.exec(querystr1)
    #         query.clear()
    #     if 'Application' not in conn.tables():
    #         querystr2 = """create table Application (id integer primary key autoincrement,
    #         name text)"""
    #         query.exec(querystr2)
    #         query.clear()
    #         query.exec("insert into Application (id, name) values (null, 'any')")
    #         query.clear()
    #     if 'Location' not in conn.tables():
    #         querystr3 = """create table Location (id integer primary key autoincrement,
    #         name text)"""
    #         query.exec(querystr3)
    #         query.clear()
    #         query.exec("insert into Location (id, name) values (null, 'any')")
    #         query.clear()
    #     if 'Photos' not in conn.tables():
    #         querystr4 = """create table Photos (id integer primary key autoincrement,
    #         name text, model_id integer, application_id integer, location_id integer, publish_data text)"""
    #         query.exec(querystr4)
    #         query.clear()
    #     if 'Sessions' not in conn.tables():
    #         querystr5 = """create table Sessions (id integer primary key autoincrement,
    #         model_id integer, location_desc text, equipment text, session_date text)"""
    #         query.exec(querystr5)
    #         query.clear()
    #     if 'Contacts' not in conn.tables():
    #         querystr6 = '''create table Contacts (id integer primary key autoincrement,
    #         model_id integer, phone text, email text, ref_s text)'''
    #         query.exec(querystr6)
    #         query.clear()
    #     conn.close()

    def makeWidget(self):
        # # self.main_box = QtWidgets.QVBoxLayout()
        # self.top_box = QtWidgets.QVBoxLayout()
        # # self.bottom_box = QtWidgets.QHBoxLayout()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.hbox = QtWidgets.QHBoxLayout()
        # self.top_box.addLayout(self.vbox)
        # self.top_box.addLayout(self.hbox)
        # # self.main_box.addLayout(self.top_box)
        # # self.main_box.addLayout(self.bottom_box)
        # # self.setLayout(self.main_box)
        # self.setLayout(self.top_box)
        Viewer.makeWidget(self)
        if self.checkModelsList():
            self.setModelListView()

        else:
            label = QtWidgets.QLabel('Models List is empty')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(label)
            self.setModelsEditButton()

    # def clear(self):
    #     for i in reversed(range(self.vbox.count())):
    #         wt = self.vbox.itemAt(i).widget()
    #         wt.setParent(None)
    #         wt.deleteLater()
    #     for i in reversed(range(self.hbox.count())):
    #         wb = self.hbox.itemAt(i).widget()
    #         wb.setParent(None)
    #         wb.deleteLater()

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
        else:
            print("not valid")
        conn.close()
        return models_count

    def setModelListView(self):
        # self.clear()
        # self.handlersql.connectBase(self.database)
        query = """select m.id, m.name, m.origin, m.ed_work, c.phone, c.email, c.ref_s 
        from Models m inner join Contacts c on m.id = c.model_id"""
        # self.stm = QtSql.QSqlQueryModel(parent=None)
        # self.stm.setQuery(query)
        # self.stm.sort(1, QtCore.Qt.AscendingOrder)
        names = [(1, 'Имя'), (2, 'Откуда'), (3, 'Образование/Работа'), (4, 'Phone'), (5, 'Email'), (6, 'References')]
        # for (i, n) in names:
        #     self.stm.setHeaderData(i, QtCore.Qt.Horizontal, n)
        # self.tv = QtWidgets.QTableView()
        # self.tv.setModel(self.stm)
        # self.tv.hideColumn(0)
        # self.vbox.addWidget(self.tv)
        Viewer.setListView(self, query, names, self.handlersql)
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
                    self.modelslist.pop(int(new[0])-1)
                    self.modelslist.insert(int(new[0])-1, (int(new[0]), value1))
                    self.saveChangedModel()
                else:
                    txt = 'Добавлена модель: '
                    if self.modelslist:
                        self.modelslist.append((self.modelslist[-1][0] + 1, value1))
                    else:
                        self.modelslist.append((1, value1))
                    self.modelnames.append(value1)
                    self.newmodel = [value1, value2, value3, value4, value5, value6]
                    self.saveModel()
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

    def getRow(self, col):
        row_number = self.tv.currentIndex().row()
        row = []
        for i in range(col):
            index = self.stm.index(row_number, i)
            row.append(self.stm.data(index))
        print('new', row)
        return row

    def changeModel(self):
        row = self.getRow(7)
        result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                'Вы действительно хотите изменить запись:\n' +
                                                'Имя: ' + row[1] + '\n' +
                                                'Откуда: ' + row[2] + '\n' +
                                                'Учеба/Работа: ' + row[3] + '\n' +
                                                'Телефон: ' + row[4] + '\n' +
                                                'Email: ' + row[5] + '\n' +
                                                'Ссылки: ' + row[6] + '\n',
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
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
        print("Change: ", self.changedmodel)
        self.handlersql.updateQuery(self.database, "Models", ["name", "origin", "ed_work", "id"],
                                    self.changedmodel[1:4] + self.changedmodel[:1])
        self.handlersql.updateQuery(self.database, "Contacts", ["phone", "email", "ref_s", "model_id"],
                                    self.changedmodel[4:] + self.changedmodel[:1])

    def deleteModel(self):
        row = self.getRow(7)
        result = QtWidgets.QMessageBox.question(None, 'Предупреждение',
                                                'Вы действительно хотите удалить запись:\n' +
                                                'Имя: ' + row[1] + '\n' +
                                                'Откуда: ' + row[2] + '\n' +
                                                'Учеба/Работа: ' + row[3] + '\n' +
                                                'Телефон: ' + row[4] + '\n' +
                                                'Email: ' + row[5] + '\n' +
                                                'Ссылки: ' + row[6] + '\n',
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.No)
        if result == 16384:
            self.handlersql.deleteQuery(self.database, "Contacts", "model_id", row[0])
            self.handlersql.deleteQuery(self.database, "Models", "id", row[0])
            self.clear()
            self.setModelListView()
        else:
            return

    def test(self):
        print('test')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Modelslist')
    window.resize(750, 400)
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() // 2) - window.width()
    window.move(x, 250)
    window.show()
    sys.exit(app.exec_())
