'''
MIT License

Copyright (c) 2019-present Paiboon Kupthanakorn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#Fifo
# Version 2
# 2020-02-27 1. binascii
# Version 1
# 2020-02-27 1. init

import binascii

__code_version = 'mtcce.v1'

__autoSpeedforceIO = 5 #5km/h

Sampledat = [
    '$$126,867688039948074,15,A01,14|8.2,190626083616,A,13.904353,100.529748,0,44,135,0,2828,4000008A,02,0,520|5|430|13444E0,9F2|D6|6|3,,*28',
    '$$117,868998030242818,220,A01,,181112133629,A,13.904270,100.529836,0,179,2,0,0,0000,02,0,520|3|2337|28CA3B0,1A7|4DE|0|0,1,*04',    
    '$$119,868998030242818,221,A01,,181112133650,A,13.904270,100.529836,0,182,-12,0,0,0000,02,0,520|3|2337|28CA3B0,1A7|4E4|0|0,1,*6D',
    '$$o207,868998031044130,AAA,35,14.180526,100.597311,181113022225,A,12,8,0,274,0.8,0,1979805,3691944,520|15|17F3|011329E7,0000,0052|0000|0000|018C|0961,00000001,0|0|0|0,108,0000,,3,0,,0|0000|0000|0000|0000|0000*3F',
    '$$p207,868998031044130,AAA,35,14.180526,100.597311,181113022315,A,12,9,0,274,0.8,0,1979805,3691994,520|15|17F3|01132F0B,0000,0052|0000|0000|018D|0962,00000001,0|0|0|0,108,0000,,3,0,,0|0000|0000|0000|0000|0000*4B',
    '$$263,863835029419947,29,A01,,170705072751,A,22.621798,114.036116,57,0,126,1627,404,80000000,02,0,460|0|24A4|F82,13C|0,%^SUKSAWADDEE$SAITHARN$MISS^^?;6007643100500157891=150619800909=?+24 2 0004552 00100 ?,*4E',
    '\x24\x24\x50\x31\x30\x36\x34\x2C\x38\x36\x31\x35\x38\x35\x30\x34\x30\x34\x39\x34\x34\x36\x38\x2C\x43\x43\x45\x2C\x19\x00\x00\x00\x0C\x00\x54\x00\x15\x00\x05\x05\x01\x06\x0A\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x07\x00\x0B\x26\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xD7\x87\x57\x01\x03\x48\x60\xCC\x06\x04\xDE\xBF\xB5\x24\x0C80\x68\x00\x00\x0D\xE4\xA0\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x09\x00\x0B\x27\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xD0\x87\x57\x01\x03\x41\x60\xCC\x06\x04\xE8\xBF\xB5\x24\x0C\x80\x68\x00\x00\x0D\xEE\xA0\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x0B\x00\x0B\x27\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xCF\x87\x57\x01\x03\x3E\x60\xCC\x06\x04\xF2\xBF\xB5\x24\x0C\x80\x68\x00\x00\x0D\xF8\xA0\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x0A\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x08\x00\x0B\x27\x00\x16\x00\x00\x17\x00\x00\x19\xA3\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xD4\x87\x57\x01\x03\x43\x60\xCC\x06\x04\xFC\xBF\xB5\x24\x0C\x80\x68\x00\x00\x0D\x02\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x0A\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x07\x00\x0B\x25\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xDA\x87\x57\x01\x03\x3E\x60\xCC\x06\x04\x06\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x0B\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x0A\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x08\x00\x0B\x24\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xDF\x87\x57\x01\x03\x2F\x60\xCC\x06\x04\x10\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x15\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x08\x00\x0B\x22\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xE9\x87\x57\x01\x03\x14\x60\xCC\x06\x04\x1A\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x1F\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x08\x00\x0B\x21\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xEE\x87\x57\x01\x03\x0E\x60\xCC\x06\x04\x24\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x29\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x08\x00\x0B\x21\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xE9\x87\x57\x01\x03\x16\x60\xCC\x06\x04\x2E\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x33\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x09\x00\x0B\x23\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xE6\x87\x57\x01\x03\xFF\x5F\xCC\x06\x04\x39\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x3D\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x09\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x1F\x01\x0A\x09\x00\x0B\x23\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xE8\x87\x57\x01\x03\xE7\x5F\xCC\x06\x04\x43\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x46\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x54\x00\x15\x00\x05\x05\x01\x06\x0A\x07\x00\x14\x00\x15\x02\x09\x08\x00\x00\x09\x17\x01\x0A\x08\x00\x0B\x23\x00\x16\x00\x00\x17\x00\x00\x19\xA2\x01\x1A\x26\x05\x40\x23\x00\x06\x02\xE8\x87\x57\x01\x03\xD7\x5F\xCC\x06\x04\x4D\xC0\xB5\x24\x0C\x80\x68\x00\x00\x0D\x50\xA1\x03\x00\x1C\x01\x00\x00\x00\x01\x49\x09\x04\x01\x00\x00\x00\x00\x00\x00\x00\x2A\x32\x30\x0D\x0A'
    ]
       
    
Samplecmd = [
    '$$k28,864507030181266,B25,60*1B',
    '@@k28,864507030181266,B25,60*1B',
    '@@z25,864507030181266,E91*9B\r\n',
    '@@\60,864507030181266,C50,22,23,24,0,0,0,0,0,0,0,0,0,0,0,0,0*D4',
    '@@a31,868998030242818,C07,*102#*99', #This Fifo USSD for Dtac '*102#'
    '@@G25,864507030181266,B70*62']


def proto2msg(datin,_verbose=False):
    
    _this_limit_for_numpkg = 100
    
    datret =""
    if _verbose:
        print(__code_version)
        print(datin)

    if len(datin) >0 :
        rawhex = str(binascii.hexlify(datin)).upper()
        rawhex = rawhex.replace('B\'', '')
        rawhex = rawhex.replace('b\'', '')
        rawhex = rawhex.replace('\'', '')
    
    else:
        return 0

    if _verbose:
        print('>>len(rawhex)',len(rawhex))
        print('>>rawhex')
        print(rawhex)

    # $$<Data identifier 1-char><Data length 3-char>,<IMEI 15-char>,<Command type 3-char aka,CCE>,
    _header1 = rawhex[:28*2] # 28-byte first
    _header1 = str(binascii.unhexlify(_header1))
    _header1 = _header1.replace('B\'', '')
    _header1 = _header1.replace('b\'', '')
    _header1 = _header1.replace('\'', '')
    
    if not ('$$' in _header1) :
        return 0
    
    if not (',CCE,' in _header1) :
        return 0
    
    _header_indentifier = str(_header1[2:(2+1)])
    _header_intdatalen = int(_header1[3:(3+4)])
    _tmp = _header1.split(',')
    _header_imei = _tmp[1]
    _header_cmdtype = _tmp[2]
    
    
    
    if _verbose:
        print('>>Header-1')
        print(_header1)
        print(_header_indentifier)
        print(_header_intdatalen)
        print(_header_imei)
        print(_header_cmdtype)
    
    # Test
    #a = '\x19\x00\x00\xF0'.encode()
    #print( int.from_bytes(a, 'little',signed=False))
    
    _hexRemainBuffer = rawhex[(28*2):((28+4)*2)] # 4-byte
    _intRemainBuffer = int.from_bytes(binascii.unhexlify(_hexRemainBuffer),'little',signed=False)
    _hexNumSmallPkg = rawhex[(32*2):((32+2)*2)] # 2-byte
    _intNumSmallPkg = int.from_bytes(binascii.unhexlify(_hexNumSmallPkg),'little',signed=False)



    
    
    if _verbose:
        print('>>Header-2_intRemainBuffer')
        print(_hexRemainBuffer)
        print(_intRemainBuffer)
        print('>>Header-2_intNumSmallPkg')
        print(_hexNumSmallPkg)
        print(_intNumSmallPkg)
   

    fullcontainhex = rawhex[(34*2):]
    remaincontainhex = fullcontainhex

    if _verbose:
        print('>>containhex')
        print(fullcontainhex)
        print('>>Loop for _intNumSmallPkg:')
        print(_intNumSmallPkg)
    
    if _intNumSmallPkg >  _this_limit_for_numpkg:
        return 0
    
    #for x in range(12):
    #  print(x)

    for x in range(_intNumSmallPkg):           
        _hexDataPkgLen = remaincontainhex[(0*2):((0+2)*2)] # 2-byte
        _intDataPkgLen = int.from_bytes(binascii.unhexlify(_hexDataPkgLen),'little',signed=False)
        _hexNumDataPkgID = remaincontainhex[(2*2):((2+2)*2)] # 2-byte
        _intNumDataPkgID = int.from_bytes(binascii.unhexlify(_hexNumDataPkgID),'little',signed=False)
        
        a_constance = 11
        partialhex = remaincontainhex[0:(_intDataPkgLen+a_constance+1)*2]
        remaincontainhex = remaincontainhex[(_intDataPkgLen+a_constance+1)*2:]
        if _verbose:
            print('x',x)
            print('>>Header-2_intDataPkgLen',_hexDataPkgLen,_intDataPkgLen)
            print('>>Header-2_intNumDataPkgID',_hexNumDataPkgID,_intNumDataPkgID)
            print('>>Header-2_len(partialhex)',len(partialhex))
            print(partialhex)
            print('>>Header-2_len(remaincontainhex)',len(remaincontainhex))
            print(remaincontainhex)

    
    

        
        
    
    postdat = datin
    
    if _verbose:
        print(postdat)
        
    datret = postdat
    return datret


def cmd2proto(datin,_verbose=False):
    datret =""
    if _verbose:
        print(__code_version)
        print(datin)
        
    postdat = datin
    
    if _verbose:
        print(postdat)
            
    datret = postdat
    return datret
        

def main():
    print("main program")
       
    proto2msg("SSS".encode())
    proto2msg("CCC".encode(),_verbose=True)
    
    for (i, dat) in enumerate(Sampledat):
        proto2msg(dat.encode(),_verbose=True)
        
 
    cmd2proto("SSS")
    cmd2proto("CCC",_verbose=True)
    
    for (i, dat) in enumerate(Samplecmd):
        cmd2proto(dat,_verbose=True)

if __name__=='__main__':
    main()


'''


'''
