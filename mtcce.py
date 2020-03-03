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
# Version 4
# 2020-03-03 1. AAA <= CCE 2. mini decode verbose
# Version 3
# 2020-03-01 1. JSON Practice
# Version 2
# 2020-02-27 1. binascii
# Version 1
# 2020-02-27 1. init
import time
import datetime
import binascii
import json
import uuid

__code_version = 'mtcce.v4'

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

Samplejson = [
    '{"c1b":{"x_00":{"dahex":"01","idhex":"05"},"x_01":{"dahex":"0A","idhex":"06"},"x_02":{"dahex":"00","idhex":"07"},"x_03":{"dahex":"00","idhex":"14"},"x_04":{"dahex":"02","idhex":"15"}},"c2b":{"x_00":{"dahex":"0000","idhex":"08"},"x_01":{"dahex":"1F01","idhex":"09"},"x_02":{"dahex":"0700","idhex":"0A"},"x_03":{"dahex":"2600","idhex":"0B"},"x_04":{"dahex":"0000","idhex":"16"},"x_05":{"dahex":"0000","idhex":"17"},"x_06":{"dahex":"A201","idhex":"19"},"x_07":{"dahex":"2605","idhex":"1A"},"x_08":{"dahex":"2300","idhex":"40"}},"c4b":{"x_00":{"dahex":"D7875701","idhex":"02"},"x_01":{"dahex":"4860CC06","idhex":"03"},"x_02":{"dahex":"DEBFB524","idhex":"04"},"x_03":{"dahex":"80680000","idhex":"0C"},"x_04":{"dahex":"E4A00300","idhex":"0D"},"x_05":{"dahex":"01000000","idhex":"1C"}},"nb":{"numnbytepkg":"1","x_00":{"dahex":"0401000000000000","idhex":"49","nlen":"9"}},"s_pkg_datalen":"84","s_pkg_numdatapkg":"21","s_pkg_partialhex":"54001500050501060A07001400150209080000091F010A07000B260016000017000019A2011A26054023000602D7875701034860CC0604DEBFB5240C806800000DE4A003001C010000000149090401000000000000","s_pkg_partialhexlen":"170","s_pkg_remaincontainhexlen":"1902"}'
    ]
Samplecmd = [
    '$$k28,864507030181266,B25,60*1B',
    #'@@k28,864507030181266,B25,60*1B',
    #'@@z25,864507030181266,E91*9B\r\n',
    #'@@\60,864507030181266,C50,22,23,24,0,0,0,0,0,0,0,0,0,0,0,0,0*D4',
    #'@@a31,868998030242818,C07,*102#*99', #This Fifo USSD for Dtac '*102#'
    '@@G25,864507030181266,B70*62']


def decode(datin,_verbose=False):
    
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
        return ''

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
        return ''
    
    if not (',CCE,' in _header1) :
        return ''

    if not ('0D0A' in _tail1hex.upper()) :
        return ''
    
    _header_indentifier = str(_header1[2:(2+1)])
    _header_intdatalen = int(_header1[3:(3+4)])
    _tmp = _header1.split(',')
    _header_imei = _tmp[1]
    _header_cmdtype = _tmp[2]
    
    #msg1='{"country abbreviation":"US","places":[{"place name":"Belmont","longitude":"-71.4594","post code":"02178","latitude":"42.4464"},{"place name":"Belmont","longitude":"-71.2044","post code":"02478","latitude":"42.4128"}],"country":"United States","place name":"Belmont","state":"Massachusetts","state abbreviation":"MA"}'
    msg1='{"__TAG__":"raw"}'
    
    _js = json.loads(msg1)
    
    
    _js['ts_cjob'] = '{}'.format(datetime.datetime.utcnow())
    _js['__VERSION__'] = __code_version
    
    _js['__UUID__'] = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.utcnow()))) # uuid5 + time utc

    _js['h1_rawhex'] = _header1
    _js['h1_datalen'] = str(_header_intdatalen)
    _js['h1_pid'] = _header_indentifier
    _js['h1_imei'] = _header_imei
    _js['h1_cmdtype'] = _header_cmdtype

    
    if _verbose:
        print('>>Header-1')
        print('_header1', len(_header1), _header1)
        print('_header_indentifier', len(_header_indentifier), _header_indentifier)
        print('_header_intdatalen', _header_intdatalen, _header_intdatalen)
        print('_header_imei', len(_header_imei), _header_imei)
        print('_header_cmdtype', len(_header_cmdtype), _header_cmdtype)
        print('_tail1hex', len(_tail1hex), _tail1hex)
                
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
        print('_hexRemainBuffer', len(_hexRemainBuffer), _hexRemainBuffer)
        print('_intRemainBuffer', _intRemainBuffer, _intRemainBuffer)
        print('>>Header-2_intNumSmallPkg')
        print('_hexNumSmallPkg', len(_hexNumSmallPkg), _hexNumSmallPkg)
        print('_intNumSmallPkg', _intNumSmallPkg, _intNumSmallPkg)
   

    fullcontainhex = rawhex[(34*2):]
    remaincontainhex = fullcontainhex

    if _verbose:
        print('>>containhex')
        print(fullcontainhex)
        print('>>Loop for _intNumSmallPkg:')
        print(_intNumSmallPkg)
    
    if _intNumSmallPkg >  _this_limit_for_numpkg:
        return ''

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
        
        if len(remainxbytehex) > 3: # fix bug nbyte >3
            _hexNumNBytePkg =  remainxbytehex[(0*2):((0+1)*2)] # 1-byte
            _intNumNBytePkg = int.from_bytes(binascii.unhexlify(_hexNumNBytePkg),'little',signed=False)
        else: 
            _hexNumNBytePkg = '00'
            _intNumNBytePkg = len(_hexNumNBytePkg)
            
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
            return ''
        
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
    
    #_data = json.dumps(_js, indent=4, sort_keys=True)
    _data = json.dumps(_js, sort_keys=True)

    
    if _verbose:       
        print(json.dumps(_data, indent=4, sort_keys=True))
        
    postdat = _data
    
    if _verbose:
        print(postdat)
        
    datret = postdat
    return datret



def is_complex(objct):
    # use of json loads method with object_hook for check object complex or not
    if '__complex__' in objct:
        return complex(objct['real'], objct['img'])
    return objct

    

def pkgdecode(datin,_verbose=False):
    
    if _verbose: 
        print(len(datin))
    
    try:
        _js = json.loads(datin)
    except ValueError as e:
        print(e)
        print("JSON input error")
        return ''


    try:
        _objc1b = _js['c1b']
        _objc2b = _js['c2b']
        _objc4b = _js['c4b']
        _objnb = _js['nb']
    except KeyError as e:
        print(e)
        print("JSON Get Key 1 error")
        return ''
    
    if _verbose: 
        print('_objc1b', len(_objc1b) , _objc1b)
        print('_objc2b', len(_objc2b) , _objc2b)
        print('_objc4b', len(_objc4b) , _objc4b)
        print('_objnb', len(_objnb) , _objnb)
    
    
    # init var @ c1b
    _v_u8GpsValid = 0
    _v_u8GpsNsat = 0
    _v_u8GsmStr = 0
    _v_u8Output = 0
    _v_u8input = 0
    for _x in range(len(_objc1b)):
        _kx = 'x_{:02d}'.format(_x)
        _xidhex = _objc1b[_kx]['idhex']
        _xrawhex = _objc1b[_kx]['dahex']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xidhex) , _xidhex)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xidhex == '05':
            _v_u8GpsValid = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '06':
            _v_u8GpsNsat= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '07':
            _v_u8GsmStr= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '14':
            _v_u8Output= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '15':
            _v_u8input= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
            
    if _verbose:
        print('_v_u8GpsValid', _v_u8GpsValid)
        print('_v_u8GpsNsat', _v_u8GpsNsat)
        print('_v_u8GsmStr', _v_u8GsmStr)
        print('_v_u8Output', _v_u8Output)
        print('_v_u8input', _v_u8input)


    # init var @ c2b
    _v_u16SpeedKMH = 0
    _v_u16Heading = 0
    _v_f32Hdop = 0.0
    _v_u16Alt = 0
    _v_f32AD1 = 0.0
    _v_f32AD2 = 0.0
    _v_f32AD4 = 0.0
    _v_f32AD5 = 0.0
    _v_u16Eventcode = 0
    

    for _x in range(len(_objc2b)):
        _kx = 'x_{:02d}'.format(_x)
        _xidhex = _objc2b[_kx]['idhex']
        _xrawhex = _objc2b[_kx]['dahex']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xidhex) , _xidhex)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xidhex == '08':
            _v_u16SpeedKMH = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '09':
            _v_u16Heading= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '0A':
            _v_f32Hdop= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1
        elif _xidhex == '1B':
            _v_u16Alt= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '16':
            _v_f32AD1= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/100
        elif _xidhex == '17':
            _v_f32AD2= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/100
        elif _xidhex == '19':
            _v_f32AD4= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/100
        elif _xidhex == '1A':
            _v_f32AD5= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/100
        elif _xidhex == '40':
            _v_u16Eventcode= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
            
    if _verbose:
        print('_v_u16SpeedKMH', _v_u16SpeedKMH)
        print('_v_u16Heading', _v_u16Heading)
        print('_v_f32Hdop', _v_f32Hdop)
        print('_v_u16Alt', _v_u16Alt)
        print('_v_f32AD1', _v_f32AD1)
        print('_v_f32AD2', _v_f32AD2)
        print('_v_f32AD4', _v_f32AD4)
        print('_v_f32AD5', _v_f32AD5)
        print('_v_u16Eventcode', _v_u16Eventcode)   

    # init var @ c4b
    _v_f32Lt = 0.0
    _v_f32Ln = 0.0
    _v_u32TimeSecSince2000 = 0
    _v_strGpsUTCyymmddHHMMSS = ''
    _v_u32Mileage = 0
    _v_u32RunTimeSec = 0
    _v_u32SysFlags = 0
    
    for _x in range(len(_objc4b)):
        _kx = 'x_{:02d}'.format(_x)
        _xidhex = _objc4b[_kx]['idhex']
        _xrawhex = _objc4b[_kx]['dahex']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xidhex) , _xidhex)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xidhex == '02':
            _v_f32Lt = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1000000
        elif _xidhex == '03':
            _v_f32Ln= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1000000
        elif _xidhex == '04':
            _v_u32TimeSecSince2000= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
            
            _time = time.gmtime(_v_u32TimeSecSince2000 + 946684800) #615890910 + (Since2000), Where January 1, 2000 UNIX time is 946684800.
            _v_strGpsUTCyymmddHHMMSS = time.strftime("%y%m%d%H%M%S",_time)
            
        elif _xidhex == '0C':
            _v_u32Mileage = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '0D':
            _v_u32RunTimeSec = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xidhex == '1C':
            _v_u32SysFlags = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)           
            
    if _verbose:
        print('_v_f32Lt', _v_f32Lt)
        print('_v_f32Ln', _v_f32Ln)
        print('_v_u32TimeSecSince2000', _v_u32TimeSecSince2000)
        print('_v_strGpsUTCyymmddHHMMSS', _v_strGpsUTCyymmddHHMMSS)
        print('_v_u32Mileage', _v_u32Mileage)
        print('_v_u32RunTimeSec', _v_u32RunTimeSec)
        print('_v_u32SysFlags', _v_u32SysFlags)
    
    
    
    #Encode
    # _v_u8GpsValid 1
    # _v_u8GpsNsat 10
    # _v_u8GsmStr 0
    # _v_u8Output 0
    # _v_u8input 2

    # _v_u16SpeedKMH 0
    # _v_u16Heading 287
    # _v_f32Hdop 7.0
    # _v_u16Alt 0
    # _v_f32AD1 0.0
    # _v_f32AD2 0.0
    # _v_f32AD4 4.18
    # _v_f32AD5 13.18
    # _v_u16Eventcode 35

    # _v_f32Lt 22.513623
    # _v_f32Ln 114.057288
    # _v_u32TimeSecSince2000 615890910
    # _v_strGpsUTCyymmddHHMMSS 190708084830
    # _v_u32Mileage 26752
    # _v_u32RunTimeSec 237796
    # _v_u32SysFlags 1    
    _x_strImei = '868777888999130'
    _x_strDataID = 'P'
    
    
    _y_datalen = '99'
    _y_GpsValid = 'V'
    if _v_u8GpsValid !=0 :
        _y_GpsValid = 'A'
    
    _y_strBaseStationInfo = '520|15|17F3|01132F0B'    
    _y_iost = '1F1F'
    _y_adcnew = '1|2|3|4|5|6' # MUST > 5 ch
    _y_rfid = 'rfid'
    
    
    pt="$$"
       
    pt= pt + _x_strDataID + _y_datalen + ','+ _x_strImei + ',' + 'AAA' + ',' + str(_v_u16Eventcode) + ','    # $$<Data identifier><Data length><IMEI>AAA<Event code>
    pt= pt + str(_v_f32Lt)+','+ str(_v_f32Ln) + ',' + _v_strGpsUTCyymmddHHMMSS + ',' + _y_GpsValid + ','    # <Latitude><Longitude><Date and time><Positioning status>
    pt= pt + str(_v_u8GpsNsat) +',' + str(_v_u8GsmStr) +',' + str(_v_u16SpeedKMH) +',' + str(_v_u16Heading) +','    # <Number of satellites><GSM signal strength><Speed><Direction>
    pt= pt + str(_v_f32Hdop) +',' + str(_v_u16Alt) +',' + str(_v_u32Mileage) +',' + str(_v_u32RunTimeSec) +','    # <Horizontal dilution of precision(HDOP)><Altitude><Mileage><Total time>
    pt= pt + _y_strBaseStationInfo +',' + _y_iost +',' + _y_adcnew +',' + _y_rfid +','    # <Base station info><I/O port status><Analog input value><Assisted event info or RFID>
    pt= pt + 'alm'  +',' + '108' +',' + '0' +',' + '0' +','    # <Customized data><Extended protocol version 108><Fuel percentage><Temperature sensor No. + Temperature value>
    pt= pt + '0' +',' + '0' +',' + '0' +',' + '0' +','    # <Data N>
    pt= pt +'*FF\r\n' # <*Checksum>\r\n


    if _verbose:
        print(pt)
        
    datret = pt 
    return datret




def proto2msg(datin,_verbose=False):
    _data= str(decode(datin,_verbose=True))
    
    print(len(_data))
    
    try:
        _js = json.loads(_data)
    except ValueError as e:
        print(e)
        print("JSON input error")
        return ''
    
    try:
        _txt_uuid = _js
        print(_txt_uuid['__UUID__'])
    except KeyError as e:
        print(e)
        print("JSON Get Key 1 error")
        return ''
    
    #_js = json.loads(str(_data))
    
    if _verbose:       
        #print(json.dumps(_js, indent=4, sort_keys=True))
        print(json.dumps(_js, sort_keys=True))
    
    if not ( _js['h1_cmdtype'] == 'CCE'):
        return ''
    
    _b_obj= _js['b']

    
    
    if _verbose:       
        print('_b_obj', len(_b_obj), _b_obj)
        
    for _x in range(len(_b_obj)):
        _kx = 'pkg_{:02d}'.format(_x)
        
        _b_obj_c1b= _js['b'][_kx]['c1b']

    
        for _y in range(len(_b_obj_c1b)):
            _ky = 'x_{:02d}'.format(_y)
            _idhex = _js['b'][_kx]['c1b'][_ky]['idhex']
            _rawhex = _js['b'][_kx]['c1b'][_ky]['dahex']
            
            if _verbose:
                print('_b_obj_c1b', len(_b_obj_c1b), _b_obj_c1b)
                print('_kx', _kx)
                print('_ky', _ky)
                print('_idhex', _idhex)
                print('_rawhex', _rawhex)                
        
    datret = _data
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
        print(proto2msg(binascii.unhexlify(dat),_verbose=True))
        
 
    cmd2proto("SSS")
    cmd2proto("CCC",_verbose=True)
    
    for (i, dat) in enumerate(Samplecmd):
        print(i)
        print(cmd2proto(dat,_verbose=True))
    
    
    
    for (i, dat) in enumerate(Samplejson):
        print(i)
        print(pkgdecode(dat,_verbose=True))
        
    # current date and time
    _time = time.gmtime(615890910 + 946684800) #615890910 + (Since2000), Where January 1, 2000 UNIX time is 946684800.
    #s1 = datetime.time(615890910 + 946684800)
    #s2 = s1.strftime("%d/%m/%Y, %H:%M:%S")
    # dd/mm/YY H:M:S format
    print('_time',_time)
    #print("s2:", s2)
    
    timetup = time.strftime("%d/%m/%Y, %H:%M:%S",_time)
    print('timetup',timetup)
    
    _t_gps_yymmddHHMMSS = time.strftime("%y%m%d%H%M%S",_time)
    print('_t_gps_yymmddHHMMSS',_t_gps_yymmddHHMMSS)


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
