# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import httplib
from xml.dom import minidom

class Search:
    _baseurl = "http://www.rai.tv"
    _nothumb = "http://www.rai.tv/dl/RaiTV/2012/images/NoAnteprimaItem.png"
    
    newsArchives = {"TG1": "BlockOB:PublishingBlock-3ad79a68-d0b8-4d12-b28c-7f48f8b3c84a",
        "TG2": "BlockOB:PublishingBlock-bce157a4-97de-49cd-8948-949a614e4b7d",
        "TG3": "BlockOB:PublishingBlock-401c09cd-050c-4816-b409-4b73be03a3bb"}
    
    newsProviders = {"TG1": "Tematica:TG1",
        "TG2": "Tematica:TG2",
        "TG3": "Tematica:TG3",
        "Rai News": "Tematica:Rai News",
        "Rai Sport": "Tematica:spt",
        "Rai Parlamento": "PageOB:Page-f3f817b3-1d55-4e99-8c36-464cea859189"}

    tematiche = ["Attualit�", "Bianco e Nero", "Cinema", "Comici", "Cronaca", "Cucina", "Cultura", "Cultura e Spettacoli", "Economia", "Fiction",
        "Hi tech", "Inchieste", "Incontra", "Interviste", "Istituzioni", "Junior", "Moda", "Musica", "News", "Politica", "Promo", "Reality",
        "Salute", "Satira", "Scienza", "Societ�", "Spettacolo", "Sport", "Storia", "Telefilm", "Tempo libero", "Viaggi"]

    def getLastContentByTag(self, tags="", numContents=16, mediaType="Video"):
        # type = "Video"
        # type = "Audio"
        tags = urllib.quote(tags)
        domain = "RaiTv"
                
        url = "http://www.rai.tv/StatisticheProxy/proxyPost.jsp?action=getLastContentByTag&numContents=%s&type=%s&tags=%s&domain=%s" % \
              (str(numContents), mediaType, tags, domain)
        xmldata = urllib2.urlopen(url).read().lstrip()
        dom = minidom.parseString(xmldata)
 
        return self.parseResponse(dom)
    
    
    def getMostVisited(self, tags, days=7, numContents=16, mediaType="Video"):
        tags = urllib.quote(tags)
        domain = "RaiTv"
        
        url = "http://www.rai.tv/StatisticheProxy/proxyPost.jsp?action=mostVisited&days=%s&state=1&records=%s&type=%s&tags=%s&domain=%s" % \
            (str(days), str(numContents), mediaType, tags, domain)
        xmldata = urllib2.urlopen(url).read().lstrip()
        dom = minidom.parseString(xmldata)    
        
        return self.parseResponse(dom)

        
    def parseResponse(self, dom):
        items = []
        
        for node in dom.getElementsByTagName('content'):
            item = {}
            item["title"] = node.getElementsByTagName('titolo')[0].childNodes[0].data
            item["date"] = node.getElementsByTagName('datapubblicazione')[0].childNodes[0].data.replace("/",".")
            descNode = node.getElementsByTagName('descrizione')
            if descNode.length > 0: 
                item["plotoutline"] = descNode[0].childNodes[0].data
            else:
                item["plotoutline"] = ""
            thumbNode = node.getElementsByTagName('pathImmagine')
            if thumbNode.length > 0:
                item["thumb"] = self._baseurl + thumbNode[0].childNodes[0].data
                # Get bigger thumbnail
                # Available sizes: /69x52, /105x79, /264x196, /433x325, /
                item["thumb"] = item["thumb"].replace("/105x79","/264x196")
            else:
                item["thumb"] = self._nothumb
            # Video URL only!!
            urlNode =  node.getElementsByTagName('h264')
            if urlNode.length > 0:
                item["url"] = urlNode[0].childNodes[0].data
            else:
                # No Video URL!!!
                # TODO: Handle <web> tag
                continue
            
            item["tvshowtitle"] = ""
            for tag in node.getElementsByTagName('tag'):
                if tag.childNodes[0].data[:13] == "NomeProgramma":
                    item["tvshowtitle"] = tag.childNodes[0].data[14:]
                    break

            items.append(item)

        return items


#search = Search()
#for tematica in search.tematiche:
#    print tematica
# Cinema
#print search.getLastContentByTag("Tematica:"+search.tematiche[2])
#for k, v in search.newsProviders.iteritems():
#    print k, "->", v
#print search.getLastContentByTag(search.newsProviders["Rai Parlamento"])
