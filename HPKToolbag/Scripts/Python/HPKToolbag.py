from maya import cmds
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

# To get the maya main window pointer and pass it to our tool window
# to stay alwayes on top of the maya main program and don't hide behind it
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)

#----------------------------------------------------------------------------------------------
class HpkToolBag_Main(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(HpkToolBag_Main,self).__init__(parent)

        #Set Window Properties
        self.setWindowTitle ("HPK Toolbag")
        self.setMinimumWidth(300)
        #self.setMinimumHeight(300)
        
        #Remove the Question mark next to the Exit button on the window
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        #Create all the widgets and layouts
        self.inits()
        self.create_widgets()
        self.create_TransferSkin_Widgets()
        self.create_ConnectOneToManyAttr_Widgets()
        self.create_connections()
    
    def inits(self):
        self.SkinNewGeo = ''
        self.SkinSourceGeo = ''

#||||||||||||||||||||||||||||||||||||||||--- Functionality ---|||||||||||||||||||||||||||||||||||||||||||||||||||
    def transferskin(self,oldSkinObj,newSkinObj,*args):
        
        skincluster = mel.eval('findRelatedSkinCluster '+oldSkinObj)
        
        #print (skincluster)
        
        infList = cmds.skinCluster(skincluster,query=True,inf=True)
        
        #print (infList)
        
        cmds.skinCluster (infList,newSkinObj,tsb=1)
        
        cmds.select (cl=1)
        cmds.select (oldSkinObj)
        cmds.select (newSkinObj,add=1)
            
        cmds.copySkinWeights(noMirror=1,surfaceAssociation='closestPoint',influenceAssociation='oneToOne')
    
    def getSelectedAttrFromChannelBox(self,Type='longName'):
        selectedAttrs = cmds.channelBox("mainChannelBox", q=1, sma=1)
        LongAttr = ''
        ShortAttr = ''
        obj = cmds.ls(sl=1)
        if (selectedAttrs!=None):
            for each in selectedAttrs:
                LongAttr = obj[0] +'.'+ cmds.listAttr("{0}.{1}".format(obj[0], each))[0]
                ShortAttr = '.'+ cmds.listAttr("{0}.{1}".format(obj[0], each))[0]
                
        if Type == 'longName':
            return (LongAttr)
        elif Type == 'shortName':
            return (ShortAttr)

    def ConnectOneToMany(self,SourceAttribute,ManyAttributes):
        ObjAttr = SourceAttribute
        selection = cmds.ls(sl=1)
        for Obj in selection:
            cmds.connectAttr (ObjAttr,Obj+ManyAttributes)

#||||||||||||||||||||||||||||||||||||||||--- Events ---|||||||||||||||||||||||||||||||||||||||||||||||||||
    #//SkinTransfer Events
    def transferSkin_Clicked(self):
        if self.SkinSourceGeo != '' and self.SkinNewGeo != '':
            self.transferskin(self.SkinSourceGeo,self.SkinNewGeo)
            print("You Did it")
    def getSourcegeo_Clicked(self):
        
        obj = cmds.ls(sl=1)
        objName = str(obj[0])
        if len(obj)==1 and objName!=self.SkinNewGeo:
            self.SkinSourceGeo = objName
            self.getSourcegeo_LE.setText(self.SkinSourceGeo)
            print (self.SkinSourceGeo)
        else:
            "Please Select One Object as a Source Skinned Object"
    def getNewgeo_Clicked(self):
        obj = cmds.ls(sl=1)
        objName = str(obj[0])
        if len(obj)==1 and objName!=self.SkinSourceGeo:
            self.SkinNewGeo = objName
            self.getNewgeo_LE.setText(self.SkinNewGeo)
            print (self.SkinNewGeo)
        else:
            "Please Select One Object as a Destination Object"

    #// Connect One To Many Events
    def getSourceAttr_Clicked(self):
        SelectedAttribute = self.getSelectedAttrFromChannelBox(Type='longName')
        if SelectedAttribute != '' and SelectedAttribute != None:
            self.getSourceAttr_LE.setText(SelectedAttribute)

    def getDestAttr_Clicked(self):        
        SelectedAttribute = self.getSelectedAttrFromChannelBox(Type='shortName')
        if SelectedAttribute != '' and SelectedAttribute != None:
            self.getDestAttr_LE.setText(SelectedAttribute)

    def ConnectOneToMany_clicked(self):
        SourceAttribute = self.getSourceAttr_LE.text()
        DestAttribute = self.getDestAttr_LE.text()
        if SourceAttribute!='' and SourceAttribute!=None and DestAttribute!='' and DestAttribute != None: 
            self.ConnectOneToMany(SourceAttribute,DestAttribute)
        else:
            print("Please Select an Attribute")

#||||||||||||||||||||||||||||||||||||||||||--- UI ---|||||||||||||||||||||||||||||||||||||||||||||||||
    
    def create_widgets(self):
    #-------------- Main TAB Widget
        self.main_tabWid = QtWidgets.QTabWidget(self)
        self.main_tabWid.setGeometry(QtCore.QRect(10, 10, 400, 500))
        self.main_tabWid.setObjectName("main_tabWid")

        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")        
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        
        self.main_tabWid.addTab(self.tab1, "Page 1")
        self.main_tabWid.addTab(self.tab2, "Page 2")
        
    def create_TransferSkin_Widgets(self):
            #------------------- Transfer Skin Widgets 
        self.skinTransfer_GBox = QtWidgets.QGroupBox(self.tab1,"Skin Transfer")
        self.skinTransfer_GBox.setGeometry(QtCore.QRect(2, 5, 390, 140))
        
        self.skinTransfer_GBox.setObjectName("skinTransfer_GBox")
        self.skinTransfer_GBox.setTitle("Skin Transfer Tool")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.skinTransfer_GBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        #// [ Source Geo ] Horizental Layout and Widgets
        self.getSourcegeo_Hlayout = QtWidgets.QHBoxLayout()
        self.getSourcegeo_Hlayout.setObjectName("getSourcegeo_Hlayout")
        
        self.getSourcegeo_LE = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.getSourcegeo_LE.setObjectName("getSourcegeo_LE")

        self.getSourcegeo_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.getSourcegeo_PB.setObjectName("getSourcegeo_PB")
        self.getSourcegeo_PB.setText("<- Source Obj")
        
            #-Add Widgets to Source Geo Horizental Layout
        self.getSourcegeo_Hlayout.addWidget(self.getSourcegeo_LE)
        self.getSourcegeo_Hlayout.addWidget(self.getSourcegeo_PB)

        #// [ New Geo ] Horizental Layout and Widgets
        self.getNewgeo_Hlayout = QtWidgets.QHBoxLayout()
        self.getNewgeo_Hlayout.setObjectName("getNewgeo_Hlayout")
        
        self.getNewgeo_LE = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.getNewgeo_LE.setObjectName("getNewgeo_LE")

        self.getNewgeo_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.getNewgeo_PB.setObjectName("getNewgeo_PB")
        self.getNewgeo_PB.setText("<- New Obj")
        
            #-Add Widgets to New Geo Horizental Layout ---
        self.getNewgeo_Hlayout.addWidget(self.getNewgeo_LE)
        self.getNewgeo_Hlayout.addWidget(self.getNewgeo_PB)        

        #// Transfer Skin Push Button ----
        self.skinTransfer_Vlayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.skinTransfer_Vlayout.setContentsMargins(0, 5, 0, 5)
        self.skinTransfer_Vlayout.setObjectName("skinTransfer_Vlayout")

        self.transferSkin_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.transferSkin_PB.setObjectName("transferSkin_PB")
        self.transferSkin_PB.setText("Transfer Skin")

        #// Transfer Skin main Vertical Layout ---
        self.skinTransfer_Vlayout.addLayout(self.getSourcegeo_Hlayout)
        self.skinTransfer_Vlayout.addLayout(self.getNewgeo_Hlayout)
        self.skinTransfer_Vlayout.addWidget(self.transferSkin_PB)
        
    def create_ConnectOneToManyAttr_Widgets(self):
            #------------------- Transfer Skin Widgets 
        self.ConnOneToMany_GBox = QtWidgets.QGroupBox(self.tab1,"Connect One Attr To Many Objects Attribute")
        self.ConnOneToMany_GBox.setGeometry(QtCore.QRect(2, 145, 390, 140))
        
        self.ConnOneToMany_GBox.setObjectName("ConnectOneToMany_GBox")
        self.ConnOneToMany_GBox.setTitle("Connect One Attribute To Many")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.ConnOneToMany_GBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        #// [ Source Attribute ] Horizental Layout and Widgets
        self.getSourceAttr_Hlayout = QtWidgets.QHBoxLayout()
        self.getSourceAttr_Hlayout.setObjectName("getSourceAttribute_Hlayout")
        
        self.getSourceAttr_LE = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.getSourceAttr_LE.setObjectName("getSourceAttribute_LE")

        self.getSourceAttr_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.getSourceAttr_PB.setObjectName("getSourceAttr_PB")
        self.getSourceAttr_PB.setText("<- Source Attribute")
        
            #-Add Widgets to Source Attributes Horizental Layout
        self.getSourceAttr_Hlayout.addWidget(self.getSourceAttr_LE)
        self.getSourceAttr_Hlayout.addWidget(self.getSourceAttr_PB)

        #// [ New Geo ] Horizental Layout and Widgets
        self.getDestAttr_Hlayout = QtWidgets.QHBoxLayout()
        self.getDestAttr_Hlayout.setObjectName("getDestAttr_Hlayout")
        
        self.getDestAttr_LE = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.getDestAttr_LE.setObjectName("getDestAttr_LE")

        self.getDestAttr_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.getDestAttr_PB.setObjectName("getDestAttr_PB")
        self.getDestAttr_PB.setText("<- Destination Attribute")
        
            #-Add Widgets to New Geo Horizental Layout ---
        self.getDestAttr_Hlayout.addWidget(self.getDestAttr_LE)
        self.getDestAttr_Hlayout.addWidget(self.getDestAttr_PB)        

        #// Transfer Skin Push Button ----
        self.ConnOneToMany_Vlayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.ConnOneToMany_Vlayout.setContentsMargins(0, 5, 0, 5)
        self.ConnOneToMany_Vlayout.setObjectName("ConnOneToMany_Vlayout")

        self.ConnOneToMany_PB = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ConnOneToMany_PB.setObjectName("ConnOneToMany_PB")
        self.ConnOneToMany_PB.setText("Connect Source to Destination")

        #// Transfer Skin main Vertical Layout ---
        self.ConnOneToMany_Vlayout.addLayout(self.getSourceAttr_Hlayout)
        self.ConnOneToMany_Vlayout.addLayout(self.getDestAttr_Hlayout)
        self.ConnOneToMany_Vlayout.addWidget(self.ConnOneToMany_PB)

    def create_connections(self):
        #//Skin Transfer Connections
        self.getSourcegeo_PB.clicked.connect(self.getSourcegeo_Clicked)
        self.getNewgeo_PB.clicked.connect(self.getNewgeo_Clicked)
        self.transferSkin_PB.clicked.connect(self.transferSkin_Clicked)

        #Connect One To Many Connections
        self.getSourceAttr_PB.clicked.connect(self.getSourceAttr_Clicked)
        self.getDestAttr_PB.clicked.connect(self.getDestAttr_Clicked)
        self.ConnOneToMany_PB.clicked.connect(self.ConnectOneToMany_clicked)
        

if __name__ == "__main__":
    try:
        HpkToolBag_Main.close() # pylint: disable:E0601
        HpkToolBag_Main.deleteLater()
    except:
        pass

    HpkToolBag_Main = HpkToolBag_Main()
    HpkToolBag_Main.show()




