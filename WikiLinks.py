import urllib.request
from html.parser import HTMLParser

#Priority Queue implementation
class PriorityQ:
    def __init__(self,ty,ar=[]):
        self.a=[]
        self.t=ty
        if ar:
            for i in ar:
                self.insert(i)
            
    def insert(self,item):
        assert type(item)==self.t
        self.a.append(item)
        self.BuildMaxHeap()
    
    def heapify(self,i):
        l=(2*i)+1
        r=(2*i)+2
        if(l<len(self.a) and r<len(self.a)):
            if(self.a[l].p>self.a[i].p and self.a[l].p>self.a[r].p):
                self.a[l],self.a[i]=self.a[i],self.a[l]
                self.heapify(l)
            if(self.a[r].p>self.a[i].p and self.a[r].p>self.a[l].p):
                self.a[r],self.a[i]=self.a[i],self.a[r]
                self.heapify(r)
        if(l<len(self.a)):
            if(self.a[l].p>self.a[i].p):
                self.a[l],self.a[i]=self.a[i],self.a[l]
                self.heapify(l)

    def BuildMaxHeap(self):
        for i in range((len(self.a)//2)-1,-1,-1):
            self.heapify(i)
    
    def ExtractMax(self):
        ans=self.a[0]
        last=len(self.a)-1
        self.a[0],self.a[last]=self.a[last],self.a[0]
        self.a.pop()
        self.heapify(0)
        return ans
    
    def Max(self):
        return self.a[0]
    
    def Empty(self):
        return len(self.a)==0

"""
chain class creates an object for a partial chain and associates it with a priority.
Example:{["Lion","Earth"],50} are data members value of a chain object. Here ["Lion","Earth"] has priority=50
"""
class chain:
    def __init__(self):
        self.a=[]
        self.p=0
    def addtochain(self,v,pri):
        self.a.append(v)
        self.p=pri
    def copy(self,fr,new,pri):
        for i in fr.a:
            self.a.append(i)
        self.a.append(new)
        self.p=pri

#links store all urls of a wiki page. HTMLParser parses the webpage and stores hyperlinks in links[] list.
links = []
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
           for name, url in attrs:
               if name == "href":
                   url = str(url)
                   if ("#" not in url) and (":" not in url):
                        val = url.split("/")
                        if("wiki" in val):
                            if val[-1] and (val[-1] not in links) and (val[-1]!= "Main_Page") and (val[-1]!="Terms_of_Use") and (val[-1]!= "Privacy_policy"):
                                a=val[-1].lower()
                                links.append(a)

#Wikilinks calls HTMLParser for a given name of Wiki page
def WikiLinks(name):
    parser = MyHTMLParser()
    myurl = "https://en.wikipedia.org/wiki/"+name
    response = urllib.request.urlopen(myurl)
    html = str(response.read())
    del links[:]
    parser.feed(html)

#Count function counts the identical links between start page and target page.
def count(start,target):
    count=0
    WikiLinks(start)
    one=[]
    for i in links:
        one.append(i)
    WikiLinks(target)
    two=[]
    for i in links:
        two.append(i)
    for i in one:
        if i in two:
            count=count+1
    #print(count)
    return count   


#findanswer function recursively calls itself untill it finds target page
"""
It extracts the highest priority partial chain from priority queue, 
finds the last wiki page in the partial chain, 
then finds all the links in it, 
then adds each link as a partial chain to same priority queue with a priority(equal to count(eachlink,target))
"""
def findanswer(p,target):
    m=p.ExtractMax()
    #print(m.a)
    try:
        WikiLinks(m.a[-1])
        if target in links:
            m.a.append(target)
            return m.a
        for i in links:
            #print(i)
            ob=chain()
            c=count(i,target)
            ob.copy(m,i,c)
            p.insert(ob)
    except:
        pass
    return findanswer(p,target)

def WikiChain(start,target):
    start=start.lower()
    target=target.lower()
    if start ==target:
        return "same values"
    o=chain()
    c=count(start,target)
    o.addtochain(start,c)
    p=PriorityQ(chain,[o])
    return findanswer(p,target)


answer=WikiChain("Lion","Moon")
print(answer)