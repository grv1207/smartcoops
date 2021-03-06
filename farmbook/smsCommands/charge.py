from farmbook.smsfct import *

def charge(entry):
    """
    Description

    When farmers borrow in kind from the cooperative; "pautang" of supplies; crop inputs or supplies such as LPG.

    Fields

    Date (of transaction)
    Sold to (Customer/Farmer)
    For each product sold
    Description (Name of product or supply)
    Quantity (of each product or supply)
    Unit price (of each product or supply)
    Amount (Quantity * Unit Price)
    Total Amount (Sum of Amounts for each product ordered)
    Sample SMS Format

    CHARGE/Customer/Description/Quantity/Unit Price

    Examples:

    `charge/charlie santos/24D/2/25`
    `ChArGe/ChArLiE SaNTos/viking/3/100`
    `charge/charlie santos/viking/3/100/organic fertilizer/2/25`
    """
    #get coop from entry SMS number.
    #find if item is in the inventory for the coop. If it isn't, still move forward with the transaction
    #but warn the coop that they need to update their inventory because one of the item is now in negative inventory.
    #add loan amount to farmer's account
    #send confirmation SMS to farmer

    params = getParams(entry)
    smsCommand = params[0]
    farmerName = params[1]
    item = params[2]
    try:
        numUnits = params[3]
        price = params[4]
        amount = float(numUnits)*float(price)
        reply = "Comfirmed. CHARGE on LOAN to %s. Total amount %s. Purchase: %s units of %s." % (farmerName,phPesos(amount),numUnits,item)
    except ValueError: 
        reply = "Could not complete cash voucher, amount entered is not numerical. "
        reply += "Example of a valid entry would be: "+smsCommand+"/"
        reply += farmerName+"/"+description+str(450.50)
        return reply
    sendSMS(getMobile(entry),reply)
