class MenardsEntity(object):

    modelsku = None
    titleInfo = None
    price = None
    image = None

    def __init__(self, modelsku, image, titleInfo, price):

        self.modelsku = modelsku
        self.titleInfo = titleInfo
        self.price = price
        self.image = image
        self.checkFields()

    def checkFields(self):


        # Check model for NoneType, if NoneType then convert to String "None"
        if (self.modelsku == None):
            self.modelsku = str(self.modelsku)
        else:
            self.modelsku = self.modelsku.strip()

        # Check image src for NoneType
        if (self.image == None):
            self.image = str(self.image)

            # Check description for NoneType, if NoneType then convert to String "None"
        if (self.titleInfo == None):
            self.titleInfo = str(self.titleInfo)
        else:
            self.titleInfo = self.titleInfo.text.strip()

            # Check price for NoneType, if NoneType then convert to String "None"
        if (self.price == None):
            self.price = str(self.price)
        else:
            self.price = self.price.text.strip()

    def toString(self):
                print("Modelsku: ", self.modelsku, "\n", " Image: ", self.image, "\n", "titleInfo: ", self.titleInfo,
                      "\n", "Price: ", self.price, "\n")
