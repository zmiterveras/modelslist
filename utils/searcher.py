class Searcher:
    def __init__(self, instance):
        self.instance = instance
        self.classname = instance.__class__.__name__

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




