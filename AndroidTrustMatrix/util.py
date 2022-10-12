import sys
import importlib
import AndroidTrustMatrix.config as Config
import requests
from AndroidTrustMatrix.Downloader import Plain_Get
from bs4 import BeautifulSoup
import TOR.tor



def eprint(*args, **kwargs):
    """Wrapper over print to write to stderr"""
    print(*args, file=sys.stderr, **kwargs)

def ImportModule(Market):
    """Dynamically import market modules"""
    # print(f"Loading Module mkt_{Market}")
    marketstring = Market.__str__().strip().replace(" ","")
    importstr = f"AndroidTrustMatrix.Tests.Markets.mkt_{marketstring}"
    try:
        module = importlib.import_module(importstr)
        return module
    except:
        eprint(f"Unable to import {importstr}")
    return None

class AndroidXMLDecompress():
    endDocTag = 0x00100101
    startTag = 0x00100102
    endTag = 0x00100103

    def decompressXML(self, xml: bytearray) -> str:
        
        finalXml = str()
        
        numbStrings = self.LEW(xml, 4*4)
        
        sitOff = 0x24
        stOff = sitOff + numbStrings * 4
        xmlTagOff = self.LEW(xml, 3 * 4)
        for i in range(xmlTagOff, len(xml) - 4, 4):
            if self.LEW(xml, i) == self.startTag:
                xmlTagOff = i
                break
        
        off = xmlTagOff
        
        while (off < len(xml)):
            tag0 = self.LEW(xml, off)
            nameSi = self.LEW(xml, off + 5 * 4)

            if tag0 == self.startTag:
                numbAttrs = self.LEW(xml, off + 7*4)
                off += 9*4
                name = self.compXmlString(xml, sitOff, stOff, nameSi)
                sb = str()
                for i in range(numbAttrs):
                    attrNameSi      = self.LEW(xml, off +   1 * 4 )
                    attrValueSi     = self.LEW(xml, off +   2 * 4 )
                    attrResId       = self.LEW(xml, off +   4 * 4 )

                    off += 5*4

                    attrName = self.compXmlString(xml,sitOff,stOff,attrNameSi)
                    attrValue = str()
                    if not attrValueSi == -1:
                        attrValue = self.compXmlString(xml, sitOff, stOff, attrValueSi)
                    else:
                        attrValue = "resourceID " + hex(attrResId) 
                    sb += " " + attrName + "=\"" + attrValue + "\""
                finalXml += "<" + name + sb + ">"
            elif tag0 == self.endTag:
                off += 6*4
                name = self.compXmlString(xml, sitOff, stOff, nameSi)
                finalXml += "</" + name + ">"
            elif tag0 == self.endDocTag:
                        break
            else:
                break
        return finalXml


    def compXmlString(self, xml: bytearray, sitOff: int, stOff: int, strInd: int) -> str:
        if strInd < 0:
            return None
        strOff = stOff + self.LEW(xml, sitOff + strInd*4)
        return self.compXmlStringAt(xml, strOff)

    def compXmlStringAt(self, arr: bytearray, strOff: bytearray) -> str:
        strlen = arr[strOff + 1] << 8 & 0xff00 | arr[strOff] & 0xff
        chars = bytearray()
        for i in range(strlen):
            if((strOff + 2 + i*2) < len(arr)):
                chars.append(arr[strOff + 2 + i*2])
        return chars.decode("utf-8",'backslashreplace')

    def LEW(self, arr: bytearray, off: int) -> int:
        c = arr[off + 3] << 24 & 0xff000000 | arr[off + 2] << 16 & 0xff0000 | arr[off + 1] << 8 & 0xff00 | arr[off] & 0xFF
        if c < -2147483648 or c > 2147483647:
            return int(-1)
        return c

def CheckVT(sha256sum):
        """Checks filehash on VirusTotal, if not seen return None, otherwise return detections"""
        url = f"https://virustotal.com/old-browsers/file/{sha256sum}"
        # Common User agent to hide web scraping
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        request_worked = False
        proxies = Config.get_proxy_config()
        response = Plain_Get(url,headers=headers)
        print(response)
        while request_worked == False:
            # Working Request
            if response.status_code == requests.status_codes.codes.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                detections = soup.find(id="detections")
                total = int(detections.get_text().strip().split("/")[0])
                request_worked = True
            # Request blocked by IP
            elif response.status_code == 403:
                print("VT: Forbidden")
                TOR.tor.main()
            # Item not found
            else:
                #print("VT: Unknown")
                return None

        threshold = 3
        if total > threshold:
            return True
        else:
            return False