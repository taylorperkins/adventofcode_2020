"""
--- Day 14: Docking Data ---
As your ferry approaches the sea port, the captain asks for your help again.
The computer system that runs this port isn't compatible with the docking program on the
ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.

After a brief inspection, you discover that the sea port's computer system uses a strange bitmask
system in its initialization program.
Although you don't have the correct decoder chip handy, you can emulate it in software!

The initialization program (your puzzle input) can either update the bitmask or write a value to memory.
Values and memory addresses are both 36-bit unsigned integers.
For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory
address 8.

The bitmask is always given as a string of 36 bits, written with the most significant bit
(representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right.
The current bitmask is applied to values immediately before they are written to memory:
    a 0 or 1 overwrites the corresponding bit in the value,
    while an X leaves the bit in the value unchanged.

For example, consider the following program:

```
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
```

This program starts by specifying a bitmask (mask = ....).
The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0,
and the 64s bit is overwritten with 1.

The program then attempts to write the value 11 to memory address 8.
By expanding everything out to individual bits, the mask is applied as follows:

```
value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
```

So, because of the mask, the value 73 is written to memory address 8 instead.
Then, the program tries to write 101 to address 7:

```
value:  000000000000000000000000000001100101  (decimal 101)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001100101  (decimal 101)
```

This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set.
Finally, the program tries to write 0 to address 8:

```
value:  000000000000000000000000000000000000  (decimal 0)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001000000  (decimal 64)
```

64 is written to address 8 instead, overwriting the value that was there previously.

To initialize your ferry's docking program, you need the sum of all values left in memory after
the initialization program completes.
(The entire 36-bit address space begins initialized to the value 0 at every address.)
In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) -
producing a sum of 165.

Execute the initialization program.
What is the sum of all values left in memory after it completes?
"""

import re
from collections import defaultdict

mask_ptrn = re.compile(r'mask\s=\s(?P<mask>.*)')
instruction_pattern = re.compile(r'mem\[(?P<address>\d+)\]\s=\s(?P<value>.*)')


program_input = """mask = 011011X11X11100101XX0XX0100100000X0X
mem[48514] = 171994
mem[14856] = 472531
mem[57899] = 15860
mem[41284] = 37917047
mem[8885] = 893069967
mem[28070] = 861473
mask = X1X0111010X011100101001XX1XX111X0X01
mem[6533] = 1380
mem[24785] = 232003103
mem[39561] = 1813
mem[56060] = 528844
mem[12033] = 500106
mem[42461] = 942
mask = 011011X1110110X10100X0110100101X0111
mem[46150] = 77769198
mem[60284] = 46877
mem[4481] = 183608702
mask = 0110XX1X1011100001011011101101X00X10
mem[47778] = 1178
mem[42379] = 172491
mem[15511] = 1222721
mem[4075] = 217763
mem[32558] = 19885622
mem[25250] = 115297285
mem[27860] = 60067719
mask = 1000111110010X010110X00011XX100X101X
mem[28879] = 189
mem[3771] = 24901
mask = 0100X1X01000X010010X1100X0000XX10000
mem[23632] = 214093440
mem[47233] = 687338
mem[32851] = 231174
mem[46003] = 880
mem[7602] = 1426802
mem[3972] = 3699
mem[47289] = 505
mask = 1010X11X0X1111X0010X011110001X0001X1
mem[16569] = 890
mem[25825] = 1428
mem[27069] = 13487330
mem[33550] = 107116
mem[12019] = 3555561
mem[21184] = 11990176
mask = 0X01111XX00010110X1000001000011X0X10
mem[49300] = 12900
mem[53132] = 123292
mem[63244] = 582487
mem[52057] = 929
mem[42271] = 98646760
mask = 10XXX1100011111X010XX01X001011X0X100
mem[43262] = 390101067
mem[28758] = 32028424
mem[22541] = 96680068
mem[30470] = 233464
mem[18764] = 17922474
mem[19462] = 296723
mem[34195] = 851682798
mask = 0110111111X1X101XX0XX1010100X0111X00
mem[8788] = 521182008
mem[25073] = 7981
mem[8110] = 308146
mask = 001XXX1111X11X01010X10X0101000X100X1
mem[7308] = 37647646
mem[43917] = 584
mem[49039] = 3001
mask = 011011111X11100100010XX0111010X11XX1
mem[46367] = 3760
mem[5838] = 34060
mem[2562] = 42993
mem[19515] = 399422
mask = 110X11XX10X0111001010X10X10100100X0X
mem[7824] = 4935
mem[6652] = 17582
mem[49318] = 493060
mem[40284] = 2911890
mem[1253] = 686855900
mask = 0110111X10X0X010X1010110000001000101
mem[26944] = 10068
mem[29880] = 247865605
mem[344] = 156732
mask = X1011XX110XX1011011X0000100X00X00X01
mem[50829] = 6328666
mem[20580] = 8003627
mask = 0110X111101X10010001X11X111X1XX0011X
mem[48514] = 8724
mem[33478] = 110880653
mem[54663] = 25789957
mem[53612] = 71101282
mem[46367] = 126912123
mask = 01001110X010XXX0010X110X1X011X011100
mem[5838] = 12870
mem[18000] = 343015514
mem[30685] = 55589406
mem[44228] = 713306
mem[1129] = 2762
mem[34841] = 6885536
mask = 01XX11111X11100X0101011100110110X1X1
mem[35325] = 2451588
mem[31617] = 67673
mask = 101XX1100011X1X1X10101000010100XX1XX
mem[33227] = 662
mem[60653] = 521655
mem[55844] = 46270031
mem[37599] = 32726936
mem[63520] = 18164611
mem[3689] = 452537
mem[44086] = 24181515
mask = 0X10111111111XX1000100110001X0011011
mem[25207] = 1213525
mem[14189] = 1233337
mem[59908] = 87089062
mask = 0100X11000000XXXX101100100001111010X
mem[16846] = 61505
mem[7712] = 27563
mem[41284] = 13329774
mem[30856] = 1484896
mask = 01101111X01110010X00000010X0100101XX
mem[38419] = 321893614
mem[14991] = 51456983
mem[12381] = 57826
mem[6559] = 114401
mem[2864] = 80801276
mem[16086] = 174346439
mask = 011X11111X11100XX11XX10XX000X0000100
mem[37599] = 95947
mem[49472] = 150514
mem[19408] = 341051
mask = 0X0XX1100X100XX0010110110X011X010000
mem[23977] = 16579
mem[59997] = 941864
mem[46934] = 32577
mem[29822] = 1906
mask = 0110XX1111X10101X000110101X1XX1010X0
mem[8825] = 2107
mem[53484] = 26041
mem[57401] = 28913
mem[50959] = 330871
mem[22159] = 1625
mask = 011011X110101001010X11X11X0011001100
mem[48514] = 3042292
mem[18415] = 876307
mem[7194] = 232258902
mem[4581] = 56114
mem[11877] = 445
mem[1227] = 436429769
mem[28519] = 2502
mask = 110011X01010111001011100110111X0X00X
mem[13525] = 640526
mem[58369] = 3878
mem[3123] = 109762
mem[57150] = 883
mask = XX101X11X0111X100101110X000X1X000100
mem[48545] = 10028639
mem[4397] = 654562946
mem[36544] = 7101042
mem[27462] = 120407321
mem[35972] = 86486570
mem[23334] = 225173647
mem[17107] = 4359965
mask = 1010X11X0011111XX1010XX0000110XX0111
mem[33553] = 344335201
mem[41851] = 113543
mem[16654] = 7332484
mem[18000] = 1915
mem[31418] = 20761
mem[1980] = 580610
mask = 01101111101X10XX0101X1X01X01010001XX
mem[43269] = 388009
mem[65494] = 36864500
mem[63660] = 216949
mem[55979] = 901
mem[37686] = 3393
mem[16832] = 3665984
mask = 011010X01011100101010001X10110101XX0
mem[19693] = 2734
mem[15050] = 29935891
mem[59843] = 3476
mem[34594] = 1337
mem[60135] = 158299
mask = 10010X10001111110XX00000000011010X10
mem[39033] = 1485856
mem[57990] = 120301614
mem[29466] = 347
mem[2562] = 1116746
mem[31269] = 679154748
mem[10752] = 835
mask = 01X011111011X0010110010X00001X000100
mem[38175] = 760
mem[34594] = 7691201
mem[38984] = 227760084
mem[3650] = 6498
mem[260] = 112361
mem[5040] = 979847
mask = 01X0111X10X01X1001011XXX01110101X100
mem[5390] = 63658321
mem[52420] = 557
mem[9939] = 92796
mask = 01100X1111XX0101X00011X00X01X0X1000X
mem[60205] = 1488
mem[10924] = 18281380
mem[13336] = 200
mask = 0X1X11111011XX10X1X1011X100101000000
mem[19718] = 521
mem[4798] = 300476366
mask = 1111XX11X00X1010101101110XX01001XX1X
mem[28625] = 8177051
mem[35213] = 914
mem[65242] = 332764
mem[35563] = 130774262
mem[4034] = 363737
mask = 0110X111X111100101X001000XX10100X1X1
mem[7824] = 539173
mem[36011] = 163100
mem[52206] = 110594
mem[983] = 237912225
mem[26994] = 784662
mem[34816] = 93802160
mask = X1X0111X110X11X100X111XX01011000X001
mem[29172] = 66977843
mem[55868] = 1897
mem[19060] = 474919751
mem[23999] = 57559255
mask = 01X01X110011101001010XX0110011100001
mem[31459] = 4058
mem[34825] = 1531
mem[43468] = 101677177
mask = XX1011111111100101010X011011000X0101
mem[28830] = 26727442
mem[56639] = 306662
mem[22541] = 366
mem[9939] = 114136
mem[45799] = 6016189
mask = 01101X1X1X111X0101X101110001111X1001
mem[62665] = 3741
mem[26248] = 832
mem[59941] = 7106115
mem[48514] = 5410501
mask = 1110101110XX10100101001010X1XX00X000
mem[50118] = 28281728
mem[43269] = 2006
mem[44016] = 62408018
mem[46266] = 3679968
mem[31427] = 22292
mem[21873] = 271500992
mask = 011011101X10XX1X010X0010000010110001
mem[1227] = 16678198
mem[14471] = 240
mem[9440] = 9500918
mask = 01001X1111X111X100X111X011001001X001
mem[39839] = 7609
mem[57408] = 21285280
mem[40010] = 611
mem[17107] = 1663
mem[949] = 1225188
mask = X10X11111X0XX01001011100001101011X10
mem[44502] = 27008174
mem[42344] = 210356
mem[51532] = 39439
mem[60265] = 744132593
mem[54292] = 1045108
mask = 011011111010100100X101111111XX0001XX
mem[14524] = 86376702
mem[27033] = 4342
mem[18605] = 195606087
mem[54269] = 235274317
mem[7148] = 6140886
mem[63870] = 32336035
mask = 01101111X1X111010X01XX0X000101111001
mem[9939] = 23277
mem[50943] = 1670
mem[62142] = 54464407
mem[29816] = 428438
mask = 011X11111X011001XX000010010011010001
mem[1137] = 135929485
mem[48709] = 3800
mem[47630] = 6819
mem[6593] = 1283542
mask = 01X11111101X10X10110010X100X0XX00000
mem[24287] = 10041254
mem[39892] = 1155
mem[45799] = 1030972709
mem[22629] = 3655
mem[63738] = 443
mask = 000X110X1X111XX1011000001110100111X1
mem[28473] = 419093797
mem[7685] = 24946
mem[52504] = 251318243
mem[17060] = 57555896
mem[28696] = 12341170
mem[49318] = 949958
mem[39190] = 231228961
mask = 01101111101X10X10X01011110110X10XX00
mem[19317] = 468
mem[3496] = 1317107
mem[51159] = 896267
mem[63660] = 1269
mem[50574] = 2996
mem[8788] = 393527
mask = X10X111X11011XX101001X1000010100010X
mem[57600] = 224172
mem[14189] = 10083658
mem[6284] = 1317
mask = 11101110XX011101X011110001011111110X
mem[12189] = 6616
mem[24162] = 709192388
mem[31228] = 6509
mask = 011011111X0X110X11011X01000001X10100
mem[33478] = 1127
mem[63196] = 6450
mem[16436] = 627
mask = 010X111XX01X10000X0X01100X111XX10100
mem[46367] = 189488269
mem[1301] = 1017
mem[43933] = 162592
mask = 01101X10100011XX01011X1001011101XXX0
mem[58253] = 800107
mem[14189] = 72287
mem[36544] = 809
mem[43371] = 3936
mask = 01111X11X000X1101101011X1010XX11XX1X
mem[47353] = 8616152
mem[9948] = 31037
mem[27614] = 17552
mem[62591] = 501508
mem[15050] = 53941715
mem[18894] = 924503418
mask = 011011111X10100001010XX11000010X0010
mem[32492] = 603917
mem[65494] = 688410
mem[41842] = 751
mem[21438] = 213904
mem[23428] = 1774
mem[48864] = 3249982
mask = 111011111100110X0011X11X0X01X00100X1
mem[24518] = 1481
mem[63545] = 7584
mem[25370] = 25652
mem[11303] = 122010
mem[59025] = 12111122
mem[58468] = 55369
mask = 0010X111X1X110010XX00X1X1000100X0001
mem[38078] = 73471887
mem[20036] = 13474
mem[14857] = 285672
mem[45702] = 83750236
mem[1227] = 1667
mem[5530] = 917
mask = 10X111X00011X101X10011000X00X100001X
mem[7387] = 37192874
mem[8320] = 3746
mem[18075] = 49816
mask = 0X10111111X11X01010XXX0011XX10111001
mem[21446] = 18734
mem[10252] = 59995
mem[11187] = 160281117
mem[13384] = 3291126
mem[29879] = 1456911
mem[29103] = 2899
mask = 01111111111110X11XX01000X01101X10100
mem[18752] = 3410
mem[14785] = 4622
mem[42271] = 290433558
mask = 011X1111101X10011X1101X0100100000000
mem[28307] = 1304
mem[6468] = 59195584
mem[29675] = 843812846
mem[54269] = 2583
mem[26994] = 1628
mem[63967] = 457554
mask = 011X1X1110X01X10X1X11101101XX1X10001
mem[983] = 63290
mem[27054] = 470821
mem[46855] = 321029
mem[16757] = 51448998
mem[48854] = 209794474
mask = 010011X000111000000111101011X011XXXX
mem[47321] = 334676
mem[16953] = 49237
mem[52408] = 73
mem[2885] = 53921929
mask = 01111X1X1X0001XX11011111X1000X1X011X
mem[37442] = 6724028
mem[16975] = 403
mem[3700] = 793989
mem[62141] = 57881
mem[38753] = 1399769
mem[949] = 522895309
mem[64657] = 3690509
mask = X1111011X0X01010XX1101X11001110X0000
mem[39879] = 34462
mem[46129] = 408625
mem[6098] = 236645
mask = 01X01111X01X10X001011000110X1X0000X0
mem[36011] = 66143371
mem[62665] = 77144
mem[20333] = 4345806
mem[51268] = 14906433
mem[8788] = 8
mask = 0110111110X011101X1101111001XX00X110
mem[47837] = 3707561
mem[2788] = 237644109
mem[44500] = 834978160
mask = 0110111X1X111X1X01X11X01101110010110
mem[43269] = 81785
mem[22314] = 4809080
mem[6736] = 6765125
mask = 1X011111X010111X01010X10010101101100
mem[31228] = 8833343
mem[9980] = 117513832
mem[6652] = 280384
mask = 11111XX1000110X0101111100001X001X111
mem[23632] = 12270
mem[25370] = 268837775
mem[6278] = 4462961
mem[14856] = 44289
mem[21140] = 881796
mem[1280] = 16313542
mem[22832] = 1511
mask = X110X1111011X01001010X111X010010X110
mem[28830] = 95
mem[30956] = 26544
mem[49153] = 101432511
mem[13036] = 127079018
mem[43764] = 190124
mask = X11X111X110110010100X01XX1X010100X01
mem[9939] = 237658
mem[13574] = 2240080
mem[47770] = 17036832
mem[5418] = 746097653
mem[34417] = 1691
mem[49852] = 29846635
mask = 0X00X1111111XX11X011101011010X01010X
mem[64569] = 67751
mem[29583] = 24119861
mask = 01X011111011X00X010X000010X0011X1011
mem[36008] = 216989
mem[6736] = 11120
mem[49610] = 2479
mask = 1001X11X001X11XX01001110X0X01100XX00
mem[56033] = 3647
mem[41238] = 11425073
mem[704] = 991541
mem[36204] = 22532968
mem[58054] = 854
mem[27990] = 416
mask = 01100111XXX01X010001111101001X000110
mem[60684] = 5272670
mem[53027] = 30100333
mem[33047] = 134
mem[38314] = 2074034
mask = 011X11111000XX1011X11X11X0100X010X0X
mem[38054] = 576322
mem[62599] = 11414165
mem[31269] = 757988507
mem[19306] = 1429134
mem[44015] = 164
mem[9279] = 206541
mask = 1X10011XX011111X01X111000001XXX01011
mem[22609] = 2871
mem[5458] = 49407
mem[45715] = 11337
mem[6714] = 12943268
mem[31617] = 112522
mem[24016] = 310061
mem[50116] = 161156
mask = 01XX1011001110100101X000X011XX01011X
mem[22798] = 7712
mem[425] = 117467551
mem[38131] = 443
mem[49300] = 3427
mem[3496] = 12457
mem[56313] = 210192073
mem[11388] = 470
mask = 01X0111111X1100X01001010000XX10001XX
mem[15511] = 12882991
mem[13729] = 27587073
mem[16832] = 95887
mem[11935] = 434
mem[37599] = 9230014
mem[51456] = 940113
mask = X1X0110110X11001010X0001000100X00000
mem[42530] = 23849383
mem[4481] = 39576414
mem[27033] = 66999062
mem[2568] = 521
mask = 01XX11X1X11101011100101X01X001011001
mem[25207] = 26029326
mem[47702] = 181844
mem[61804] = 195905
mem[58661] = 573094
mask = XX0X11X110X1XX0101100X00100010111X01
mem[30539] = 937
mem[18075] = 961
mem[43468] = 2995
mask = X100111X10111000010X1XXX000X1110X010
mem[43917] = 380864177
mem[14524] = 1586
mem[18609] = 147093
mask = X111101110001010111X01010X0X0X010XX1
mem[65331] = 2368204
mem[7895] = 17051968
mem[37863] = 9960
mask = 1001X110001X110XX1000X100X00X0010010
mem[8885] = 266546087
mem[7636] = 1177692
mem[60223] = 15113918
mem[33234] = 313534611
mem[22029] = 5497253
mem[43203] = 38725
mem[27550] = 50640114
mask = X10111111X1010110X10X00X100X0X100001
mem[18725] = 175877
mem[21665] = 155179105
mem[20295] = 37333258
mem[2568] = 6498
mem[33326] = 1301
mem[49356] = 53132
mem[40627] = 2578
mask = 01X00X1X00X00100X10111X1X0010X00X100
mem[53488] = 7265
mem[45490] = 139
mem[41507] = 160588518
mask = X10X1X1110X010X10110X1001111X011111X
mem[57240] = 4916897
mem[19839] = 125142155
mem[23281] = 977
mem[3004] = 881788
mem[36506] = 76747405
mem[35213] = 5540318
mask = X1XX0X11X01X1110011110000011X100X011
mem[16620] = 245874
mem[14856] = 21357
mem[12475] = 810123
mask = 111XX111001XX0X0010110001101000X0100
mem[63199] = 305
mem[39892] = 377
mem[12295] = 175
mem[17536] = 3891
mask = 01101111101110XXX10X011X1X0X11100100
mem[19462] = 38858221
mem[62522] = 80896
mem[13993] = 111858
mem[12566] = 2009960
mem[13325] = 274
mask = 011011110XX11101X101010X01010X01001X
mem[26616] = 31949
mem[33740] = 62868747
mask = XX0111110000101101101100111XX10X101X
mem[20305] = 411809
mem[3779] = 12833168
mem[48058] = 826623362
mem[34532] = 2498
mem[36708] = 33436
mem[47233] = 86458
mem[64839] = 30673114
mask = 01111X11X11X10001111000X0X10110X00X0
mem[31360] = 89307
mem[21087] = 202229
mem[63039] = 29854290
mem[28519] = 48618785
mask = 01X01111101010010X01101X0110101111X0
mem[32447] = 16207
mem[18490] = 4246
mem[2972] = 74930276"""


def mask_gen(mask: str):
    mask = [(ind, v) for ind, v in enumerate(mask) if v != "X"]

    value = []
    while True:
        value = yield "".join(value)
        value = list(value)
        for ind, m in mask:
            value[ind] = m


def to_bit(v: int):
    return '{:036b}'.format(v)


def main():

    # will be coroutine later on
    mask = ...
    mem = defaultdict(int)

    for line in program_input.splitlines():
        if line[:3] == "mem":
            m = instruction_pattern.match(line)
            address, value = m.group("address"), m.group("value")

            masked = mask.send(to_bit(int(value)))
            mem[address] = int(masked, 2)

        else:
            mask = mask_ptrn.match(line).group("mask")

            mask = mask_gen(mask=mask)
            _ = next(mask)

    print(sum(mem.values()))


if __name__ == '__main__':
    main()
