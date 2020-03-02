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

#MT CCE
# Version 3
# 2020-03-01 1. JSON Practice
# Version 2
# 2020-02-27 1. binascii
# Version 1
# 2020-02-27 1. init

import datetime
import binascii
import json
import uuid

__code_version = 'mtcce.v3'

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
       
Sampledathex = [
    '3132332C',
    '242450313036342C3836313538353034303439343436382C4343452C190000000C0054001500050501060A07001400150209080000091F010A07000B260016000017000019A2011A26054023000602D7875701034860CC0604DEBFB5240C806800000DE4A003001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B270016000017000019A2011A26054023000602D0875701034160CC0604E8BFB5240C806800000DEEA003001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A0B000B270016000017000019A2011A26054023000602CF875701033E60CC0604F2BFB5240C806800000DF8A003001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A08000B270016000017000019A3011A26054023000602D4875701034360CC0604FCBFB5240C806800000D02A103001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A07000B250016000017000019A2011A26054023000602DA875701033E60CC060406C0B5240C806800000D0BA103001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A08000B240016000017000019A2011A26054023000602DF875701032F60CC060410C0B5240C806800000D15A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B220016000017000019A2011A26054023000602E9875701031460CC06041AC0B5240C806800000D1FA103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B210016000017000019A2011A26054023000602EE875701030E60CC060424C0B5240C806800000D29A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B210016000017000019A2011A26054023000602E9875701031660CC06042EC0B5240C806800000D33A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B230016000017000019A2011A26054023000602E687570103FF5FCC060439C0B5240C806800000D3DA103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B230016000017000019A2011A26054023000602E887570103E75FCC060443C0B5240C806800000D46A103001C0100000001490904010000000000000054001500050501060A070014001502090800000917010A08000B230016000017000019A2011A26054023000602E887570103D75FCC06044DC0B5240C806800000D50A103001C010000000149090401000000000000002A32300D0A'
    ]

    
Samplecmd = [
    '$$k28,864507030181266,B25,60*1B',
    #'@@k28,864507030181266,B25,60*1B',
    #'@@z25,864507030181266,E91*9B\r\n',
    #'@@\60,864507030181266,C50,22,23,24,0,0,0,0,0,0,0,0,0,0,0,0,0*D4',
    #'@@a31,868998030242818,C07,*102#*99', #This Fifo USSD for Dtac '*102#'
    '@@G25,864507030181266,B70*62']


def proto2msg(datin,_verbose=False):
    
    _this_limit_for_numpkg = 100
    
    datret =""
    if _verbose:
        print(__code_version)

    if len(datin) >32 :
        rawhex = str(binascii.hexlify(datin)).upper()
        rawhex = rawhex.replace('B\'', '')
        rawhex = rawhex.replace('b\'', '')
        rawhex = rawhex.replace('\'', '')
    else:
        return 0

    if _verbose:
        print('>>len(datin)',len(datin))
        print(datin)
        print('>>len(rawhex)',len(rawhex))
        print('>>rawhex')
        print(rawhex)

    # $$<Data identifier 1-char><Data length 3-char>,<IMEI 15-char>,<Command type 3-char aka,CCE>,
    _header1 = rawhex[:28*2] # 28-byte first
    _header1 = str(binascii.unhexlify(_header1))
    _header1 = _header1.replace('B\'', '')
    _header1 = _header1.replace('b\'', '')
    _header1 = _header1.replace('\'', '')
    
    # \r\n
    _tail1hex = rawhex[len(rawhex)-(2*2):] # Last 2byte

    
    if not ('$$' in _header1) :
        return 0
    
    if not (',CCE,' in _header1) :
        return 0

    if not ('0D0A' in _tail1hex.upper()) :
        return 0
    
    _header_indentifier = str(_header1[2:(2+1)])
    _header_intdatalen = int(_header1[3:(3+4)])
    _tmp = _header1.split(',')
    _header_imei = _tmp[1]
    _header_cmdtype = _tmp[2]
    
    #msg1='{"country abbreviation":"US","places":[{"place name":"Belmont","longitude":"-71.4594","post code":"02178","latitude":"42.4464"},{"place name":"Belmont","longitude":"-71.2044","post code":"02478","latitude":"42.4128"}],"country":"United States","place name":"Belmont","state":"Massachusetts","state abbreviation":"MA"}'
    msg1='{"__VERSION__":"0.8"}'
    _js = json.loads(msg1)
    _js['ts_cjob'] = '{}'.format(datetime.datetime.utcnow())
    
    _js['__UUID__'] = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.utcnow()))) # uuid5 + time utc

    _js['h1_rawhex'] = _header1
    _js['h1_datalen'] = str(_header_intdatalen)
    _js['h1_pid'] = _header_indentifier
    _js['h1_imei'] = _header_imei
    _js['h1_cmdtype'] = _header_cmdtype

    
    if _verbose:
        print('>>Header-1')
        print(_header1)
        print(_header_indentifier)
        print(_header_intdatalen)
        print(_header_imei)
        print(_header_cmdtype)
        
        print('>>_Tail-1-hex')
        print(_tail1hex)
        
        print(json.dumps(_js, indent=4, sort_keys=True))
    
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

    _js['h2_remaincache'] = str(_intRemainBuffer)
    _js['h2_numsmallpkg'] = str(_intNumSmallPkg)
    
    #for x in range(12):
    #  print(x)
    _js['b'] = {} # init nest dict
    for x in range(_intNumSmallPkg):           
        _hexDataPkgLen = remaincontainhex[(0*2):((0+2)*2)] # 2-byte
        _intDataPkgLen = int.from_bytes(binascii.unhexlify(_hexDataPkgLen),'little',signed=False)
        _hexNumDataPkgID = remaincontainhex[(2*2):((2+2)*2)] # 2-byte
        _intNumDataPkgID = int.from_bytes(binascii.unhexlify(_hexNumDataPkgID),'little',signed=False)
        
        partialhex = remaincontainhex[0:(_intDataPkgLen+1)*2]
        remaincontainhex = remaincontainhex[(_intDataPkgLen+2)*2:]
        
        _jskey = 'pkg_{:02d}'.format(x)
        _js['b'][_jskey] = {} # init nest dict

        _js['b'][_jskey]['s_pkg_datalen'] = str(_intDataPkgLen)
        _js['b'][_jskey]['s_pkg_numdatapkg'] = str(_intNumDataPkgID)
        _js['b'][_jskey]['s_pkg_partialhexlen'] = str(len(partialhex))
        _js['b'][_jskey]['s_pkg_partialhex'] = partialhex
        _js['b'][_jskey]['s_pkg_remaincontainhexlen'] = str(len(remaincontainhex))
                
        if _verbose:
            print('x',x)
            print('>>Small-Pkg_intDataPkgLen',_hexDataPkgLen,_intDataPkgLen)
            print('>>Small-Pkg_intNumDataPkgID',_hexNumDataPkgID,_intNumDataPkgID)
            print('>>Small-Pkg_len(partialhex)',len(partialhex))
            print(partialhex)
            print('>>Small-Pkg_len(remaincontainhex)',len(remaincontainhex))
            print(remaincontainhex)
        
        #0-loop
        remainxbytehex = partialhex[4*2:]
        
        xbytehex = remainxbytehex
        
        _hexNum1byteID = xbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNum1byteID = int.from_bytes(binascii.unhexlify(_hexNum1byteID),'little',signed=False)

        _js['b'][_jskey]['c1b'] = {} # init nest dict
        for _x in range(_intNum1byteID):
            _y= 1 + (_x*2)
            _xidhex =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+1)*2)] # 1-byte
                        
            _jsy = 'x_{:02d}'.format(_x)
            _js['b'][_jskey]['c1b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['c1b'][_jsy]['idhex'] = _xidhex
            _js['b'][_jskey]['c1b'][_jsy]['dahex'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',_xidhex,_xidhex)
                print('>>x-byte__xrawhex',_xrawhex,_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum1byteID*2))*2:]
        if _verbose:
            print('>>x-byte_hexNum1byteID',_hexNum1byteID,_hexNum1byteID)
            print('>>x-byte_intNum1byteID',_intNum1byteID,_intNum1byteID)
            print('>>x-byte_len(xbytehex)',len(xbytehex))
            print(xbytehex)
            print('>>x-byte_len(remainxbytehex)',len(remainxbytehex))
            print(remainxbytehex)
        
        xbytehex = remainxbytehex
        
        _hexNum2byteID = xbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNum2byteID = int.from_bytes(binascii.unhexlify(_hexNum2byteID),'little',signed=False)
        
        _js['b'][_jskey]['c2b'] = {} # init nest dict
        for _x in range(_intNum2byteID):
            _y= 1 + (_x*3)
            _xidhex =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+2)*2)] # 2-byte
            
            _jsy = 'x_{:02d}'.format(_x)
            _js['b'][_jskey]['c2b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['c2b'][_jsy]['idhex'] = _xidhex
            _js['b'][_jskey]['c2b'][_jsy]['dahex'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',_xidhex,_xidhex)
                print('>>x-byte__xrawhex',_xrawhex,_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum2byteID*3))*2:]
        if _verbose:
            print('>>x-byte_hexNum2byteID',_hexNum2byteID,_hexNum2byteID)
            print('>>x-byte_intNum2byteID',_intNum2byteID,_intNum2byteID)
            print('>>x-byte_len(xbytehex)',len(xbytehex))
            print(xbytehex)
            print('>>x-byte_len(remainxbytehex)',len(remainxbytehex))
            print(remainxbytehex)
        
        xbytehex = remainxbytehex
        
        _hexNum4byteID = xbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNum4byteID = int.from_bytes(binascii.unhexlify(_hexNum4byteID),'little',signed=False)
        
        _js['b'][_jskey]['c4b'] = {} # init nest dict
        for _x in range(_intNum4byteID):
            _y= 1 + (_x*5)
            _xidhex =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+4)*2)] # 4-byte
            
            _jsy = 'x_{:02d}'.format(_x)
            _js['b'][_jskey]['c4b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['c4b'][_jsy]['idhex'] = _xidhex
            _js['b'][_jskey]['c4b'][_jsy]['dahex'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',_xidhex,_xidhex)
                print('>>x-byte__xrawhex',_xrawhex,_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum4byteID*5))*2:]
        if _verbose:
            print('>>x-byte_hexNum4byteID',_hexNum4byteID,_hexNum4byteID)
            print('>>x-byte_intNum4byteID',_intNum4byteID,_intNum4byteID)
            print('>>x-byte_len(xbytehex)',len(xbytehex))
            print(xbytehex)
            print('>>x-byte_len(remainxbytehex)',len(remainxbytehex))
            print(remainxbytehex)        
        

        _hexNumNBytePkg =  remainxbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNumNBytePkg = int.from_bytes(binascii.unhexlify(_hexNumNBytePkg),'little',signed=False)
        
        if _verbose:
            print('>>Header-3_intNumNBytePkg')
            print(_hexNumNBytePkg)
            print(_intNumNBytePkg)
       

        if _verbose:
            print('>>Nbyte_remainxbytehex')
            print(remainxbytehex)
            print('>>Nbyte_Loop for _intNumNBytePkg:')
            print(_intNumNBytePkg)
        
        if _intNumNBytePkg >  _this_limit_for_numpkg:
            return 0
        
        #for x in range(12):
        #  print(x)
        
        _js['b'][_jskey]['nb'] = {} # init nest dict
        _js['b'][_jskey]['nb']['numnbytepkg'] = str(_intNumNBytePkg)
        
        for _x in range(_intNumNBytePkg):
            
            xbytehex = remainxbytehex
            
            _xidhex =  xbytehex[(1*2):((1+1)*2)] # 1-byte
            
            _hexNumNbyteID = xbytehex[(2*2):((2+1)*2)] # 1-byte
            _intNumNbyteID = int.from_bytes(binascii.unhexlify(_hexNumNbyteID),'little',signed=False)
            
            _y= 3
            _xrawhex = xbytehex[(_y*2):((_y+_intNumNbyteID)*2)] # N-byte
            
            remainxbytehex = xbytehex[(_y+_intNumNbyteID-1)*2:] # Need RAW TCP Checking Nbyte..Nbyte-1....Nbyte-2

            _jsy = 'x_{:02d}'.format(_x)
            _js['b'][_jskey]['nb'][_jsy] = {} # init nest dict
            _js['b'][_jskey]['nb'][_jsy]['nlen'] = str(_intNumNbyteID)
            _js['b'][_jskey]['nb'][_jsy]['idhex'] = _xidhex
            _js['b'][_jskey]['nb'][_jsy]['dahex'] = _xrawhex

            
            if _verbose:
                print('>>x-byte_hexNumNbyteID',_hexNumNbyteID,_hexNumNbyteID)
                print('>>x-byte_intNumNbyteID',_intNumNbyteID,_intNumNbyteID)
                print('>>x-byte__len(xrawhex)',len(_xrawhex),len(_xrawhex))
                print('>>x-byte__xidhex',_xidhex,_xidhex)
                print('>>x-byte__xrawhex',_xrawhex,_xrawhex)
                print('>>x-byte_len(xbytehex)',len(xbytehex))
                print(xbytehex)
                print('>>x-byte_len(remainxbytehex)',len(remainxbytehex))
                print(remainxbytehex)

    # Last func
    _js['in_rawhex'] = rawhex
    _js['in_rawhex_sz'] = str(int(len(rawhex)/2))
    _js['ts_ejob'] = '{}'.format(datetime.datetime.utcnow())
    if _verbose:       
        print(json.dumps(_js, indent=4, sort_keys=True))
        
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
    
    for (i, dat) in enumerate(Sampledathex):
        print(i)
        proto2msg(binascii.unhexlify(dat),_verbose=True)
        
 
    cmd2proto("SSS")
    cmd2proto("CCC",_verbose=True)
    
    for (i, dat) in enumerate(Samplecmd):
        print(i)
        cmd2proto(dat,_verbose=True)

if __name__=='__main__':
    main()


'''
A nested dict is a dictionary within a dictionary. A very simple thing.

>>> d = {}
>>> d['dict1'] = {} # must: init nest dict
>>> d['dict1']['innerkey'] = 'value'
>>> d
{'dict1': {'innerkey': 'value'}}


# https://jsoneditoronline.org/#left=local.xowame&right=local.wilija

import json

msg1='{"country abbreviation":"US","places":[{"place name":"Belmont","longitude":"-71.4594","post code":"02178","latitude":"42.4464"},{"place name":"Belmont","longitude":"-71.2044","post code":"02478","latitude":"42.4128"}],"country":"United States","place name":"Belmont","state":"Massachusetts","state abbreviation":"MA"}'
print(msg1)

jobj1=json.loads(msg1)

print(len(jobj1))
print(jobj1)

print(jobj1['country abbreviation'])
print(jobj1['state abbreviation'])

print(len(jobj1['places']))
print(jobj1['places'])
print(jobj1['places'][0])
print(jobj1['places'][1])

print(len(jobj1['places'][0]))
print(jobj1['places'][0]['place name'])
print(jobj1['places'][0]['post code'])

for song in jobj1:
  print(song)

for note in jobj1['places']:
  print(note)

# For dict JSON

for (_k, _v) in jobj1.items():
  print("Key: " + _k)
  print("Value: " + str(_v))

for (_k, _v) in jobj1['places'][0].items():
  print("Key: " + _k)
  print("Value: " + str(_v))

#JSON Tree
print(json.dumps(jobj1, indent=4, sort_keys=True))

'''
