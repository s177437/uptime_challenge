import pika
import Pyro4

class Invoice :

    pricelist={"m1.micro":0.05, "m1.tiny": 0.1, "m1.small": 0.2, "m1.medium":0.4, "m1.large":0.8, "m1.xlarge": 1.6, "m1.2xlarge":3.2}

    def calculatePrice(self,accountingdict):
        price = 0
        for flavor, numberofunits in accountingdict.iteritems():
            unitprice=self.pricelist[flavor]
            price+=unitprice*numberofunits
        return price/12

i=Invoice()
print i.calculatePrice({"m1.tiny":2,"m1.2xlarge":0,"m1.xlarge":0,"m1.micro":0,"m1.medium":1,"m1.large":0,"m1.small":0})