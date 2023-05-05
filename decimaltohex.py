from decimal import Decimal

class DTH:
      
    # methods
    def convertohex(self, val):
        arr = []
        tmp = val *1000;
        hexval = hex(tmp)[2:].zfill(6)
        val1 = int(hexval[:2], 16)
        arr.append(val1)
        val2 =  int(hexval[2:4], 16)
        arr.append(val2)
        val3 =  int(hexval[4:6], 16)
        arr.append(val3)
        return arr
    def converttohexforpecc(self,val):
        arr1= []
        hexval = val[2:].zfill(4)
        val1 = int(hexval[:2], 16)
        arr1.append(val1)
        val2 =  int(hexval[2:4], 16)
        arr1.append(val2)
        return arr1