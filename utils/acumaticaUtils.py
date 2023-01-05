#%% Python
# Copyright TCB

# Uses an acumatica stock item as a shop item in an e-commerce website
from lib2to3.pytree import convert
from tokenize import String
from unicodedata import decimal
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)
import mysql.connector
from mysql.connector import Error
import os
import requests
import json
import shutil
import re
import uuid

class prodDict():
    def __init__(self):
        self.name               = str()
        self.alt_name           = str()
        self.price              = 0.00
        self.price_code         = str()
        self.uom                = 'unit'
        self.image_url          = str()
        self.image_url_desc     = str()
        self.title_description  = str()
        self.description        = str()
        self.description2       = str()
        
    def __iter__(self):
        # For converting to dict:
        # https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
        iters = dict((x,y) for x,y in self.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)
        for x,y in iters.items():
            yield x,y

class AcumaticaDapper():
    def __init__(self) -> None:
        self.COMPANY = 'PhoneRepairShop1'
        self.DBNAME = 'phonerepairshoptake2'
        self.BASEENDPT = os.environ["ACUMATICAENDPT"]
        self.SERVICE_URL = f'{self.BASEENDPT}/{self.COMPANY}/entity/Default/18.200.001/'
        self.GETFILE = f"{self.BASEENDPT}/Frames/GetFile.ashx?fileID="
        try:
            self.DBENDPOINT = os.environ["DBENDPOINT"]
            self.DBUSER= os.environ["DBUSER"]
            self.DBPASS = os.environ["DBPASS"]

            self.connection = mysql.connector.connect(host = self.DBENDPOINT,
                                                database = self.DBNAME,
                                                user = self.DBUSER ,
                                                password = self.DBPASS,
                                                auth_plugin='mysql_native_password')
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
        except Error as e:
            print("Error while connecting to MySQL", e)
    
    def getImageFromDatabase(self, fileName, fileId='b33c365a-0651-4889-af52-6d08249af45d'):
        self.connection.reconnect()
        mycursor = self.connection.cursor(buffered=True)
        mycursor.execute(f"SELECT * FROM uploadfilerevision where FileID = '{fileId}'")
        myresult = mycursor.fetchone()
        base = './static'
        filePath = f'/product_images/{fileName}.png'
        #Save Image
        with open(base + filePath, "wb") as fh:
            fh.write(myresult[3])
        mycursor.close()
        self.connection.close()
        return filePath

    def get(self, endpt= "CSAnswers"):
        r=requests.get(self.SERVICE_URL+endpt, auth=('admin', os.environ["ACUMATICAPWD"]), verify=False)
        assert (r.status_code == 200)
        return r.json()['value']
    
    def getInvFiles(self):
        return self.get(endpt="File?$filter=PrimaryScreenID eq 'IN2025PL'")
    
    def getInvFilesDetailed(self):
        return self.get(endpt="File?$filter=PrimaryScreenID eq 'IN202500'")
    
    def createSQLStockItems(self, string):
        if len(string) < 8:
            print("skipping product creation, identified entry is too short")
            return
        self.connection.reconnect()
        mycursor = self.connection.cursor(buffered=True)

        uid = uuid.uuid1()
        noteuuid = uuid.uuid1()

        inventoryCD = string[0:10]
        description = string

        #mycursor.execute(f"insert into inventoryitem(CompanyID, InventoryCD, CreatedByID, CreatedByScreenID, CreatedDateTime,LastModifiedByID, LastModifiedByScreenID, LastModifiedDateTime, ItemType, ItemStatus, BaseUnit, SalesUnit, PurchaseUnit, DecimalBaseUnit, NoteId, Descr) values(2, '{string}', uuid(), 'IN202500', NOW(), uuid(), 'IN202500', NOW(), 'F', 'AC', 'PIECE', 'PIECE','PIECE', 1, uuid(), 'Sql')")
        mycursor.execute(f"""INSERT InventoryItem(`InventoryItem`.`CompanyID`, `InventoryItem`.`InventoryCD`, `InventoryItem`.`StkItem`, `InventoryItem`.`Descr`, `InventoryItem`.`ItemClassID`, `InventoryItem`.`ItemStatus`, `InventoryItem`.`ItemType`, `InventoryItem`.`ValMethod`, `InventoryItem`.`TaxCategoryID`, `InventoryItem`.`TaxCalcMode`, `InventoryItem`.`WeightItem`, `InventoryItem`.`BaseUnit`, `InventoryItem`.`SalesUnit`, `InventoryItem`.`PurchaseUnit`, `InventoryItem`.`DecimalBaseUnit`, `InventoryItem`.`DecimalSalesUnit`, `InventoryItem`.`DecimalPurchaseUnit`, `InventoryItem`.`Commisionable`, `InventoryItem`.`ReasonCodeSubID`, `InventoryItem`.`SalesAcctID`, `InventoryItem`.`SalesSubID`, `InventoryItem`.`InvtAcctID`, `InventoryItem`.`InvtSubID`, `InventoryItem`.`COGSAcctID`, `InventoryItem`.`COGSSubID`, `InventoryItem`.`StdCstRevAcctID`, `InventoryItem`.`StdCstRevSubID`, `InventoryItem`.`StdCstVarAcctID`, `InventoryItem`.`StdCstVarSubID`, `InventoryItem`.`PPVAcctID`, `InventoryItem`.`PPVSubID`, `InventoryItem`.`POAccrualAcctID`, `InventoryItem`.`POAccrualSubID`, `InventoryItem`.`LCVarianceAcctID`, `InventoryItem`.`LCVarianceSubID`, `InventoryItem`.`DeferralAcctID`, `InventoryItem`.`DeferralSubID`, `InventoryItem`.`LastSiteID`, `InventoryItem`.`LastStdCost`, `InventoryItem`.`PendingStdCost`, `InventoryItem`.`PendingStdCostDate`, `InventoryItem`.`StdCost`, `InventoryItem`.`StdCostDate`, `InventoryItem`.`BasePrice`, `InventoryItem`.`BaseWeight`, `InventoryItem`.`BaseVolume`, `InventoryItem`.`BaseItemWeight`, `InventoryItem`.`BaseItemVolume`, `InventoryItem`.`WeightUOM`, `InventoryItem`.`VolumeUOM`, `InventoryItem`.`PackSeparately`, `InventoryItem`.`PackageOption`, `InventoryItem`.`PreferredVendorID`, `InventoryItem`.`PreferredVendorLocationID`, `InventoryItem`.`DefaultSubItemID`, `InventoryItem`.`DefaultSubItemOnEntry`, `InventoryItem`.`DfltSiteID`, `InventoryItem`.`DfltShipLocationID`, `InventoryItem`.`DfltReceiptLocationID`, `InventoryItem`.`ProductWorkgroupID`, `InventoryItem`.`ProductManagerID`, `InventoryItem`.`PriceWorkgroupID`, `InventoryItem`.`PriceManagerID`, `InventoryItem`.`LotSerClassID`, `InventoryItem`.`PostClassID`, `InventoryItem`.`DeferredCode`, `InventoryItem`.`DefaultTerm`, `InventoryItem`.`DefaultTermUOM`, `InventoryItem`.`PriceClassID`, `InventoryItem`.`IsSplitted`, `InventoryItem`.`UseParentSubID`, `InventoryItem`.`KitItem`, `InventoryItem`.`MinGrossProfitPct`, `InventoryItem`.`NonStockReceipt`, `InventoryItem`.`NonStockReceiptAsService`, `InventoryItem`.`NonStockShip`, `InventoryItem`.`AccrueCost`, `InventoryItem`.`CostBasis`, `InventoryItem`.`PercentOfSalesPrice`, `InventoryItem`.`CompletePOLine`, `InventoryItem`.`ABCCodeID`, `InventoryItem`.`ABCCodeIsFixed`, `InventoryItem`.`MovementClassID`, `InventoryItem`.`MovementClassIsFixed`, `InventoryItem`.`MarkupPct`, `InventoryItem`.`RecPrice`, `InventoryItem`.`ImageUrl`, `InventoryItem`.`HSTariffCode`, `InventoryItem`.`UndershipThreshold`, `InventoryItem`.`OvershipThreshold`, `InventoryItem`.`CountryOfOrigin`, `InventoryItem`.`NoteID`, `InventoryItem`.`CreatedByID`, `InventoryItem`.`CreatedByScreenID`, `InventoryItem`.`CreatedDateTime`, `InventoryItem`.`LastModifiedByID`, `InventoryItem`.`LastModifiedByScreenID`, `InventoryItem`.`LastModifiedDateTime`, `InventoryItem`.`GroupMask`, `InventoryItem`.`CycleID`, `InventoryItem`.`Body`, `InventoryItem`.`IsTemplate`, `InventoryItem`.`TemplateItemID`, `InventoryItem`.`DefaultRowMatrixAttributeID`, `InventoryItem`.`DefaultColumnMatrixAttributeID`, `InventoryItem`.`GenerationRuleCntr`, `InventoryItem`.`AttributeDescriptionGroupID`, `InventoryItem`.`ColumnAttributeValue`, `InventoryItem`.`RowAttributeValue`, `InventoryItem`.`Visibility`, `InventoryItem`.`Availability`, `InventoryItem`.`NotAvailMode`, `InventoryItem`.`ExportToExternal`) 
        VALUES(2, '{inventoryCD}', true, '{description}', 1, 'AC', 'F', 'A', 'EXEMPT', 'T', false, 'PIECE', 'PIECE', 'PIECE', true, true, true, false, NULL, 2274, 650, 2261, 650, 2267, 650, NULL, NULL, NULL, NULL, NULL, NULL, 2264, 650, NULL, NULL, NULL, NULL, NULL, 0.0, 0.0, NULL, 0.0, NULL, 0.0, 0.0, 0.0, 0.0, 0.0, NULL, NULL, false, 'N', NULL, NULL, 15, false, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'DEFAULT', 'STOCKITEM', NULL, 0, 'Y', NULL, false, false, false, 0.000000, true, false, true, false, 'S', 0.0, 'Q', NULL, false, NULL, false, 0.000000, 0.0, NULL, NULL, 100.000000, 100.000000, NULL, '{noteuuid}', '{uid}', 'IN202500', UTC_TIMESTAMP(6), '{uid}', 'IN202500', UTC_TIMESTAMP(6), NULL, NULL, NULL, false, NULL, NULL, NULL, 0, NULL, NULL, NULL, 'X', 'X', 'X', true)""")
        self.connection.commit()
        mycursor.execute("SELECT LAST_INSERT_ID() /* IN.20.25.00 */;")
        self.connection.commit()
        lastInsertedId = mycursor.fetchone()[0]
        print(lastInsertedId)
        mycursor.execute(f"""INSERT INUnit(`INUnit`.`CompanyID`, `INUnit`.`UnitType`, `INUnit`.`ItemClassID`, `INUnit`.`InventoryID`, `INUnit`.`ToUnit`, `INUnit`.`FromUnit`, `INUnit`.`UnitMultDiv`, `INUnit`.`UnitRate`, `INUnit`.`PriceAdjustmentMultiplier`, `INUnit`.`CreatedByID`, `INUnit`.`CreatedByScreenID`, `INUnit`.`CreatedDateTime`, `INUnit`.`LastModifiedByID`, `INUnit`.`LastModifiedByScreenID`, `INUnit`.`LastModifiedDateTime`) VALUES(2, 1, 0, {int(lastInsertedId)}, 'PIECE', 'PIECE', 'M', 1.000000, 1, '{uid}', 'IN202500', UTC_TIMESTAMP(6), '{uid}', 'IN202500', UTC_TIMESTAMP(6)) /* IN.20.25.00 */""")
        mycursor.execute(f"""UPDATE INUnit SET CompanyMask = CASE WHEN CompanyID = 2 THEN binaryMaskAdd(`CompanyMask`, 2, 2) ELSE binaryMaskSub(`CompanyMask`, 2, 2) END WHERE (`INUnit`.`UnitType` = 1 AND `INUnit`.`ItemClassID` = 0 AND `INUnit`.`InventoryID` = {int(lastInsertedId)} AND `INUnit`.`ToUnit` = 'PIECE' AND `INUnit`.`FromUnit` = 'PIECE') AND CompanyID IN (1, 2) /* IN.20.25.00 */""")
        self.connection.commit()

        return mycursor.rowcount

    def getSQLstockItem(self):
        self.connection.reconnect()
        mycursor = self.connection.cursor()
        mycursor.execute(f"SELECT * FROM inventoryitem")
        myresult = mycursor.fetchone()
        return myresult

    def createStockItem(self, headers, cookies, endpt="StockItem"):
        item = {
            'InventoryCD':'ApiTestItem',
            'ItemClassID':1,
            'TaxCategoryID':'EXEMPT',
            'PostClassID':'STOCKITEM',
            'BaseUnit':'PIECE',
            'SalesUnit':'PIECE',
            'PurchaseUnit':'PIECE',
        }
        print(self.SERVICE_URL+endpt)
        r=requests.put(self.SERVICE_URL+endpt, auth=('admin', os.environ["ACUMATICAPWD"]), verify=False,  data=item, headers=headers, cookies=cookies)
        pp.pprint(r)
        pp.pprint(r.content)
        return r

    def auth(self):
        endpoint = f"http://localhost/{self.COMPANY}/entity/auth/login"
        creds = {
            'name':"admin",
            "password":os.environ["ACUMATICAPWD"],
            "company":"MyStore",
            "branch":"MYSTORE",
        }
        r=requests.post(endpoint, data = creds)
        # assert (r.status_code == 204)
        pp.pprint(r.content)
        return r

    def logout(self, headers, cookies):
        endpoint = f"http://localhost/{self.COMPANY}/entity/auth/logout"
        r=requests.post(endpoint, headers=headers, cookies=cookies)
        # assert (r.status_code == 204)
        return r

if __name__ == "__main__":
    # pp.pprint(AcumaticaOdata().getItemWithAttributes())
    authReq = AcumaticaDapper().auth()
    headerauth = authReq.headers
    cookies = authReq.cookies

    print(headerauth)
    try:
        AcumaticaDapper().createStockItem(headerauth, cookies)
    except Exception as e:
        pp.pprint(e)
    finally:
        AcumaticaDapper().logout(headerauth, cookies)
    