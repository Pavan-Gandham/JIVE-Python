from collections import Counter
from fileinput import filename
from itertools import count
import os
comments=[]
totalMethodCall=[]
totalLines=0
count=0
tempDict={}
constructorLineNum=[]
cTemp=""
tempp=[]
classList = []
funList = []
funPintList=[]
constructorList=[]
fileName=""
numOfContructor=0

class Diagram:

    def removeComents(self,file):
        ch='#'
        global comments
        for i in file:
         comments.append(i.split(ch, 1)[0])
         comments=' '.join(comments).split()
    
    def classList(self, file):
        for fun in file:
            if "class" in fun:
                head, sep, tail = fun.partition(":")
                y = str(head.split("class"))
                y = y[6:]
                y = y[:-2]
                c = y[len(y)-2:]
                y = f"{y}"
                classList.append(y)
                
    def functionList(self, file):
        for fun in file:
            if "def" in fun:
                head, sep, tail = fun.partition("(")
                x = str(head.split("def"))
                x = x[6:]
                x = x[:-2]
                x = f".{x}"
                funList.append(x)
          
    def constructormethod(self,file):
       for (i, fun) in enumerate(file):
         for cName in classList:
            if cName in fun:
              global constructorLineNum
              if "=" and "(" and ")"in fun:
               constructorLineNum.append(i)
               constructorIndexPos = fun.find("=")
               constructorList.append(fun[:constructorIndexPos])
              global cTemp
              cTemp=cName
              inc = 1
              global tempDict
              for i in constructorList:
                tempDict[i] = cTemp+":"+str(inc)
                inc+=1
    
    def constructorPrint(self,file):
            for word in classList:
              if word in file:
                 if "(" in file:
                   a = file.split("=")
                   a = a[0]
                   global count  
                   count+=1
                   totalMethodCall.append(f"main,{count},{fileName},Method Call,caller={tempDict.get(a)}#main:1,target={tempDict.get(a)}#{tempDict.get(a)}")
                   count+=1
                   totalMethodCall.append(f"main,{count},{fileName},Method Exit,returner={tempDict.get(a)}#{tempDict.get(a)},value=")
                         
    def funtionPrint(self,file):
          for word in funList:
              if word in file:
                a = file.split(".")
                a = a[0]
                funPintList.append(word)  
                counter = Counter(funPintList)
                fTemp = word
                fTemp = fTemp[1:]
                global count  
                count+=1
                totalMethodCall.append(f"main,{count},{fileName},Method Call,caller={tempDict.get(a)}#main:1,target={tempDict.get(a)}#{fTemp}:{counter[word]}")
                count+=1
                totalMethodCall.append(f"main,{count},{fileName},Method Exit,returner={tempDict.get(a)}#{fTemp}:{counter[word]},value=")

    def methodPrint(self,file):
        global count
        lines = file[constructorLineNum[0]:totalLines]
        count+=1
        totalMethodCall.append(f"main,{count},{fileName},Method Call,caller=SYSTEM,target={cTemp}#main:1")
        for line in lines:
         self.constructorPrint(line)
         self.funtionPrint(line)
        count+=1
        totalMethodCall.append(f"main,{count},{fileName},Method Exit,returner={cTemp}#main:1,value=")   

    def umlCode(self,file):
            print("@startuml")
            for line in file:
                if f"caller=SYSTEM" in line:
                   print(f"->{cTemp} :main1")
                   print(f"activate {cTemp}")
                elif f"target" in line:
                  target = line.split(",")
                  target = target[-1]
                  target = target.split("=")
                  targetTotal = target[1]
                  targetTotal = targetTotal.replace(":","")
                  targetHash = targetTotal.split("#")[0]
                  targetTotal = targetTotal.replace("#"," :")
                  print(f"{cTemp} -> {targetTotal}") 
                  print(f"activate {targetHash}")
                elif f"returner={cTemp}#main:1" in line:
                  print(f"<--{cTemp}")
                  print(f"deactivate {cTemp}")
                elif f"returner" in line:
                  print(f"{cTemp} <-- {targetHash}")
                  print(f"deactivate {targetHash}")
            print("@enduml")
                
        
def main():
    obj = Diagram()
    file = open("Queue.py", "r")
    inputFile = file.readlines()
    k = []
    k = [x.replace(' ', '') for x in inputFile]
    file.close()
    global totalLines
    global fileName
    fileName = os.path.basename(file.name)
    obj.removeComents(k)
    totalLines = len(comments)
    obj.classList(comments)
    obj.functionList(comments)
    #print(funList)
    obj.constructormethod(comments)
    obj.methodPrint(comments)
    obj.umlCode(totalMethodCall)
   
    
if __name__ == "__main__":
        main()