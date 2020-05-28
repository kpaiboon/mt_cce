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
# Version 16
# 2020-05-28 1. MAP A84 Digital_Input 2. y_accel_mg_data = 30 : _y_decel_mg_data = 18
# Version 15
# 2020-05-20 1. Bug fixex _v_hexInput <= _v_hexinput= _xrawhex 2. sz = len(__PATTERN_IMEI)
# Version 14
# 2020-05-18 1. Matching pattern IMEI
# Version 12B
# 2020-05-14 1. Show Hex input16 and output 2. Add prefix ,AAA
# Version 12
# 2020-05-13 1. fixed FWD_REV_SENS is little endian 2.Optm M_HexStriped
# Version 11
# 2020-05-12 1. fixed N-byte: Photo name (*.jpg) : T633L = 0x28, MDVR = 0x44
# Version 10
# 2020-05-08 1. fixed sz json : FE 2E
# Version 9
# 2020-05-08 1. 2N-Byte Sampledathex2Nb 2. FE 2E : FWD_REV_SENS 3. Temperature , PhotoName
# Version 8
# 2020-03-16 1. EventCode share 1byte ( Code 01: T633L ) and 2byte ( Code 40: MDVR )
# Version 7
# 2020-03-15 1. Altitude Fix code 0x0B 2. del _cce_ofsbyte 3. add fuel percent
# Version 6
# 2020-03-14 1. Minimal JSON
# Version 5
# 2020-03-12 1. shortinput <== Longinput 2. __autoSpeedforceIO 3. New ADC Hex <== Int 
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
import re

__code_version = 'mtcce.v16'

__PATTERN_IMEI = '86'
__NEW_PREFIX_IMEI = '!!'

__autoSpeedforceIO = 5 #5km/h

Sampledathex = [
    '3132332C',
    '242450313036342C3836313538353034303439343436382C4343452C190000000C0054001500050501060A07001400150209080000091F010A07000B260016000017000019A2011A26054023000602D7875701034860CC0604DEBFB5240C806800000DE4A003001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B270016000017000019A2011A26054023000602D0875701034160CC0604E8BFB5240C806800000DEEA003001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A0B000B270016000017000019A2011A26054023000602CF875701033E60CC0604F2BFB5240C806800000DF8A003001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A08000B270016000017000019A3011A26054023000602D4875701034360CC0604FCBFB5240C806800000D02A103001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A07000B250016000017000019A2011A26054023000602DA875701033E60CC060406C0B5240C806800000D0BA103001C0100000001490904010000000000000054001500050501060A07001400150209080000091F010A08000B240016000017000019A2011A26054023000602DF875701032F60CC060410C0B5240C806800000D15A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B220016000017000019A2011A26054023000602E9875701031460CC06041AC0B5240C806800000D1FA103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B210016000017000019A2011A26054023000602EE875701030E60CC060424C0B5240C806800000D29A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A08000B210016000017000019A2011A26054023000602E9875701031660CC06042EC0B5240C806800000D33A103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B230016000017000019A2011A26054023000602E687570103FF5FCC060439C0B5240C806800000D3DA103001C0100000001490904010000000000000054001500050501060907001400150209080000091F010A09000B230016000017000019A2011A26054023000602E887570103E75FCC060443C0B5240C806800000D46A103001C0100000001490904010000000000000054001500050501060A070014001502090800000917010A08000B230016000017000019A2011A26054023000602E887570103D75FCC06044DC0B5240C806800000D50A103001C010000000149090401000000000000002A32300D0A',
    '2424573433302C3836343339343034303031373732372C4343452C0400000004005F00180006018605010609071F14001B000B0801000966010A08000B120016000017000018000019A1011AD608290000410000060271D9D3000393DDFF05049769FB250C61B800000D6B5605004200000000010E0C08020500800004A59C0000006400190006012305010609071F14001B000B0801000900010A08000B120016000017000018000019A1011AE308290000410000070271D9D300037ADDFF05049969FB250C63B800000D6D5605001C010000004200000000010E0C08020500800004A59C0000005F00180006010305010609071F14001B000B0801000900010A08000B120016000017000018000019A1011AE308290000410000060271D9D300037ADDFF05049969FB250C63B800000D6E5605004204000000010E0C08020500800004A59C0000006400190006012305010609071F14001B000B0802000908010A08000B0E0016000017030018000019A1011AE5082900004100000702A0D9D3000339DDFF0504A369FB250C69B800000D775605001C010000004204000000010E0C08020500800004A59C0000002A34420D0A',
    '24245E3133342C3836343339343034303031373732372C4343452C0000000001006400190006012305010606071F14001B000B08000009F6000A0C000B240016000017000018000019A1011AD808290000410000070232D9D300031EDDFF05042F6AFB250CBBB800000D045705001C010000004204000000010E0C08020500800004A59C0000002A37330D0A',
    '2424643239312C3836343339343034303031373732372C4343452C0000000001000101190006012505010609071F14001B000B0803000957000A09000B000016000017000018000019A1011A7309290000410000060278D9D3000334DDFF05046895FC250C5CCC00000DAE7306004204000000020E0C08020500800004A59C00000039712520205E44524956494E47204C4943454E53452454455354244D522E5E5E3F0D0A3B363030373634313131313131313131313131393D3138303931393737303431313D3F0D0A2B32312020202020202020202020203120202020202020202020202039393939393538202030303130303F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002A31330D0A',
    '2424663239312C3836343339343034303031373732372C4343452C010000000100010119000601250501060A071F14001B000B0802000970000A0C000B000016000017000018000019A1011A720929000041000006029DD9D3000341DDFF05047695FC250C60CC00000DBC7306004204000000020E0C08020500800004A59C00000039722520205E44524956494E47204C4943454E5345245445535437244D522E5E5E3F0D0A3B363030373634313131313131313131313131373D3138303731393737303431373D3F0D0A2B32332020202020202020202020203120202020202020202020202031303030303037202030303130303F000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002A38440D0A'
    ]

Sampledathex2Nb = [
    #2x N-bute : Type I : 0E BaseSattion : Type II : FE 2E : FWD_REV_SENS
    '2424593134382C3836343339343034303031373732372C4343452C00000000010072001A000601230501060C071714001B000B0800000958010A07000B030016000017000018000019A1011A2A09290000410000070282D9D300035ADDFF0504782020260C3B0800000D3C1C00001C0100000042EE000000020E0C080205008000059BAB000000FE2B0B00000000000000000000002A41450D0A',
    '24 24 5D 31 34 33 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 01 00 00 00 01 00 6D 00 19 00 06 01 04 05 01 06 09 07 1F 14 00 1B 00 0B 08 00 00 09 62 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A2 01 1A 2D 09 29 00 00 41 00 00 06 02 D5 D9 D3 00 03 1E DD FF 05 04 90 0E 20 26 0C 9D 03 00 00 0D 75 0A 00 00 42 EC 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 02 19 00 00 00 2B 00 00 00 03 00 2A 36 33 0D 0A',
    '24 5D 31 34 33 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 01 00 00 00 01 00 6D 00 19 00 06 01 04 05 01 06 09 07 1F 14 00 1B 00 0B 08 00 00 09 62 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A2 01 1A 2D 09 29 00 00 41 00 00 06 02 D5 D9 D3 00 03 1E DD FF 05 04 90 0E 20 26 0C 9D 03 00 00 0D 75 0A 00 00 42 EC 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 02 19 00 00 00 2B 00 00 00 03 00 2A 36 33 0D 0A',
    '24245D3134332C3836343339343034303031373732372C4343452C0100000001006D00190006010405010609071F14001B000B0800000962010A0D000B000016000017000018000019A2011A2D092900004100000602D5D9D300031EDDFF0504900E20260C9D0300000D750A000042EC000000020E0C08020500800004A59C000000FE2B0B02190000002B00000003002A36330D0A',
    '24 24 5C 35 39 32 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 05 00 00 00 05 00 6D 00 19 00 06 01 0C 05 01 06 0A 07 1F 14 00 1B 00 0B 08 00 00 09 21 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 2F 09 29 00 00 41 00 00 06 02 C0 D9 D3 00 03 32 DD FF 05 04 87 0E 20 26 0C 9B 03 00 00 0D 6B 0A 00 00 42 E6 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 17 00 00 00 2A 00 00 00 11 00 6D 00 19 00 06 01 04 05 01 06 0A 07 1F 14 00 1B 00 0B 08 00 00 09 21 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A2 01 1A 30 09 29 00 00 41 00 00 06 02 C0 D9 D3 00 03 32 DD FF 05 04 88 0E 20 26 0C 9B 03 00 00 0D 6C 0A 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 17 00 00 00 2A 00 00 00 11 00 6D 00 19 00 06 01 0C 05 01 06 0A 07 1F 14 00 1B 00 0B 08 00 00 09 21 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A2 01 1A 2F 09 29 00 00 41 00 00 06 02 C0 D9 D3 00 03 32 DD FF 05 04 88 0E 20 26 0C 9B 03 00 00 0D 6D 0A 00 00 42 E6 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 18 00 00 00 2A 00 00 00 21 00 6D 00 19 00 06 01 04 05 01 06 0A 07 1F 14 00 1B 00 0B 08 00 00 09 21 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 2F 09 29 00 00 41 00 00 06 02 C0 D9 D3 00 03 32 DD FF 05 04 8A 0E 20 26 0C 9B 03 00 00 0D 6E 0A 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 18 00 00 00 2A 00 00 00 21 00 72 00 1A 00 06 01 23 05 01 06 0A 07 1F 14 00 1B 00 0B 08 00 00 09 21 01 0A 0D 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 2A 09 29 00 00 41 00 00 07 02 C0 D9 D3 00 03 32 DD FF 05 04 8B 0E 20 26 0C 9B 03 00 00 0D 70 0A 00 00 1C 01 00 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 18 00 00 00 2A 00 00 00 21 00 2A 30 31 0D 0A',
    '24245C3539322C3836343339343034303031373732372C4343452C0500000005006D00190006010C0501060A071F14001B000B0800000921010A0D000B000016000017000018000019A1011A2F092900004100000602C0D9D3000332DDFF0504870E20260C9B0300000D6B0A000042E6000000020E0C08020500800004A59C000000FE2B0B01170000002A00000011006D0019000601040501060A071F14001B000B0800000921010A0D000B000016000017000018000019A2011A30092900004100000602C0D9D3000332DDFF0504880E20260C9B0300000D6C0A000042EE000000020E0C08020500800004A59C000000FE2B0B01170000002A00000011006D00190006010C0501060A071F14001B000B0800000921010A0D000B000016000017000018000019A2011A2F092900004100000602C0D9D3000332DDFF0504880E20260C9B0300000D6D0A000042E6000000020E0C08020500800004A59C000000FE2B0B01180000002A00000021006D0019000601040501060A071F14001B000B0800000921010A0D000B000016000017000018000019A1011A2F092900004100000602C0D9D3000332DDFF05048A0E20260C9B0300000D6E0A000042EE000000020E0C08020500800004A59C000000FE2B0B01180000002A000000210072001A000601230501060A071F14001B000B0800000921010A0D000B000016000017000018000019A1011A2A092900004100000702C0D9D3000332DDFF05048B0E20260C9B0300000D700A00001C0100000042EE000000020E0C08020500800004A59C000000FE2B0B01180000002A00000021002A30310D0A',
    '24 24 44 31 30 38 39 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 0B 00 00 00 09 00 D1 00 19 00 06 01 25 05 00 06 00 07 00 14 00 1B 00 0B 08 00 00 09 00 00 0A 00 00 0B 00 00 16 00 00 17 03 00 18 00 00 19 A1 01 1A 26 09 29 00 00 41 00 00 06 02 6C D9 D3 00 03 AE DD FF 05 04 FB 0F 20 26 0C 43 04 00 00 0D C7 0B 00 00 42 EE 00 00 00 02 39 70 25 20 20 5E 44 52 49 56 49 4E 47 20 4C 49 43 45 4E 53 45 24 54 45 53 54 34 24 4D 52 2E 5E 5E 3F 7C 3B 36 30 30 37 36 34 31 31 31 31 31 31 31 31 31 31 31 31 34 3D 31 38 30 34 31 39 37 37 30 34 31 34 3D 3F 7C 2B 31 34 20 20 20 20 20 20 20 20 20 20 20 20 31 20 20 20 20 20 20 20 20 20 20 20 20 31 30 30 30 30 30 34 20 20 30 30 31 30 30 3F FE 2B 0B 02 00 00 00 00 01 00 00 00 00 00 5F 00 18 00 06 01 19 05 01 06 09 07 00 14 00 1B 00 0B 08 01 00 09 4B 01 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 26 09 29 00 00 41 00 00 06 02 82 D9 D3 00 03 EE DC FF 05 04 00 10 20 26 0C 44 04 00 00 0D CB 0B 00 00 42 EC 00 00 00 01 FE 2B 0B 02 00 00 00 00 02 00 00 00 04 00 5F 00 18 00 06 01 0C 05 01 06 09 07 00 14 00 1B 00 0B 08 01 00 09 0A 00 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 24 09 29 00 00 41 00 00 06 02 6E D9 D3 00 03 16 DD FF 05 04 06 10 20 26 0C 49 04 00 00 0D D1 0B 00 00 42 E6 00 00 00 01 FE 2B 0B 01 01 00 00 00 05 00 00 00 00 00 5F 00 18 00 06 01 1D 05 01 06 09 07 00 14 00 1B 00 0B 08 01 00 09 0A 00 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 24 09 29 00 00 41 00 00 06 02 6E D9 D3 00 03 16 DD FF 05 04 06 10 20 26 0C 49 04 00 00 0D D1 0B 00 00 42 E6 00 00 00 01 FE 2B 0B 01 01 00 00 00 05 00 00 00 00 00 6D 00 19 00 06 01 04 05 01 06 08 07 1F 14 00 1B 00 0B 08 01 00 09 00 00 0A 10 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 24 09 29 00 00 41 00 00 06 02 6B D9 D3 00 03 16 DD FF 05 04 06 10 20 26 0C 49 04 00 00 0D D2 0B 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 00 00 00 00 00 00 00 00 FE 2B 0B 01 01 00 00 00 05 00 00 00 00 00 6D 00 19 00 06 01 0C 05 01 06 08 07 1F 14 00 1B 00 0B 08 01 00 09 00 00 0A 10 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 26 09 29 00 00 41 00 00 06 02 6B D9 D3 00 03 16 DD FF 05 04 07 10 20 26 0C 49 04 00 00 0D D2 0B 00 00 42 E6 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 02 00 00 00 05 00 00 00 26 00 6D 00 19 00 06 01 04 05 01 06 09 07 1F 14 00 1B 00 0B 08 00 00 09 53 01 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 24 09 29 00 00 41 00 00 06 02 6C D9 D3 00 03 11 DD FF 05 04 09 10 20 26 0C 49 04 00 00 0D D4 0B 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 02 00 00 00 05 00 00 00 26 00 6D 00 19 00 06 01 0C 05 01 06 09 07 1F 14 00 1B 00 0B 08 00 00 09 5C 01 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 24 09 29 00 00 41 00 00 06 02 6E D9 D3 00 03 11 DD FF 05 04 0A 10 20 26 0C 49 04 00 00 0D D5 0B 00 00 42 E6 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 03 00 00 00 05 00 00 00 19 00 6D 00 19 00 06 01 04 05 01 06 09 07 1F 14 00 1B 00 0B 08 00 00 09 50 01 0A 0F 00 0B 10 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 26 09 29 00 00 41 00 00 06 02 71 D9 D3 00 03 0C DD FF 05 04 0A 10 20 26 0C 49 04 00 00 0D D6 0B 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 03 00 00 00 05 00 00 00 19 00 2A 31 32 0D 0A',
    '24 24 42 31 34 38 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 01 00 00 00 01 00 72 00 1A 00 06 01 23 05 01 06 0A 07 1F 14 00 1B 00 0B 08 01 00 09 2C 01 0A 09 00 0B 00 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 31 09 29 00 00 41 00 00 07 02 82 D9 D3 00 03 3E DD FF 05 04 03 0F 20 26 0C D5 03 00 00 0D E8 0A 00 00 1C 01 00 00 00 42 E6 00 00 00 02 0E 0C 08 02 05 00 80 00 04 A5 9C 00 00 00 FE 2B 0B 01 1F 00 00 00 3E 00 00 00 10 00 2A 36 36 0D 0A'
    ]


Samplejson = [
    #'{"1b":{"00":{"dh":"01","ih":"05"},"01":{"dh":"0A","ih":"06"},"02":{"dh":"00","ih":"07"},"03":{"dh":"00","ih":"14"},"04":{"dh":"02","ih":"15"}},"2b":{"00":{"dh":"0000","ih":"08"},"01":{"dh":"1F01","ih":"09"},"02":{"dh":"0700","ih":"0A"},"03":{"dh":"2600","ih":"0B"},"04":{"dh":"0000","ih":"16"},"05":{"dh":"0000","ih":"17"},"06":{"dh":"A201","ih":"19"},"07":{"dh":"2605","ih":"1A"},"08":{"dh":"2300","ih":"40"}},"4b":{"00":{"dh":"D7875701","ih":"02"},"01":{"dh":"4860CC06","ih":"03"},"02":{"dh":"DEBFB524","ih":"04"},"03":{"dh":"80680000","ih":"0C"},"04":{"dh":"E4A00300","ih":"0D"},"05":{"dh":"01000000","ih":"1C"}},"nb":{"numnbytepkg":"1","00":{"dh":"0401000000000000","ih":"49","sz":"9"}},"s_pkg_datalen":"84","s_pkg_numdatapkg":"21","s_pkg_partialhex":"54001500050501060A07001400150209080000091F010A07000B260016000017000019A2011A26054023000602D7875701034860CC0604DEBFB5240C806800000DE4A003001C010000000149090401000000000000","s_pkg_partialhexlen":"170","s_pkg_remaincontainhexlen":"1902"}'
    '{"1b":{"00":{"dh":"01","ih":"05"},"01":{"dh":"0A","ih":"06"},"02":{"dh":"00","ih":"07"},"03":{"dh":"00","ih":"14"},"04":{"dh":"02","ih":"15"}},"2b":{"00":{"dh":"0000","ih":"08"},"01":{"dh":"1F01","ih":"09"},"02":{"dh":"0700","ih":"0A"},"03":{"dh":"2600","ih":"0B"},"04":{"dh":"0000","ih":"16"},"05":{"dh":"0000","ih":"17"},"06":{"dh":"A201","ih":"19"},"07":{"dh":"2605","ih":"1A"},"08":{"dh":"2300","ih":"40"}},"4b":{"00":{"dh":"D7875701","ih":"02"},"01":{"dh":"4860CC06","ih":"03"},"02":{"dh":"DEBFB524","ih":"04"},"03":{"dh":"80680000","ih":"0C"},"04":{"dh":"E4A00300","ih":"0D"},"05":{"dh":"01000000","ih":"1C"}},"nb":{"00":{"dh":"0401000000000000","ih":"49","sz":"9"}},"s_pkg_datalen":"84","s_pkg_numdatapkg":"21","s_pkg_partialhex":"54001500050501060A07001400150209080000091F010A07000B260016000017000019A2011A26054023000602D7875701034860CC0604DEBFB5240C806800000DE4A003001C010000000149090401000000000000","s_pkg_partialhexlen":"170","s_pkg_remaincontainhexlen":"1902"}'
    ]
Samplecmd = [
    '$$k28,864507030181266,B25,60*1B',
    #'@@k28,864507030181266,B25,60*1B',
    #'@@z25,864507030181266,E91*9B\r\n',
    #'@@\60,864507030181266,C50,22,23,24,0,0,0,0,0,0,0,0,0,0,0,0,0*D4',
    #'@@a31,868998030242818,C07,*102#*99', #This Fifx USSD for Dtac '*102#'
    '@@G25,864507030181266,B70*62',
    '@@A25,865789020991321,A10*62', #@ sample CCE mdvr the loc query
    '@@A25,'+__NEW_PREFIX_IMEI+'5789020991321,A10*62'
    
    ]


M_HexStripped = lambda s: "".join(i for i in s if ((0x30<=ord(i)<=0x39) or (0x41<=ord(i)<=0x46) or (0x61<=ord(i)<=0x66)) )
#print(M_HexStripped("12 56 : 88 AAFF aaff\r\n\tss"))


def decode(datin,_verbose=False):
    
    _this_limit_for_numpkg = 100
    
    datret =''
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

    # $$<Data identifier 1-char><Data length 3-4-char>,<IMEI 15-char>,<Command type 3-char aka,CCE>,
    
    #find ',CCE,' = 2C 43 43 45 2C = 2C4343452C ; Max 30 byte nomarl 23-25 byte
    
    _cce_ofs =int(rawhex.find('2C4343452C',0,30*2)/2)
    
    if _cce_ofs < 5 :
        return ''
    
    _cce_ofs = _cce_ofs + 5 # first byte of binary (after Comma)
    
    if _verbose:
        print('_cce_ofs', _cce_ofs)
        print('_cce_ofs + 10 *2 Hex', rawhex[_cce_ofs *2 :(_cce_ofs+ 10)*2] )
        print('_cce_ofs + 10 chr', str(binascii.unhexlify(rawhex[_cce_ofs *2 :(_cce_ofs+ 10)*2])))


    _header1 = rawhex[:_cce_ofs*2] # 28-byte first
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
    _js['h1_pid'] = _header_indentifier
    _js['h1_imei'] = _header_imei
    _js['h1_cmdtype'] = _header_cmdtype
    
    if _verbose:
        print('>>Header-1')
        print('_header1', len(_header1), _header1)
        print('_header_indentifier', len(_header_indentifier), _header_indentifier)
        print('_header_imei', len(_header_imei), _header_imei)
        print('_header_cmdtype', len(_header_cmdtype), _header_cmdtype)
        print('_tail1hex', len(_tail1hex), _tail1hex)
                
        print(json.dumps(_js, indent=4, sort_keys=True))
    
    # Test
    #a = '\x19\x00\x00\xF0'.encode()
    #print( int.from_bytes(a, 'little',signed=False))
    
    _hexRemainBuffer = rawhex[(_cce_ofs*2):((_cce_ofs+4)*2)] # 4-byte
    _intRemainBuffer = int.from_bytes(binascii.unhexlify(_hexRemainBuffer),'little',signed=False)
    _hexNumSmallPkg = rawhex[((_cce_ofs+4)*2):(((_cce_ofs+4)+2)*2)] # 2-byte
    _intNumSmallPkg = int.from_bytes(binascii.unhexlify(_hexNumSmallPkg),'little',signed=False)
    
    if _verbose:
        print('>>Header-2_intRemainBuffer')
        print('_hexRemainBuffer', len(_hexRemainBuffer), _hexRemainBuffer, _intRemainBuffer)
        print('>>Header-2_intNumSmallPkg')
        print('_hexNumSmallPkg', len(_hexNumSmallPkg), _hexNumSmallPkg, _intNumSmallPkg)

    fullcontainhex = rawhex[((_cce_ofs+4+2)*2):]
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
        
        partialhex = remaincontainhex[0:(_intDataPkgLen+2)*2] # fix bug --00-- : last -00
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

        _js['b'][_jskey]['1b'] = {} # init nest dict
        _js['b'][_jskey]['num_1b'] = str(_intNum1byteID)
        for _x in range(_intNum1byteID):
            _y= 1 + (_x*2)
            _xih =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+1)*2)] # 1-byte
                        
            _jsy = '{:02d}'.format(_x)
            _js['b'][_jskey]['1b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['1b'][_jsy]['ih'] = _xih
            _js['b'][_jskey]['1b'][_jsy]['dh'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',len(_xih),_xih)
                print('>>x-byte__xrawhex',len(_xrawhex),_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum1byteID*2))*2:]
        if _verbose:
            print('>>x-byte_hexNum1byteID',len(_hexNum1byteID), _hexNum1byteID, _intNum1byteID)
            print('>>x-byte__xbytehex',len(xbytehex), xbytehex)
            print('>>x-byte__remainxbytehex',len(remainxbytehex),remainxbytehex)            
        
        xbytehex = remainxbytehex
        
        _hexNum2byteID = xbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNum2byteID = int.from_bytes(binascii.unhexlify(_hexNum2byteID),'little',signed=False)
        
        _js['b'][_jskey]['2b'] = {} # init nest dict
        _js['b'][_jskey]['num_2b'] = str(_intNum2byteID)
        for _x in range(_intNum2byteID):
            _y= 1 + (_x*3)
            _xih =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+2)*2)] # 2-byte
            
            _jsy = '{:02d}'.format(_x)
            _js['b'][_jskey]['2b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['2b'][_jsy]['ih'] = _xih
            _js['b'][_jskey]['2b'][_jsy]['dh'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',len(_xih),_xih)
                print('>>x-byte__xrawhex',len(_xrawhex),_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum2byteID*3))*2:]
        if _verbose:
            print('>>x-byte_hexNum2byteID',len(_hexNum2byteID), _hexNum2byteID, _intNum2byteID)
            print('>>x-byte__xbytehex',len(xbytehex), xbytehex)
            print('>>x-byte__remainxbytehex',len(remainxbytehex),remainxbytehex)     
        
        xbytehex = remainxbytehex
        
        _hexNum4byteID = xbytehex[(0*2):((0+1)*2)] # 1-byte
        _intNum4byteID = int.from_bytes(binascii.unhexlify(_hexNum4byteID),'little',signed=False)
        
        _js['b'][_jskey]['4b'] = {} # init nest dict
        _js['b'][_jskey]['num_4b'] = str(_intNum4byteID)
        for _x in range(_intNum4byteID):
            _y= 1 + (_x*5)
            _xih =  xbytehex[(_y*2):((_y+1)*2)] # 1-byte
            _y=_y+1
            _xrawhex = xbytehex[(_y*2):((_y+4)*2)] # 4-byte
            
            _jsy = '{:02d}'.format(_x)
            _js['b'][_jskey]['4b'][_jsy] = {} # init nest dict            
            _js['b'][_jskey]['4b'][_jsy]['ih'] = _xih
            _js['b'][_jskey]['4b'][_jsy]['dh'] = _xrawhex
            
            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',len(_xih),_xih)
                print('>>x-byte__xrawhex',len(_xrawhex),_xrawhex)
                
        remainxbytehex = xbytehex[( 1+ (_intNum4byteID*5))*2:]
        if _verbose:
            print('>>x-byte_hexNum4byteID',len(_hexNum4byteID), _hexNum4byteID, _intNum4byteID)
            print('>>x-byte__xbytehex',len(xbytehex), xbytehex)
            print('>>x-byte__remainxbytehex',len(remainxbytehex),remainxbytehex)    
        
        if len(remainxbytehex) > 3: # fix bug nbyte >3
            _hexNumNBytePkg =  remainxbytehex[(0*2):((0+1)*2)] # 1-byte
            _intNumNBytePkg = int.from_bytes(binascii.unhexlify(_hexNumNBytePkg),'little',signed=False)
            remainxbytehex = remainxbytehex[2:] # fix bug --00-- :  NumNBytePkg
        else: 
            _hexNumNBytePkg = '00'
            _intNumNBytePkg = len(_hexNumNBytePkg)
            
        if _verbose:
            print('>>Header-3_intNumNBytePkg')
            print(_hexNumNBytePkg)
            print(_intNumNBytePkg)
       
        if _verbose:
            print('>>Nbyte_remainxbytehex')
            print('remainxbytehex', len(remainxbytehex), remainxbytehex)
            print('>>Nbyte_Loop for _intNumNBytePkg:', _intNumNBytePkg)

        _js['h3_NumNBytePkg'] = str(_intNumNBytePkg)
            
        if _intNumNBytePkg >  _this_limit_for_numpkg:
            return ''
        
        #for x in range(12):
        #  print(x)
        
        _js['b'][_jskey]['nb'] = {} # init nest dict
        #_js['b'][_jskey]['nb']['numnbytepkg'] = str(_intNumNBytePkg)
        _js['b'][_jskey]['num_nb'] = str(_intNumNBytePkg)
        
        
        for _x in range(_intNumNBytePkg):
            xbytehex = remainxbytehex
            _xih =  xbytehex[(0*2):((0+1)*2)] # Type-I: 1-byte
            
            _isover2xnb = False
            if (_xih == 'FE') or  (_xih == 'FD') or  (_xih == 'FF'):
                _isover2xnb = True
            
            if _isover2xnb:
                _xih =  xbytehex[(0*2):((1+1)*2)] # Type-II: 2-byte
                
            if _verbose:
                print('_isover2xnb FE xx',_isover2xnb)
                print('_xih',_xih)
            
            _yy = 0
            if not _isover2xnb:
                _hexNumNbyteID = xbytehex[(1*2):((1+1)*2)] # Type-I: 1-byte
            else:
                _hexNumNbyteID = xbytehex[(2*2):((2+1)*2)] # Type-II: 2-byte
                _yy= 1
            
            _intNumNbyteID = int.from_bytes(binascii.unhexlify(_hexNumNbyteID),'little',signed=False)
            
            _y= 2
            _xrawhex = xbytehex[((_y+_yy)*2):(((_y+_yy)+_intNumNbyteID)*2)] # N-byte
            
            remainxbytehex = xbytehex[(_y+_intNumNbyteID)*2:] # Need RAW TCP Checking Nbyte..Nbyte-1....Nbyte-2

            _jsy = '{:02d}'.format(_x)
            _js['b'][_jskey]['nb'][_jsy] = {} # init nest dict
            _js['b'][_jskey]['nb'][_jsy]['sz'] = str(_intNumNbyteID)
            _js['b'][_jskey]['nb'][_jsy]['ih'] = _xih
            _js['b'][_jskey]['nb'][_jsy]['dh'] = _xrawhex

            if _verbose:
                print('x',_x)
                print('>>x-byte__xidhex',len(_xih),_xih)
                print('>>x-byte__xrawhex',len(_xrawhex),_xrawhex)                
                print('>>x-byte_hexNumNbyteID',len(_hexNumNbyteID), _hexNumNbyteID, _intNumNbyteID)
                print('>>x-byte__xbytehex',len(xbytehex), xbytehex)
                print('>>x-byte__remainxbytehex',len(remainxbytehex),remainxbytehex)

    # Last func
    _js['in_rawhex'] = rawhex
    _js['in_numbyte'] = str(int(len(rawhex)/2))
    _js['ts_ejob'] = '{}'.format(datetime.datetime.utcnow())
    
    #_data = json.dumps(_js, indent=4, sort_keys=True)
    _data = json.dumps(_js, sort_keys=True)

    #if _verbose:       
    #    print(json.dumps(_data, indent=4, sort_keys=True))
        
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


def pkgdecode(datin,_verbose=False,_x_strImei = '868666777888999',_x_strDataID = '1'):
    
    datin = str(datin)
    datin = datin.replace('\'', '"')
    
    if _verbose: 
        print(len(datin))
        
    try:
        _js = json.loads(datin)
    except ValueError as e:
        print(e)
        print("JSON input error")
        return ''

    try:
        _obj1b = _js['1b']
        _obj2b = _js['2b']
        _obj4b = _js['4b']
        _objnb = _js['nb']
    except KeyError as e:
        print(e)
        print("JSON Get Key 1 error")
        return ''
    
    if _verbose: 
        print('_obj1b', len(_obj1b) , _obj1b)
        print('_obj2b', len(_obj2b) , _obj2b)
        print('_obj4b', len(_obj4b) , _obj4b)
        print('_objnb', len(_objnb) , _objnb)
    
    # init var @ 1b-2b shared
    _v_u16Eventcode_share_1b2b = 0
    
    # init var @ 1b
    _v_u8GpsValid = 0
    _v_u8GpsNsat = 0
    _v_u8GsmStr = 0
    _v_hexOutput = '00'
    _v_hexInput = '00'

    for _x in range(len(_obj1b)):
        _kx = '{:02d}'.format(_x)
        _xih = _obj1b[_kx]['ih']
        _xrawhex = _obj1b[_kx]['dh']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xih) , _xih)
            print('_xrawhex', len(_xrawhex) , _xrawhex)
            
        if _xih == '01':
            #share 1byte ( Code 01: T633L ) and 2byte ( Code 40: MDVR )
            _v_u16Eventcode_share_1b2b= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)           
        elif _xih == '05':
            _v_u8GpsValid = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '06':
            _v_u8GpsNsat= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '07':
            _v_u8GsmStr= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '14':
            _v_hexOutput= _xrawhex
        elif _xih == '15':
            _v_hexInput= _xrawhex
            
    if _verbose:
        print('_v_u8GpsValid', _v_u8GpsValid)
        print('_v_u8GpsNsat', _v_u8GpsNsat)
        print('_v_u8GsmStr', _v_u8GsmStr)
        print('_v_hexOutput', _v_hexOutput)
        print('_v_hexInput', _v_hexInput)
        print('_v_u16Eventcode_share_1b2b', _v_u16Eventcode_share_1b2b)   

    # init var @ 2b
    _v_u16SpeedKMH = 0
    _v_u16Heading = 0
    _v_f32Hdop = 0.0
    _v_u16Alt = 0
    _v_u16HundredthAD1 = 0
    _v_u16HundredthAD2 = 0
    _v_u16HundredthAD3 = 0
    _v_u16HundredthAD4 = 0
    _v_u16HundredthAD5 = 0
    _v_u16HundredthAD6 = 0
    _v_u16HundredthFuelPercentage = 0
    

    for _x in range(len(_obj2b)):
        _kx = '{:02d}'.format(_x)
        _xih = _obj2b[_kx]['ih']
        _xrawhex = _obj2b[_kx]['dh']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xih) , _xih)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xih == '08':
            _v_u16SpeedKMH = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '09':
            _v_u16Heading= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '0A':
            _v_f32Hdop= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1
        elif _xih == '0B':
            _v_u16Alt= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '16':
            _v_u16HundredthAD1= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '17':
            _v_u16HundredthAD2= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '18':
            _v_u16HundredthAD3= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '19':
            _v_u16HundredthAD4= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '1A':
            _v_u16HundredthAD5= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '29':
            _v_u16HundredthFuelPercentage= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)            
        elif _xih == '40':
            #share 1byte ( Code 01: T633L ) and 2byte ( Code 40: MDVR )
            _v_u16Eventcode_share_1b2b= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '41':
            _v_u16HundredthAD6= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)    
        
            
    if _verbose:
        print('_v_u16SpeedKMH', _v_u16SpeedKMH)
        print('_v_u16Heading', _v_u16Heading)
        print('_v_f32Hdop', _v_f32Hdop)
        print('_v_u16Alt', _v_u16Alt)
        print('_v_u16HundredthAD1', _v_u16HundredthAD1,'\t\t_v_u16HundredthAD2', _v_u16HundredthAD2)
        print('_v_u16HundredthAD4', _v_u16HundredthAD3,'\t\t_v_u16HundredthAD4', _v_u16HundredthAD4)
        print('_v_u16HundredthAD5', _v_u16HundredthAD5,'\t\t_v_u16HundredthAD6', _v_u16HundredthAD6)
        print('_v_u16HundredthFuelPercentage', _v_u16HundredthFuelPercentage)
        print('_v_u16Eventcode_share_1b2b', _v_u16Eventcode_share_1b2b)   

    # init var @ 4b
    _v_f32Lt = 0.0
    _v_f32Ln = 0.0
    _v_u32TimeSecSince2000 = 0
    _v_strGpsUTCyymmdHMMSS = ''
    _v_u32Mileage = 0
    _v_u32RunTimeSec = 0
    _v_u32SysFlags = 0
    _v_hexSysFlags = ''
    _v_hexWordInput = 'FF563412' # use FF as legacy input eg. 04
    
    for _x in range(len(_obj4b)):
        _kx = '{:02d}'.format(_x)
        _xih = _obj4b[_kx]['ih']
        _xrawhex = _obj4b[_kx]['dh']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xih) , _xih)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xih == '02':
            _v_f32Lt = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1000000
        elif _xih == '03':
            _v_f32Ln= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)/1000000
        elif _xih == '04':
            _v_u32TimeSecSince2000= int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
            
            _time = time.gmtime(_v_u32TimeSecSince2000 + 946684800) #615890910 + (Since2000), Where January 1, 2000 UNIX time is 946684800.
            _v_strGpsUTCyymmdHMMSS = time.strftime("%y%m%d%H%M%S",_time)
            
        elif _xih == '0C':
            _v_u32Mileage = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '0D':
            _v_u32RunTimeSec = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
        elif _xih == '1C':
            _v_u32SysFlags = int.from_bytes(binascii.unhexlify(_xrawhex),'little',signed=False)
            # reverse-hex
            _v_hexSysFlags = hex(_v_u32SysFlags)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
            
        elif _xih == '42':
            _v_hexWordInput = _xrawhex
            _v_hexInput = _v_hexWordInput[0:2]

    if _verbose:
        print('_v_f32Lt', _v_f32Lt)
        print('_v_f32Ln', _v_f32Ln)
        print('_v_u32TimeSecSince2000', _v_u32TimeSecSince2000)
        print('_v_strGpsUTCyymmdHMMSS', _v_strGpsUTCyymmdHMMSS)
        print('_v_u32Mileage', _v_u32Mileage)
        print('_v_u32RunTimeSec', _v_u32RunTimeSec)
        print('_v_hexSysFlags', _v_hexSysFlags)  
        print('_v_u32SysFlags', _v_u32SysFlags)
        print('_v_hexWordInput', _v_hexWordInput)
        print('_v_hexInput', _v_hexInput)


    # init var @ nb
    _v_c39_hexCard = ''
    _v_c39_strCard = ''
    _v_cOE_hexMccNmc = ''
    _v_cFE2B_hexFwdRevSen = ''
    _v_c28_c44_share_strPhotoName = ''
    _v_c2A_hexTemp1 = ''
    _v_c2B_hexTemp2 = ''
    _v_c2C_hexTemp3 = ''
    _v_c2D_hexTemp4 = ''
    
    _v_c2E_hexTemp5 = ''
    _v_c2F_hexTemp6 = ''
    _v_c30_hexTemp7 = ''
    _v_c31_hexTemp8 = ''
    
    for _x in range(len(_objnb)):
        _kx = '{:02d}'.format(_x)
        _xih = _objnb[_kx]['ih']
        _xrawhex = _objnb[_kx]['dh']
        if _verbose: 
            print('_kx', len(_kx) , _kx)
            print('_xidhex', len(_xih) , _xih)
            print('_xrawhex', len(_xrawhex) , _xrawhex)           
        
        if _xih == '39':
            _v_c39_hexCard = _xrawhex
            _v_c39_strCard = str(binascii.unhexlify(_xrawhex))
            _v_c39_strCard = _v_c39_strCard.replace('B\'', '')
            _v_c39_strCard = _v_c39_strCard.replace('b\'', '')
            _v_c39_strCard = _v_c39_strCard.replace('\'', '')
            _v_c39_strCard = _v_c39_strCard.replace('\\r\\n', '\r')
        elif _xih == '0E':
            _v_cOE_hexMccNmc = _xrawhex
        elif _xih == 'FE2B':
            _v_cFE2B_hexFwdRevSen = _xrawhex
        elif _xih == '28':
            _v_c28_c44_share_strPhotoName = str(binascii.unhexlify(_xrawhex))
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('B\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('b\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('\\r\\n', '\r')
        elif _xih == '44':
            _v_c28_c44_share_strPhotoName = str(binascii.unhexlify(_xrawhex))
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('B\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('b\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('\'', '')
            _v_c28_c44_share_strPhotoName = _v_c28_c44_share_strPhotoName.replace('\\r\\n', '\r')
        elif _xih == '2A':
            _v_c2A_hexTemp1 = _xrawhex
        elif _xih == '2B':
            _v_c2B_hexTemp2 = _xrawhex
        elif _xih == '2C':
            _v_c2C_hexTemp3 = _xrawhex
        elif _xih == '2D':
            _v_c2D_hexTemp4 = _xrawhex
        elif _xih == '2E':
            _v_c2E_hexTemp5 = _xrawhex
        elif _xih == '2F':
            _v_c2F_hexTemp6 = _xrawhex
        elif _xih == '30':
            _v_c30_hexTemp7 = _xrawhex
        elif _xih == '31':
            _v_c31_hexTemp8 = _xrawhex              
            
    if _verbose:
        print('_v_c39_hexCard', _v_c39_hexCard)
        print('_v_c39_strCard', _v_c39_strCard)
        print('_v_cOE_hexMccNmc', _v_cOE_hexMccNmc)
        print('_v_cFE2B_hexFwdRevSen', _v_cFE2B_hexFwdRevSen)
        print('_v_c28_c44_share_strPhotoName', _v_c28_c44_share_strPhotoName)
        print('_v_c2A_hexTemp1', _v_c2A_hexTemp1,'\t\t_v_c2B_hexTemp2', _v_c2B_hexTemp2)
        print('_v_c2C_hexTemp3', _v_c2C_hexTemp3,'\t\t_v_c2D_hexTemp4', _v_c2D_hexTemp4)
        print('_v_c2E_hexTemp5', _v_c2E_hexTemp5,'\t\t_v_c2F_hexTemp6', _v_c2F_hexTemp6)
        print('_v_c30_hexTemp7', _v_c30_hexTemp7,'\t\t_v_c31_hexTemp8', _v_c31_hexTemp8)


    
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
    # _v_strGpsUTCyymmdHMMSS 190708084830
    # _v_u32Mileage 26752
    # _v_u32RunTimeSec 237796
    # _v_u32SysFlags 1
    
    #_x_strImei = '868666777888999'
    #_x_strDataID = '1'
    
    
    _y_datalen = '99'
    _y_GpsValid = 'V'
    if _v_u8GpsValid !=0 :
        _y_GpsValid = 'A'

    _y_strFuelPerc = hex(_v_u16HundredthFuelPercentage)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
    
    _y_strBaseStationInfo = '0|0|0000|00000000'
    if len(_v_cOE_hexMccNmc) >= 22:
        _int_mcc = int.from_bytes(binascii.unhexlify(_v_cOE_hexMccNmc[0:(2*2)]),'little',signed=False)
        _int_nmc = int.from_bytes(binascii.unhexlify(_v_cOE_hexMccNmc[(2*2):(4*2)]),'little',signed=False)
        _int_lac = int.from_bytes(binascii.unhexlify(_v_cOE_hexMccNmc[(4*2):(6*2)]),'little',signed=False)
        _hex_lac = hex(_int_lac)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
        _int_cid = int.from_bytes(binascii.unhexlify(_v_cOE_hexMccNmc[(6*2):(10*2)]),'little',signed=False)
        _hex_cid = hex(_int_cid)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
        _int_rxl = int.from_bytes(binascii.unhexlify(_v_cOE_hexMccNmc[(10*2):(12*2)]),'little',signed=True)
        _y_strBaseStationInfo = str(_int_mcc)
        _y_strBaseStationInfo = _y_strBaseStationInfo + '|' + str(_int_nmc)
        _y_strBaseStationInfo = _y_strBaseStationInfo + '|' + _hex_lac
        _y_strBaseStationInfo = _y_strBaseStationInfo + '|' + _hex_cid
        _y_strBaseStationInfo = _y_strBaseStationInfo + '|' + str(_int_rxl)
        
    _v_hexLegacyIO = '1F1F'
    _v_hexLegacyIO = _v_hexInput + _v_hexOutput
    
    if _verbose:
        print('Pre _v_hexInput', _v_hexInput)
        print('Pre _v_hexOutput', _v_hexOutput)
        print('Pre _v_hexLegacyIO', _v_hexLegacyIO)
        

    #debug-case:  _v_u32SysFlags bit 1 <== 0000 00x0 where: x == 1 or 0x02
    #_v_u32SysFlags = 0x02 # ACC On
    #_v_u32SysFlags = 0x01 # Unknow
    #_v_hexLegacyIO = '100F'
    if not ((_v_u32SysFlags & 0x02) == 0):
        _int_big_v_hexLegacyIO = int.from_bytes(binascii.unhexlify(_v_hexLegacyIO),'big',signed=False)
        #print('_int_big_v_hexLegacyIO', _int_big_v_hexLegacyIO) #debug-geninfo
        _int_big_v_hexLegacyIO = _int_big_v_hexLegacyIO | int('0x0400',16)
        #print('_int_big_v_hexLegacyIO', _int_big_v_hexLegacyIO) #debug-geninfo
        _v_hexLegacyIO = hex(_int_big_v_hexLegacyIO)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
        #print('_v_hexLegacyIO', _v_hexLegacyIO) #debug-geninfo

        if _verbose:
            print('Override ACC=On <== System flag 0x02')
            print('Final _v_hexLegacyIO', _v_hexLegacyIO)

    #debug-case:  autoSpeedforceIO
    #_v_u16SpeedKMH = 99
    #_v_hexLegacyIO = '100F'
    if _v_u16SpeedKMH > __autoSpeedforceIO:
        _int_big_v_hexLegacyIO = int.from_bytes(binascii.unhexlify(_v_hexLegacyIO),'big',signed=False)        
        #print('_int_big_v_hexLegacyIO', _int_big_v_hexLegacyIO) #debug-geninfo
        _int_big_v_hexLegacyIO = _int_big_v_hexLegacyIO | int('0x0400',16)
        #print('_int_big_v_hexLegacyIO', _int_big_v_hexLegacyIO) #debug-geninfo
        _v_hexLegacyIO = hex(_int_big_v_hexLegacyIO)[2:].upper() # hex(x)[2:] use hex() without 0x get the first two characters removed
        #print('_v_hexLegacyIO', _v_hexLegacyIO) #debug-geninfo        
        
        if _verbose:
            print('Override ACC=On <== speeding over xx kmh')
            print('Final _v_hexLegacyIO', _v_hexLegacyIO)
        
    
    _y_iost = _v_hexLegacyIO
    
    _y_adcnew = '1|2|3|4|5|6' # MUST > 5 ch
    _y_adcnew = hex(_v_u16HundredthAD1)[2:].upper()
    _y_adcnew = _y_adcnew + '|' + hex(_v_u16HundredthAD2)[2:].upper()
    _y_adcnew = _y_adcnew + '|' + hex(_v_u16HundredthAD3)[2:].upper()
    _y_adcnew = _y_adcnew + '|' + hex(_v_u16HundredthAD4)[2:].upper()
    _y_adcnew = _y_adcnew + '|' + hex(_v_u16HundredthAD5)[2:].upper()
    _y_adcnew = _y_adcnew + '|' + hex(_v_u16HundredthAD6)[2:].upper()
    
    _y_rfid = 'rfid'
    if len(_v_c39_strCard) >10:
        _v_c39_strCard = _v_c39_strCard.replace('B\'', '')
        _v_c39_strCard = _v_c39_strCard.replace('b\'', '')
        _v_c39_strCard = _v_c39_strCard.replace('\'', '')
        _v_c39_strCard = _v_c39_strCard.replace('\\r\\n', '\r')
        _y_rfid = _v_c39_strCard
        _v_u16Eventcode_share_1b2b = '37' # force '37' log in/out
        
    
    _y_cust_data ='alm'
    #debug-case:  FwdRevSen
    #_v_cFE2B_hexFwdRevSen = '0103000000050000000700' # 1|3|5|7
    #_v_cFE2B_hexFwdRevSen = '020D000000110000001600' # 2|13|17|22
    
    if len(_v_cFE2B_hexFwdRevSen) >= (11*2):
        # Min 11 byte ( 22-char) ( little-endian)
        #Status: 1 byte. Example:    00 = stop    01 = forward status    02 = reverse status
        #Forward count: 4 bytes
        #Reverse count: 4 bytes
        #RPM: 2 bytes
        # formatted AAA (Customized data): ,Sensor status | Number of forward | Number of reverse | speed,

        _int_v_mag_State = int.from_bytes(binascii.unhexlify(_v_cFE2B_hexFwdRevSen[(0*2):(1*2)]),'little',signed=False) # 1 byte 0 
        _int_v_mag_FwdNum = int.from_bytes(binascii.unhexlify(_v_cFE2B_hexFwdRevSen[(1*2):(5*2)]),'little',signed=False) # 4 byte  1 2 3 4
        _int_v_mag_BckNum = int.from_bytes(binascii.unhexlify(_v_cFE2B_hexFwdRevSen[(5*2):(9*2)]),'little',signed=False) # 4 byte  5 6 7 8
        _int_v_mag_Speed = int.from_bytes(binascii.unhexlify(_v_cFE2B_hexFwdRevSen[(9*2):(11*2)]),'little',signed=False) # 2 byte 9 10
        
        _y_cust_data = '{:01d}|{:01d}|{:01d}|{:01d}'.format(_int_v_mag_State,_int_v_mag_FwdNum,_int_v_mag_BckNum,_int_v_mag_Speed)
        
        if _verbose:
            print('_v_cFE2B_hexFwdRevSen', _v_cFE2B_hexFwdRevSen)
            print('_y_cust_data', _y_cust_data)
            
    _y_a84_data = '0|0000|0000|0000|0000|0000'
    test_hexInput = _v_hexInput
    if not(len(test_hexInput) >=2):
        test_hexInput = '00'+test_hexInput
        
    _y_a84_data = '{:01d}|00{:s}|{:04X}|{:04X}|{:04X}'.format(0,test_hexInput,0,0,0)
    
    _y_accel_mg_data = 30
    _y_decel_mg_data = 18
        
    if _v_u16Eventcode_share_1b2b == 0:
        # do process
        _v_u16Eventcode_share_1b2b = '35' # force '35' standard
        
    if _verbose:
        print('Final _v_u16Eventcode_share_1b2b', _v_u16Eventcode_share_1b2b)
        print('Final _v_hexLegacyIO', _v_hexLegacyIO)
    
    pt="$$"
       
    pt= pt + _x_strDataID + _y_datalen + ','+ _x_strImei + ',' + 'AAA' + ',' + str(_v_u16Eventcode_share_1b2b) + ','    # $$<Data identifier><Data length><IMEI>AAA<Event code>
    pt= pt + str(_v_f32Lt)+','+ str(_v_f32Ln) + ',' + _v_strGpsUTCyymmdHMMSS + ',' + _y_GpsValid + ','    # <Latitude><Longitude><Date and time><Positioning status>
    pt= pt + str(_v_u8GpsNsat) +',' + str(_v_u8GsmStr) +',' + str(_v_u16SpeedKMH) +',' + str(_v_u16Heading) +','    # <Number of satellites><GSM signal strength><Speed><Direction>
    pt= pt + str(int(_v_f32Hdop/10)) +',' + str(_v_u16Alt) +',' + str(_v_u32Mileage) +',' + str(_v_u32RunTimeSec) +','    # <Horizontal dilution of precision(HDOP)><Altitude><Mileage><Total time>
    pt= pt + _y_strBaseStationInfo +',' + _y_iost +',' + _y_adcnew +',' + _y_rfid +','    # <Base station info><I/O port status><Analog input value><Assisted event info or RFID>
    pt= pt + _y_cust_data  +',' + '108' +',' + _y_strFuelPerc +',' + '0' +','    # <Customized data><Extended protocol version 108><Fuel percentage><Temperature sensor No. + Temperature value>
    pt= pt + '0' +',' + '0' +',' + '0' +',' + _y_a84_data +','    # <Data N>
    pt= pt + str(_y_accel_mg_data) +',' + str(_y_decel_mg_data) +',' +'0' +',' + '0'   # <MaxAccel_mg><MaxDecel_mg>
    pt= pt +'*FF\r\n' # <*Checksum>\r\n

    if _verbose:
        print(pt)
        
    datret = pt 
    return datret



def proto2msg(datin,_verbose=False):
    datret = ''
    _data= str(decode(datin,_verbose))
    
    #print(str(binascii.hexlify(datin)).upper())
    try:
        _js = json.loads(_data)
    except ValueError as e:
        print(e)
        print("JSON input error")
        return ''
    
    try:
        _txt_uuid = _js['__UUID__']
        _txt_imei = _js['h1_imei']
        
    except KeyError as e:
        print(e)
        print("JSON Get Key 1 error")
        return ''
    
    #_js = json.loads(str(_data))
    if len(__NEW_PREFIX_IMEI) > 0:
        sz = len(__PATTERN_IMEI)
        if _txt_imei[0:sz] == __PATTERN_IMEI:
            _txt_imei = __NEW_PREFIX_IMEI + _txt_imei[sz:]
            if _verbose:
                print('>> @Override _txt_imei',_txt_imei)
                
    if _verbose:       
        #print(json.dumps(_js, indent=4, sort_keys=True))
        print(len(_data))
        print(json.dumps(_js, sort_keys=True))
        print(_txt_uuid)
        print(_txt_imei)
        
        
    
    if not ( _js['h1_cmdtype'] == 'CCE'):
        return ''
    
    _b_obj= _js['b']

    
    if _verbose:       
        print('_b_obj', len(_b_obj), _b_obj)
        
    for _x in range(len(_b_obj)):
        _kx = 'pkg_{:02d}'.format(_x)
        _b_obj= _js['b'][_kx]

        if _verbose:
            print('_b_obj', len(_b_obj), _b_obj)
            print('_kx', _kx)
          
        datret = datret + pkgdecode(_b_obj,_verbose=_verbose,_x_strImei = _txt_imei,_x_strDataID = str(_x %10))
    #datret = _data
    return datret
    
    
def cmd2proto(datin,_verbose=False):
    '''
    "CCE" CheckSum8 Modulo 256

    *: It is a fixed character. Checksum: Contains two hexadecimal characters; indicates the sum of characters
    from the packet header to the asterisk (*) (including the packet header and asterisk).
    $$<Data identifier><Data length>,<IMEI>,<Command type>,<Command content><*Checksum>\r\n
    '''   
    datret =''
    if _verbose:
        print(__code_version)
        print(datin)
        
    postdat = datin
    
    if len(__NEW_PREFIX_IMEI) > 0:
        if len(datin) > 10:
            if datin[0:2] == '@@': #
                if datin[0:10].find(__NEW_PREFIX_IMEI) >=0:                    
                    tdat =  datin[0:10] # Extrack A
                    tdat = tdat.replace('\r','')
                    tdat = tdat.replace('\n','')
                    tdat = tdat.replace(',' +__PATTERN_IMEI , ',' +__NEW_PREFIX_IMEI) # ,86 <= ,AA
                    
                    tdat = tdat + datin[10:] # A+B
                    tdat = tdat[:len(tdat)-2]

                    #print(hex(sum('1c03e8'.encode('ascii')) % 256)[2:].upper()) # 0x94
                    #print(hex(sum(tdat.encode('ascii')) % 256)[2:].upper())
                    
                    csumhex = hex(sum(tdat.encode('ascii')) % 256)[2:].upper()
                    tdat = tdat + csumhex + '\r\n'
                    postdat= tdat
                
                    if _verbose:
                        print('>> @Override __ADD_PREFIX_IMEI cmd2proto',__NEW_PREFIX_IMEI , '__PATTERN_IMEI',__PATTERN_IMEI, 'New CheckSum',csumhex)            
    
    if _verbose:
        print(postdat)
            
    datret = postdat
    return datret
        

def main():
    print("main program")
    
    print('####### Verbose Testing ##### 2')
    for (i, dat) in enumerate(Sampledathex):
        print(i)
        print(proto2msg(binascii.unhexlify(dat),_verbose=True))

    print('####### Verbose Testing ##### 2.1')
    for (i, dat) in enumerate(Sampledathex2Nb):
        print(i)
        dat = M_HexStripped(dat)
        print(proto2msg(binascii.unhexlify(dat),_verbose=True))
 
    cmd2proto("SSS")
    cmd2proto("CCC",_verbose=True)
    
    for (i, dat) in enumerate(Samplecmd):
        print(i)
        print(cmd2proto(dat,_verbose=True))
    
    for (i, dat) in enumerate(Samplejson):
        print(i)
        print(pkgdecode(dat,_verbose=True,_x_strImei = '868666777888111',_x_strDataID = '2'))
        
    print('####### Silent ##### 2')    
    for (i, dat) in enumerate(Sampledathex):
        print(i)
        print(proto2msg(binascii.unhexlify(dat),_verbose=False))

    print('####### Silent ##### 2.1')    
    for (i, dat) in enumerate(Sampledathex2Nb):
        print(i)
        dat = M_HexStripped(dat)
        print(proto2msg(binascii.unhexlify(dat),_verbose=False))
        
        
    print('####### Silent ##### 3') 
    for (i, dat) in enumerate(Samplecmd):
        print(i)
        print(cmd2proto(dat,_verbose=False))
    print('####### Silent ##### 4') 
    for (i, dat) in enumerate(Samplejson):
        print(i)
        print(pkgdecode(dat,_verbose=False,_x_strImei = '868666777888111',_x_strDataID = '2'))
        
    # current date and time
    _time = time.gmtime(615890910 + 946684800) #615890910 + (Since2000), Where January 1, 2000 UNIX time is 946684800.
    #s1 = datetime.time(615890910 + 946684800)
    #s2 = s1.strftime("%d/%m/%Y, %H:%M:%S")
    # dd/mm/YY H:M:S format
    print('_time',_time)
    #print("s2:", s2)
    
    timetup = time.strftime("%d/%m/%Y, %H:%M:%S",_time)
    print('timetup',timetup)
    
    _t_gps_yymmdHMMSS = time.strftime("%y%m%d%H%M%S",_time)
    print('_t_gps_yymmdHMMSS',_t_gps_yymmdHMMSS)


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


'''
0x00 - 0xFA     <-- N-byte type 1
0xFE00 - 0xFFFF <-- N-byte type 2


24 24 59 31 34 38 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 00 00 00 00 01 00 72 00 1A 00 06 01 23 05 01 06 0C 07 17 14 00 1B 00 0B 08 00 00 09 58 01 0A 07 00 0B 03 00 16 00 00 17 00 00 18 00 00 19 A1 01 1A 2A 09 29 00 00 41 00 00 07 02 82 D9 D3 00 03 5A DD FF 05 04 78 20 20 26 0C 3B 08 00 00 0D 3C 1C 00 00 1C 01 00 00 00 42 EE 00 00 00 02 0E 0C 08 02 05 00 80 00 05 9B AB 00 00 00 FE 2B 0B 00 00 00 00 00 00 00 00 00 00 00 2A 41 45 0D 0A 

24 24 59 31 34 38 2C 38 36 34 33 39 34 30 34 30 30 31 37 37 32 37 2C 43 43 45 2C 00 00 00 00 01 00 72 00 1A 00 
06 ---> Quantity of 1-byte ID = 6
01 23 
05 01 
06 0C 
07 17 
14 00 
1B 00 
0B  ---> Quantity of 2-byte ID = 11
08 00 00 
09 58 01 
0A 07 00 
0B 03 00 
16 00 00 
17 00 00 
18 00 00 
19 A1 01 
1A 2A 09 
29 00 00 
41 00 00 
07  ---> Quantity of 4-byte ID = 7
02 82 D9 D3 00 
03 5A DD FF 05 
04 78 20 20 26 
0C 3B 08 00 00 
0D 3C 1C 00 00 
1C 01 00 00 00 
42 EE 00 00 00 
02  ---> Quantity of n-byte ID = 2
0E 0C 08 02 05 00 80 00 05 9B AB 00 00 00 ---> base station info    <-- N-byte type 1
FE 2B 0B 00 00 00 00 00 00 00 00 00 00 00 ---> rotation sensor      <-- N-byte type 2
2A 41 45 0D 0A 


###This only program for  <-- N-byte type 1
###todo  <-- N-byte type 1 and  <-- N-byte type 2
>>Nbyte_remainxbytehex
remainxbytehex 56 020E0C080205008000059BAB000000FE2B0B00000000000000000000
>>Nbyte_Loop for _intNumNBytePkg: 2
x 0
>>x-byte__xidhex 2 0E
>>x-byte__xrawhex 24 080205008000059BAB000000
>>x-byte_hexNumNbyteID 2 0C 12
>>x-byte__xbytehex 56 020E0C080205008000059BAB000000FE2B0B00000000000000000000
>>x-byte__remainxbytehex 28 00FE2B0B00000000000000000000
x 1
>>x-byte__xidhex 2 FE
>>x-byte__xrawhex 22 0B00000000000000000000
>>x-byte_hexNumNbyteID 2 2B 43
>>x-byte__xbytehex 28 00FE2B0B00000000000000000000
>>x-byte__remainxbytehex 0


'''
