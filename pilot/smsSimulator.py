import re, csv, time, random, getopt, sys, locale
from datetime import datetime
import philippinesData, cropInputsData

#Global variables
scn = "+63 915 866 8018" #Smart Coops number
sleepTime = 0 #to simulate time in between SMS messages, 1.5 secs more realistic
affirmativeAns = ['yes','y','ye','ya','oo','yeah','yup','1']

provinces = philippinesData.provinces
citiesOrM = philippinesData.citiesOrMunici
coops = philippinesData.coops
crops = philippinesData.crops
cropInputs = cropInputsData.cropInputs

class Farmer():
    """Farmers have a name, a mobile phone number, and possibly belong to a coop"""

    def __init__(self, mobileNum = None, name = None, coop = None, crops = None, loanBal = 0, savingsBal = 0, purchaseHist = []):
        self.mobileNum = mobileNum
        self.name = name
        self.coop = coop
        self.crops = crops
        self.loanBal = loanBal
        self.savingsBal = savingsBal
        self.purchaseHist = purchaseHist

    def getMobileNum(self):
        return self.mobileNum
    def setMobileNum(self, mobileNum):
        self.mobileNum = mobileNum

    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

    def getCoop(self):
        return self.coop
    def setCoop(self, coop):
        self.coop = coop

    def getCrops(self):
        return self.crops
    def setCrops(self, crops):
        self.crops = crops

    def getLoanBal(self):
        return self.loanBal
    def setLoanBal(self, loanBal):
        self.loanBal = loanBal

    def getSavingsBal(self):
        return self.savingsBal
    def savingsWithdraw(self,amount):
        self.savingsBal = self.savingsBal - amount
    def savingsDeposit(self,amount):
        self.savingsBal = self.savingsBal + amount

    def getPurchaseHist(self):
        return self.purchaseHist
    def setPurchaseHist(self, purchaseHist): #eventually should create add/delete methods for purchase history
        self.purchaseHist = purchaseHist

#For debugging purposes
sampleFarmer = Farmer(12341234,'Danny Castonguay','San Benito Multipurpose Coop',[{'name':'Cloves','size':1.5},{'name':'Cocoa beans','size':12.7},{'name':'Coconuts','size':6},{'name':'Coffee, green','size':22}],1200000,600000)

class Location():
    """Each exchange has a location as provided by the telco, which we use to inform the farmer of prices or local resources"""
    def __init__(self, province = None, cityOrM = None, gpsCoord = None):
        self.province = province
        self.cityOrM = cityOrM
        self.gpsCoord = gpsCoord
    def getProvince(self):
        return self.province
    def setProvince(self, province):
        self.province = province
    def getCityOrM(self):
        return self.cityOrM
    def setCityOrM(self, cityOrM):
        self.cityOrM = cityOrM
    def getGPSCoord(self):
        return self.gpsCoord
    def setGPSCoord(self, name):
        self.gpsCoord = gpsCoord
    def getName(self):
        return self.cityOrM + ", " + self.province

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).  """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

def searchList(myStr, myList):
    """Returns the set of strings resulting from a substring search"""
    pattern = re.compile(r'.*'+myStr+'.*', re.IGNORECASE)
    results = []
    for l in myList:
        r = re.search(pattern,l)
        if r is not None:
            results.append(r.group())
    return results

def searchListDict(myStr, myListDict, key):
    """Returns the set of dictionaries resulting from a substring search over specific key"""
    pattern = re.compile(r'.*'+myStr+'.*', re.IGNORECASE)
    results = []
    for d in myListDict:
        r = re.search(pattern,d[key])
        if r is not None:
            results.append(d)
    return results

def makeListStr(myList):
    myStr = ''
    for i in range(1,len(myList)+1):
        myStr = myStr + ' ' + str(i) + ") " + myList[i-1] + ','
    return myStr[1:-1]

def affirmative(ans):
    return any([ans.lower() == x for x in affirmativeAns])

def phPesos(value):
    """Formats a numerical value into a string with thousand separators ','"""
    return 'P'+'{:,.2f}'.format(value)

def smsPrint(body):
    """Prints a pretty sms msg on the terminal"""
    smsSeparator = "=================================================================="
    width = len(smsSeparator)
    smsBorder = '-'*width
    print '\n\n'+smsSeparator
    print datetime.now().strftime("%a, %b %d at %I:%M%p") + ". New SMS from " + scn + ":"
    print smsBorder
    print wrap_onspace(body, width)
    print smsSeparator
    time.sleep(sleepTime)

def getSMS():
    """Simulates the user sending an SMS to SMART Coops"""
    print '\n'
    prompt = 'Send a new SMS to ' + scn + ' (SMART Coops) :\nMessage Content > '
    newSMS = raw_input(prompt)
    print '\n                                     Message sent...\n\n\n\n\n',
    time.sleep(sleepTime)
    print '\n\n\n\n\n'
    return newSMS

def getName():
    """Retrieves and confirms the name of the farmer"""
    smsPrint("Please reply to this SMS with your name (ex: Capitan, Sergio).")
    name = getSMS()
    smsPrint("Pleased to meet you "+name+". Did I get your name correctly? (Reply yes or no). ")
    if affirmative(getSMS()):
        reply = "Great, thank you for confirming your name, "+name
        reply += ". SMART Coops helps you find out about prices for crop inputs, crop produce, loans, and more."
        smsPrint(reply)
        return name
    else:
        return getName()

def getGPSCoord():
    """presumably we would retrive information from the telco as to the location from where the farmer is calling from, 
    and use that in the getCoop function, not implemented"""
    return 0

def getNearbyProvince(gpsCoord):
    return 'Laguna'

def getNearbyCityOrM(gpsCoord):
    return 'San Pablo'

def getNearbyCoops(loc):
    """given a location, returns the nearby cooperatives"""
    return ['San Benito Multipurpose Coop', 'San Pablo Cooperative', 'Calamba Association of Rice Planters']

def getItemFromList(itemType, myList):
    """Obtains from the user an item from a list, offering the user to either enter a corresponding number or a substring search"""
    smsPrint("Select your "+itemType+" from this list: "+makeListStr(myList))
    ans = getSMS()
    try: #check if user entered a numeric value
        num = int(ans)
        if num in range(1, len(myList)+1):
            return myList[num-1]
        else:
            getItemFromList(itemType,myList)
    except ValueError: #it's ok, user might have written an answer instead of a numeric value
        matchingItems = searchList(ans,myList)
        if len(matchingItems) == 0:
            return getItemFromList(itemType,myList)
        if len(matchingItems) == 1:
            return matchingItems[0]
        if len(matchingItems) > 1:
            return getItemFromList(itemType,matchingItems)

def getProvince():
    reply = 'What province is your farm located in (e.g. '+ random.choice(provinces) 
    reply += ')? You may spell only a few letters and I will search for it.'
    smsPrint(reply)
    ans = getSMS()
    likelyProvinces = searchList(ans,provinces)
    if len(likelyProvinces) == 1:
        smsPrint("Is your farm located in "+likelyProvinces[0]+"? (yes or no)")
        if affirmative(getSMS()):
            return likelyProvinces[0]
        else:
            return getProvince()
    elif len(likelyProvinces) == 0:
        smsPrint("No provinces found that match '"+ans+"'.")
        return getProvince()
    else:
        return getItemFromList('province',likelyProvinces)

def getCityOrM(province):
    reply =  'Your farm is in '+province+' province. What city or municipality is it located nearest to (e.g. '
    reply += random.choice(citiesOrM[province])
    reply += ')? You may spell only a few letters and I will search for it.'
    smsPrint(reply)
    ans = getSMS()
    likelyCitiesOrM = searchList(ans,citiesOrM[province])
    if len(likelyCitiesOrM) == 1:
        smsPrint("Is your farm located in "+likelyCitiesOrM[0]+", "+province+"? (yes or no)")
        if affirmative(getSMS()):
            return likelyCitiesOrM[0]
        else:
            return getCityOrM(province)
    elif len(likelyCitiesOrM) == 0:
        smsPrint("No cities or municipalities found that match '"+ans+"'.")
        return getCityOrM(province)
    else:
        return getItemFromList('city or municipality',likelyCitiesOrM)

def getCoop(loc = None):
    if loc == None:
        gpsCoord = getGPSCoord()
        loc = Location(getNearbyProvince(gpsCoord), getNearbyCityOrM(gpsCoord), gpsCoord)
    coops = getNearbyCoops(loc)
    optionsStr = makeListStr(coops+['Other', 'Not member of a cooperative'])
    reply = "I see that you are sending messages from near "+loc.getName()
    reply += ". Which cooperative are you a member of? "+optionsStr
    smsPrint(reply)
    ans = getSMS()
    try:
        i = int(ans)
        if i in range(1,len(coops)+1):
            smsPrint("You are a member of "+coops[i-1]+", is this correct? (yes or no)")
            if affirmative(getSMS()):
                return coops[i-1]
            else:
                return getCoops2(loc)
        elif i == len(coops)+1:
            loc.setProvince(getProvince())
            loc.setCityOrM(getCityOrM(loc.getProvince()))
            return getCoop(loc)
        elif i == len(coops)+2:
            return None
        else:
            raise ValueError
    except ValueError:
        smsPrint("I don't understand. Your answer '"+ans+"' is not one of the menu options.")
        getCoop(loc)

def getCropName():
    reply =  'What crop is your farm cultivating (e.g. ' + random.choice(crops)
    reply += ')? You may spell only a few letters and I will search for it.'
    smsPrint(reply)
    ans = getSMS()
    likelyCrops = searchList(ans,crops)
    if len(likelyCrops) == 1:
        smsPrint("Is your farm cultivating "+likelyCrops[0]+"? (yes or no)")
        if affirmative(getSMS()):
            return likelyCrops[0]
        else:
            return getCropName()
    elif len(likelyCrops) == 0:
        smsPrint("No crops found that matches '"+ans+"'.")
        return getCropName()
    else:
        return getItemFromList('crop',likelyCrops)

def getCropSize(crop):
    """Prompts user for the size of the crop farming"""
    ansEx =  str(random.randint(0,20))+'.'+str(random.randint(0,9))
    reply = 'Your farm is cultivating '+crop+', please try to estimate the number of hectares (e.g. '
    reply += ansEx + ') for this crop.'
    smsPrint(reply)
    ans = getSMS()
    try:
        if float(ans) >= 0:
            smsPrint("You are cultivating "+ans+" hectares of "+crop+", is this correct? (yes or no)")
            if affirmative(getSMS()):
                return float(ans)
            else:
                getCropSize(crop)
        else:
            raise ValueError
    except ValueError:
        smsPrint("I cannot understand your response. '"+ans+"' is not a valid answer (e.g. "+ansEx+").")
        getCropSize(crop)

def getCrops():
    """Prompts farmer for all of the crops being cultivated"""
    confirmation = 'no'
    crops = []
    while not affirmative(confirmation):
        cropName = getCropName()
        cropSize = float(getCropSize(cropName))
        crops.append({'name':cropName,'size':cropSize})
        cropList = []
        for c in crops:
            cropList.append(str(c['size']) + " hectares of " + c['name'])
        smsPrint("You are cultivating " + makeListStr(cropList) + ". Are you cultivating anything else? (yes or no)")
        ans = getSMS()
        if affirmative(ans):
            confirmation = 'no'
        else:
            confirmation = 'yes'
    return crops

def firstTime():
    """Informs the farmer of what SMART Coop is, and of the cost"""
    print """
  ___ __  __   _   ___ _____    ___                  
 / __|  \/  | /_\ | _ \_   _|  / __|___  ___ _ __ ___
 \__ \ |\/| |/ _ \|   / | |   | (__/ _ \/ _ \ '_ (_-<
 |___/_|  |_/_/ \_\_|_\ |_|    \___\___/\___/ .__/__/
                                            |_|      
"""
    print "\n"
    print "                    |-------------------------------------------|"
    print "                    | SMART Coops SMS Simulator. For demo only. |" 
    print "                    |                      All rights reserved. |"
    print "                    |-------------------------------------------|"
    print "\n\n"
    print "Context:"
    print " The first time around, the farmer sends an SMS to SMART Coops."
    print " The sms could be empty, or could require a passcode or a"
    print " keyword like 'join' for the system to engage.\n\n\n"
    s = "Hello, it is the first time you are using SMART Coops. "
    s = s + "Note that SMS sent to and received from SMART Coops are free of charge, so do not worry about your load balance."
    smsPrint(s)
    f = Farmer()
    f.setName(getName())
    f.setCoop(getCoop())
    f.setCrops(getCrops())
    return f

def applyLoanMenu(farmer):
    confirmation = 'no'
    while not affirmative(confirmation):
        reply = "SMART Coops apply for loan. Your current loan balance is "+phPesos(farmer.getLoanBal())
        reply = reply+". Please reply with the amount of loan you would like to apply for (numeric value only, in PHP)."
        smsPrint(reply)
        loanAmount = getSMS()
        try:
            l = int(loanAmount)
            smsPrint("You are about to apply for a loan of "+phPesos(l)+", is the amount correct? (yes or no)")
            ans = getSMS()
            if affirmative(ans):
                farmer.setLoanBal(farmer.getLoanBal()+l)
                farmer.savingsDeposit(l)
                reply = "Congratulation, your loan has been approved. "+phPesos(l)+" has been deposited in your account. "
                reply += "Your new loan balance is "+phPesos(farmer.getLoanBal())+". Returning to previous menu."
                smsPrint(reply)
                confirmation = 'yes'
            else:
                confirmation = 'no'
        except ValueError:
            smsPrint("I do not understand. Please reply with a numeric value. Your reply: '" + loadAmount + "' is not a numerical value.")

def viewLoanBalMenu(farmer):
    reply = "SMART Coops loan balance. Your current loan balance is "+phPesos(farmer.getLoanBal())
    reply += ". You currently have "+phPesos(farmer.getSavingsBal())+" in your savings account, available to purchase crop inputs."
    smsPrint(reply + " Returning to previous menu.")

def makeLoanPaymentMenu(farmer):
    smsPrint("This menu is not complete yet... Returning to previous menu")

def loansMenu(farmer):
    optionsStr = makeListStr(['Apply for loan','View loan balance','Make loan payment','Main menu'])
    confirmation = 'no'
    while not affirmative(confirmation):
        smsPrint("SMART Coops loans menu. What would you like to do: "+optionsStr)
        ans = getSMS()
        try:
            if int(ans) == 4:
                confirmation = 'yes'
            elif int(ans) in range(1,4):
                {1:applyLoanMenu,2:viewLoanBalMenu,3:makeLoanPaymentMenu}[int(ans)](farmer)
            else:
                smsPrint("Please reply with a numeric value. Your reply: '" + ans + "' is not one of the menu options")
        except ValueError:
            smsPrint("Please reply with a numeric value. Your reply: '" + ans + "' is not one of the menu options")

def buyInputMenu(farmer,crop):
    confirmation = 'no'
    likelyInput = []
    while not affirmative(confirmation):
        reply = "Buy inputs, " + crop + " menu. Please enter the name of the product you are looking for (e.g. "
        randomInput = random.choice(cropInputs)
        smsPrint(reply + randomInput["productName"] + ' manufactured by ' + randomInput["brand"] + ') or reply 0 to return to previous menu. Please try to spell the product name as completely as possible.')
        ans = getSMS()
        if ans == '0':
            return farmer
        likelyInput =  searchListDict(ans, cropInputs, "productName")
        if len(likelyInput) == 1:
            ic = likelyInput[0]
            name = ic["productName"]
            price = ic["price"]
            units = ic["units"]
            smsPrint("Are you interested in buying "+name+" for the price of "+phPesos(price)+" per "+units+"? (yes or no)")
            ans = getSMS()
            if affirmative(ans):
                smsPrint("How many units of "+name+" do you want to buy for the price of "+phPesos(price)+" per "+units+"? (Please answer a number)")
                try:
                    quantity = int(getSMS())
                    if quantity >= 0:
                        amount = quantity*price
                        farmer.savingsWithdraw(amount)
                        ic["purchaseDate"] = datetime.now().strftime("%a, %b %d at %I:%M%p")
                        ic["quantity"] = quantity
                        ic["amount"] = amount
                        farmer.setPurchaseHist(farmer.getPurchaseHist().append(ic))
                        reply = "You have purchased "+str(quantity)+units+" of "+name+" for the total amount of "+phPesos(amount)
                        reply += ". Your new savings account balance is "+phPesos(farmer.getSavingsBal())+"."
                        smsPrint(reply)
                except ValueError:
                    smsPrint("Please reply with an whole number. Your reply: '" + quantity + "' is not valid")
        elif len(likelyInput) == 0:
            smsPrint("Unfortunately, no crop input matches your spelling.")
        else:
            randomInput = random.choice(cropInputs)
            reply = "Please be more specific, many crop inputs match your spelling, such as "
            reply += randomInput["productName"] + ' manufactured by ' + randomInput["brand"] + "."
            smsPrint(reply)
    return farmer

def inputsMenu(farmer):
    optionsList = []
    for c in farmer.getCrops():
        optionsList += [c["name"] + " inputs"]
    optionsStr = makeListStr(["View all products"] + optionsList + ["Main menu"])
    confirmation = 'no'
    while not affirmative(confirmation):
        reply = "Buy inputs menu. You currently have "+phPesos(farmer.getSavingsBal())
        reply += " in your savings account. What would you like to buy: "+optionsStr
        smsPrint(reply)
        ans = getSMS()
        try:
            if int(ans) > len(farmer.getCrops())+1: #+1 bcz 'View all products' is first option, which means main menu is selected option
                confirmation = 'yes'
            elif ans == '1':
                buyInputMenu(farmer,'All products')
            else:
                buyInputMenu(farmer,farmer.getCrops()[int(ans)-2]['name']) #-1 bcz indexing list, -1 because of 'All products' option
        except ValueError:
            smsPrint("Please reply with a numeric value. Your reply: '" + ans + "' is not one of the menu options")

def harvestMenu(farmer):
    optionsStr = makeListStr(['Loans','Buy inputs','Sell harvest','Farm advices','View my profile','Contact SMART Coops'])
    smsPrint("This menu is not complete yet... Returning to main menu")
def adviceMenu(farmer):
    optionsStr = makeListStr(['Loans','Buy inputs','Sell harvest','Farm advices','View my profile','Contact SMART Coops'])
    smsPrint("This menu is not complete yet... Returning to main menu")

def farmerProfileMenu(farmer):
    #confirmation = 'no'
    #    while not affirmative(confirmation):
    reply = "Name: "+ farmer.getName() + ". "
    reply += "Coop: "+ farmer.getCoop() + ". "
    cropList = []
    for c in farmer.getCrops():
        cropList.append(c['name']+" on "+str(c['size'])+" hectares")
    reply += "Crops cultivated: "+ makeListStr(cropList) + ". "
    reply += "Current loan balance: " + phPesos(farmer.getLoanBal()) + ". "
    reply += "Current savings balance: " + phPesos(farmer.getSavingsBal()) + ". "
    optionsStr = makeListStr(['View purchase history', 'Change name', 'Change coop', 'Change crops', 'Main menu'])
    reply += "What actions would you like to take: "+optionsStr
    smsPrint(reply)
    ans = getSMS()
    #    try:
    #       {1:loansMenu,2:inputsMenu,3:harvestMenu,4:adviceMenu,5:farmerProfileMenu,6:contactSCMenu}[int(ans)](farmer)
    #  except ValueError:
    #     smsPrint("Please reply with a numeric value. Your reply: '" + ans + "' is not one of the menu options")

def contactSCMenu(farmer):
    optionsStr = makeListStr(['Loans','Buy inputs','Sell harvest','Farm advices','View my profile','Contact SMART Coops'])
    smsPrint("This menu is not complete yet... Returning to main menu")

def mainMenu(farmer):
    optionsStr = makeListStr(['Loans','Buy inputs','Sell harvest','Farm advices','View my profile','Contact SMART Coops'])
    while True:
        smsPrint("SMART Coops main menu. What would you like to do: "+optionsStr)
        ans = getSMS()
        try:
            {1:loansMenu,2:inputsMenu,3:harvestMenu,4:adviceMenu,5:farmerProfileMenu,6:contactSCMenu}[int(ans)](farmer)
        except ValueError:
            smsPrint("Please reply with a numeric value. Your reply: '" + ans + "' is not one of the menu options")
    

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    """ As suggested in http://www.artima.com/weblogs/viewpost.jsp?thread=4829 """

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        mainMenu(firstTime())
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
