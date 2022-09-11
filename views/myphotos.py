from .viewer import Viewer
from PyQt5 import QtWidgets, QtCore
import datetime


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

    def checkPhotosList(self):
        photos_count = False
        querystr = "select id, name, model_id from Photos"
        conn, query = self.handlersql.connectBase(self.database)  # connectBase(self.database)
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
        names = [(1, 'Модель'), (2, 'Фото'), (3, 'Приложение'), (4, 'Дата публикации'), (5, 'Тип локации')]
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
                        self.photoslist.append(
                            (self.photoslist[-1][0] + 1, value2, self.models[value1][0]))  # adedd(id, name, model_id)
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
        tladd_photo = QtWidgets.QWidget(parent=None, flags=QtCore.Qt.Window)
        tladd_photo.setWindowTitle('Добавить')
        # tladd_photo.setWindowModality(QtCore.Qt.WindowModal)
        # tladd_photo.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        cb_modelsname = QtWidgets.QComboBox()
        cb_modelsname.addItems(self.names)
        lE_photo = QtWidgets.QLineEdit()
        cb_app = QtWidgets.QComboBox()
        cb_app.addItems([i[1] for i in self.app_list])  # [i[1] for i in self.app_list]
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
