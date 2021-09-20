import graphviz
from bs4 import BeautifulSoup
import threading
import os
from fiber import fiber

filePathName = "test-output/round-table.gv"
filePublic = "test-output"

mode = "svg"


eventMap = {}
eventList = ["click"]

def pushData(initList,viewData,childName):
    # print(viewData,childName)
    initList.append({
        "nodeName":viewData.get("nodeName"),
        "childName":childName.get("nodeName"),
        "childKey": childName.get("nodeKey"),
        "nodeEvent":viewData.get("nodeEvent"),
        "nodeKey":viewData.get("nodeKey")
    })

def pushEvent(viewData):
    if viewData.get("nodeKey"):
        nodeSelfKey = viewData["nodeKey"]
    else:
        nodeSelfKey = viewData["nodeName"]
    eventMap[nodeSelfKey] = {"nodeEvent" : viewData.get("nodeEvent"),"relation":viewData.get("relation"),"nodeKey":viewData.get("nodeKey"),"nodeName":viewData["nodeName"]}

def recursion(viewData,initList,mainstream=False):
    if mainstream:
        pushEvent(viewData)
    if "child" in viewData:
        for i in viewData["child"]:
            pushData(initList, viewData,i)
            recursion(i,initList,mainstream)
    else:
        pass


def renderDigraph(initList,eventMap,fileName,**kwargs):
    print(initList,eventMap,fileName,kwargs)
    u = graphviz.Digraph('unix', filename='unix.gv',
                         node_attr={'color': 'lightblue2', 'style': 'filled'})
    u.attr(size='6,6')
    for item in eventMap:
        # print(item, "initList[item].")
        if eventMap[item].get("nodeKey"):
            u.node(eventMap[item].get("nodeKey"),eventMap[item].get("nodeName"))

    for node in initList:
        # print(initList,"initList")
        if node.get("nodeKey"):
            if node.get("childKey"):
                u.edge(node["nodeKey"], node["childKey"])
            else:
                u.edge(node["nodeKey"], node["childName"])
        else:
            if node.get("childKey"):
                u.edge(node["nodeName"], node["childKey"])
            else:
                u.edge(node["nodeName"], node["childName"])


    u.format = kwargs["mode"] if kwargs.get("mode") else  mode
    u.render(fileName, view=kwargs['views'])


def handleRelationData(relation,map,list):
    fileAbsName = os.path.join(os.getcwd(), filePublic,map+".gv")
    recursion(relation, list, False)
    renderDigraph(list,{},fileAbsName,views = False,mode="png")

    print(fileAbsName+ "." + mode)

    # relationSvg = readTemplate("embed.js")
    # print(relationSvg)
    # print("handleRelationData",list)

def relationList(eventMap):
    for map in eventMap:
        if eventMap[map].get("relation") and type(eventMap[map].get("relation")) != str:
            print(eventMap[map].get("relation"))
            relationListBoth = []
            lyon = threading.Thread(target=handleRelationData,args=(eventMap[map].get("relation"),map,relationListBoth))
            lyon.start()



def createSvgFactory(viewData):
    print(viewData,"viewData")
    if not (type(viewData) is dict):
        return;
    initList = []
    recursion(viewData,initList,True)
    renderDigraph(initList,eventMap,filePathName,views = True )
    relationList(eventMap)
    # print(initList,"3")



def xpathDom(readFilesLine,**kwargs):
    html = BeautifulSoup(readFilesLine, 'html.parser')
    for item in html.select("g g title"):
        kwargs.index += 1
        if item.text in eventMap:
            text = item.text
            if eventMap[text]["nodeEvent"] in eventList:
                readStringHoder = kwargs.readTemplateStr.format(
                    index=kwargs.index, node=item.parent['id'],
                    eventName=eventMap[text]["nodeEvent"],
                    relation=eventMap[text]["relation"],
                    nodeKeyName=eventMap[text]['nodeKey'] if eventMap[text]['nodeKey'] else eventMap[text]['nodeName']
                )
                kwargs.readStringHoders += readStringHoder + "\r\n"


def readFile(filePathName):
    filePathName = filePathName + "." + mode
    fileAbsName = os.path.join(os.getcwd(),filePathName)
    # print(fileAbsName)
    listenerEvent = ""
    with open(fileAbsName,"r") as f:
        readFiles = f.read()
        html = BeautifulSoup(readFiles,'html.parser')
        # print("f.read()",readFiles, "f.read()")
        index = 0
        readTemplateStr = readTemplate("template.js")
        customEvent = readTemplate("customFunction.js")
        readStringHoders = customEvent + "\r\n"
        for item in html.select("g g title"):
            index += 1
            if item.text in eventMap:
                text = item.text
                if eventMap[text]["nodeEvent"] in eventList:
                    readStringHoder = readTemplateStr.format(
                        index=index,node=item.parent['id'],
                        eventName=eventMap[text]["nodeEvent"],
                        relation=eventMap[text]["relation"],
                        nodeKeyName = eventMap[text]['nodeKey'] if eventMap[text]['nodeKey'] else eventMap[text]['nodeName']
                    )
                    readStringHoders += readStringHoder + "\r\n"

        createFileName = os.path.join(os.getcwd(), "scriptLister.js")
        scriptPathName = createFunctionFactory(readStringHoders,createFileName)
        readF = readFiles.replace("</svg>","<script>"+readStringHoders+"</script></svg>")
        # print(readF)
        with open(fileAbsName,"w") as fw:
            fw.write(readF)



def createFunctionFactory(readStringHoder,createFileName):
    with open(createFileName,"w") as f:
        f.write(readStringHoder)


def readTemplate(fileName):
    filePathName = os.path.join(os.getcwd(),fileName)
    with open(filePathName,"r") as f:
        return f.read()
        # print(f.read())




if __name__ == "__main__":

    createSvgFactory(fiber)
    readFile(filePathName)
    # readTemplate()

