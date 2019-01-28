class MenardsEntity(object):

    modelsku = None
    titleInfo = None

    def __init__(self,modelsku, titleInfo):

        self.modelsku = modelsku
        self.titleInfo = titleInfo
        self.checkFields()

    def checkFields(self):
        # Check model for NoneType, if NoneType then convert to String "None"
        if (self.modelsku == None):
            self.modelsku = str(self.modelsku)
        else:
            self.modelsku = self.modelsku.text.strip()

            # Check description for NoneType, if NoneType then convert to String "None"
        if (self.titleInfo == None):
            self.titleInfo = str(self.titleInfo)
        else:
            self.titleInfo = self.titleInfo.text.strip()

    def toString(self):
                print("Modelsku: ", self.modelsku, "\n", "titleInfo: ", self.titleInfo, "\n")
