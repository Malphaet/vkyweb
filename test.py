# Copyleft (c) 2016 Cocobug All Rights Reserved.

from minitest import minitest

import types
from blessings import Terminal
from generator import *


#import vkyweb

term=Terminal()
unit=minitest.testUnit
simple=minitest.simpleTestUnit
group=minitest.testGroup
dual=models.dual

class testParser(simple):
    """Testing the file parser"""
    def __init__(self,name):
        super(testParser,self).__init__(name)

    def _tests_all(self):
        config_langs=["*","en","fr"]
        self.currentTest("parser:load")
        config=file_parser.parse_file("sites/example_website/_config.txt")
        self.addSuccess()

        self.currentTest("parser_config")
        if (type(config)==file_parser.WebPage):
            self.addSuccess()
        else:
            self.addFailure("config is supposed to be a WebPage")


        self.currentTest("parser_config:var:type")
        if type(config.variables)==dict:
            self.addSuccess()
        else:
            self.addFailure("config is not a dict")

        self.currentTest("parser_config:lang")
        for lang in config_langs:
            if lang not in config.list_of_lang:
                self.addFailure("lang {} not in config".format(lang))
        self.addSuccess()

        self.currentTest("parser_config:content")
        if type(config.content)==list:
            for e in config.content:
                if len(e)!=2:
                    self.addFailure("line is not formated with [text,[lang]]")
            self.addSuccess()
        else:
            self.addFailure("content is supposed to be a list of lines&langs")

        self.currentTest("parser_config:generator")
        gen=config.get_next_line("*")
        if type(gen)==types.GeneratorType:
            self.addSuccess()
        else:
            self.addFailure("get_next_line is supposed to be a generator")

        self.currentTest("parser_config:generator:lang")
        content_by_lang={'*':[],'fr':[],'en':[]}
        for line in config.content:
            txt,langs=line[0],line[1]
            for lang in langs:
                if lang in ["fr","en"]:
                    content_by_lang[lang].append(txt)
                elif lang=="*":
                    for l in config_langs:
                        content_by_lang[l].append(txt)
        success=True
        for l in ["en","fr"]:
            generator_table=[e for e in config.get_next_line(l)]
            if len(content_by_lang[l])!=len(generator_table):
                self.addFailure("generator and model don't have the same length [{}]".format(l))
                success=False
            for i in range(len(generator_table)):
                if generator_table[i]!=content_by_lang[l][i]:
                    self.addFailure("generator and model have different content [{}:{}]".format(l,i))
                    success=False
        if success:
            self.addSuccess()

        self.currentTest("parser_config:generator:type")
        for l in config.get_next_line("*"):
            if type(l)!=str:
                self.addFailure("type is supposed to be a string")

        self.currentTest("parser_file:open")
        index=file_parser.parse_file("sites/example_website/index.txt")
        self.addSuccess()

        self.currentTest("parser_file")
        contentCheck={
            'error':['![Alt text](/path/to/img.jpg)', "If you don't close properly something __a lot of content will be lost", '__in the generation', 'process', 'Like this']
            ,"*":['![Alt text](/path/to/img.jpg)', 'Like this']
            ,"en":['Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '![Alt text](/path/to/img.jpg)', 'Like this']
            ,"fr": ['Loreme ipsume dolore site amete, consecteture adipisicinge elite, sede doe eiusmode tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolore ine reprehenderite ine voluptate velite esse cillume dolore eu fugiatte nulla pariature. Excepteure sinte occaecate cupidatate none proidente, sunta ine culpa qui officia deserunte mollite anime ide est laborume.', '![Alt text](/path/to/img.jpg)', 'Like this']
            ,"hidden":['![Alt text](/path/to/img.jpg)', 'Hiden text, can be used in many ways. Note that hidden is not a reserved keyword and is just treated separately in the generation process.', 'Like this']
            ,"useless":['![Alt text](/path/to/img.jpg)', 'The useless keyword is not reserved either, and since it wont be treated in the generation process, it will just be lost', 'Like this']
        }
        self.addSuccess()
        for lang in contentCheck.keys():
            self.currentTest("parser_file:"+lang)
            if contentCheck[lang]==[e for e in index.get_next_line(lang)]:
                self.addSuccess()
            else:
                self.addFailure("Error text doesn't match")


class testTree(simple):
    """docstring for testTree."""
    def __init__(self,name):
        super(testTree, self).__init__(name)

    def _testTree(self):
        list_of_lang=["fr","en","*"]
        self.currentTest("tree:load")
        webt=tree_parser.makeWebsite("sites/example_website")
        self.addSuccess()

        self.currentTest("tree:repr")
        if repr(webt)=="WebTree @ sites/example_website/":
            self.addSuccess()
        else:
            self.addFailure("Repr incorrect")


        self.currentTest("tree:get_title")
        if webt.get_title("en")!="Mulloland":
            self.addFailure("lang incorrect [en]")
        elif webt.get_title("fr")!="Mulehollande":
            self.addFailure("lang incorrect [fr]")
        else:
            self.addSuccess()

        self.currentTest("tree:config")
        if type(webt.config_file)!=file_parser.WebPage:
            self.addFailure("config malformed"+srt(type(webt.config_file)))
        else:
            self.addSuccess()


        self.currentTest("tree:name")
        if webt.name!="_config.txt":
            self.addFailure("malformed name"+webt.name)
        else:
            self.addSuccess()

        #webt.print_webtree("fr",'[fr] ')
        self.currentTest("tree:Poetry")
        poetry=webt.tree.get_subtree("Poetry","fr")
        if type(poetry)!=tree_parser.WebSubTree:
            self.addFailure("can't acess the Poetry subtree")
        else:
            self.addSuccess()

        self.currentTest("tree:Poetry:loading")
        poem1=poetry.get_node("poetry1","fr")
        if type(poem1)!=tree_parser.WebNode:
            self.addFailure("can't acess the node")
        else:
            self.addSuccess()

        self.currentTest("tree:Poetry:config")
        status=True
        for l in list_of_lang:
            if poem1.get_variable("title",l)!="Rose":
                status=False
                self.addFailure("title incorrect for {}".format(l))
        if status:
            self.addSuccess()

        self.currentTest("tree:Poetry:content")
        poem1content=poem1.get_content("fr").split("\n")
        if poem1content==["Une rose qui passe","Quelle est bien belle","Mais pourquoi donc","Esceque tu est jolie",""]:
            self.addSuccess()
        else:
            self.addFailure("can't load content")

        #webt.print_webtree('en')

class testModel(simple):
    """docstring for testModel."""
    def __init__(self,arg):
        super(testModel, self).__init__(arg)

    def _testModel(self):
        self.currentTest("loading:nodes")
        site=tree_parser.makeWebsite("sites/example_website")
        lang="fr"
        current_node=site.tree.get_node("index",lang)
        previous_node=site.tree.get_node("index",lang)
        self.addSuccess()

        self.currentTest("model:icons")
        status=True
        batch={
            "image":['/test.jpg',"very.bad.practice.png","mono/dont.do.txt/this.mp3.svg"],
            "audio":["33/%20mother%!of bad%20names.aiff"],
            "text":["no more/bad/name.txt"],
            "other":["why tho.why"]
        }
        for result,filenames in batch.items():
            for f in filenames:
                if (result!=model.getDataType(f)):
                    self.addFailure("'{}' is not from type {} ({} found)".format(f,result,model.getDataType(f)))
                    status=False
                    break
            if not status:
                break
        if status:
            self.addSuccess()

        self.currentTest("model:htmlpath")
        class falseNode(object):
            def __init__(self,name):
                self.name=name

        res=[model.makeHTMLName(falseNode("/bla/foo.bar")),model.makeHTMLName(falseNode("goo.foo.bar"))]
        expected=["/bla/foo.html","goo.foo.html"]
        success=True
        for i in range(len(res)):
            if res[i]!=expected[i]:
                self.addFailure("malformed HTML names expected {} (got {})".format(expected[i],res[i]))
                success=False
                break

        if success:
            self.addSuccess()

        #
        # menu=model.makeContainer(dual,site,current_node,previous_node,lang)
        # data=model.makeData(dual,current_node,lang)
        #
        # page=model.makePage(dual,site,lang,menu,data)
        #print(page)

class testDual(simple):
    """docstring for testDual."""
    def __init__(self, arg):
        super(testDual, self).__init__(arg)

    def _testDual(self):
        self.currentTest("dual:icon")
        if((dual.geticon('audio')=="music") and (dual.geticon("other")=="file")):
            self.addSuccess()
        else:
            self.addFailure("non conform dict"+str([e for e in dual.icons.keys()]))

        dualDict={"pagetitle":"#_pagetitle_#","websitename":"#_websitename_#","menu":"\{menu\}","page":"\{page\}"}
        self.testThisDictOnDis("dual:container",dualDict,dual.container,str)

        menuDict={'previous':"TESTPREV",'menulist':"\{menulist\}",'articles':"#_articles_#"}
        self.testThisDictOnDis("dual:menu",menuDict,dual.menu,str)

        contentDict={"content":"\{content\}","title":"\{title\}"}
        self.testThisDictOnDis("dual:content",contentDict,dual.content,str)

        menuDict={"text":"TESTOEXT","link":"NONE","datatype":"audio"}
        menuDictReturn={"text":"TESTOEXT","link":"NONE","datatype":dual.geticon("audio")}
        self.testThisDictOnDis("dual:menuitem",menuDict,dual.menuitem,str,menuDictReturn)

        self.currentTest("dual:makeSubNodelist")

        self.currentTest("site:loading")
        site=tree_parser.makeWebsite("sites/example_website")
        self.addSuccess()

        status=True
        linkList=dual.makeSubNodelist(site.tree,"en",model.getDataType,model.makeHTMLName)
        # print(site.tree.subtree["Poetry"]["*"].config_file)
        nominalLinkList=['<li><a href="index.html"><i class="fa fa-book "></i>Transaltionus</a></li>',
        '<li><a href="article1.html"><i class="fa fa-book "></i>First article</a></li>',
        '<li><a href="Poetry"><i class="fa fa-folder "></i>Poetry</a></li>']
        for i in range(len(nominalLinkList)):
            if linkList[i] not in nominalLinkList:
                self.addFailure("link {} malformed (expected {})".format(i,nominalLinkList[i]),nonDestructive=True)
                self.addFailure("                  (got      {})".format(linkList[i]),nonDestructive=True)
                status=False

        if status:
            self.addSuccess()

    def testThisDictOnDis(self,name,testDict,testFunction,returnType=str,returnDict=None):
        res=testFunction(**testDict)
        if returnDict==None:
            returnDict=testDict
        self.currentTest(name+":type")
        if type(res)==returnType:
            self.addSuccess()
        else:
            self.addFailure("wrong return type (expected {}, got {})".format(type(res),returnType))
        # print(res)
        self.currentTest(name+':content')
        status=True
        for key,val in returnDict.items():
            if res.find(val)<0:
                self.addFailure("can't find {}".format(key))
                status=False
                break
        if status:
            self.addSuccess()
        # menuitem(text,link,datatype)
        # makeSubNodelist(subnode,lang,getdatatype)

testVky=group(name="vkyWeb_all",terminal=term,verbose=1,align=42)
#testConfig=group(name="config",terminal=term,prefix="| ")
#testParser=group(name="parser",terminal=term,prefix="| ")
#testTree=group(name="tree",terminal=term,prefix="| ")
#testModel=group(name="model",terminal=term,prefix="| ")

#testVky.addTest(testParser)
#testVky.addTest(testTree)
#testVky.addTest(testModel)

#testParser time

testParser("file_parser").test()
testVky.addTest(testParser("file_parser"))
testVky.addTest(testTree("tree_parser"))
testVky.addTest(testModel("model"))
testVky.addTest(testDual("model:dual"))
#testVky.addTest(testConfig("testConfig",config)) test a config file

testVky.test()
