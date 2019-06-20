import math
import crcmod
import crcmod.predefined

def stuffing(data, flag):
    temp = data
    iterFlag = False
    count = 0
    i = 0
    while i < len(temp):
        if not iterFlag and temp[i] == flag[count]:
            iterFlag = True
            count = 1
        elif iterFlag and count == 5 and temp[i] == flag[count-1]:
            count = 0
            iterFlag = False
            temp = temp[:i+1] + '0' + temp[i+1:]
        elif iterFlag and temp[i] == flag[count]:
            count+=1
        else:
            count = 0
            iterFlag = False
        if count == 0 and temp[i] == flag[count]:
            iterFlag = True
            count = 1
        i+=1
    return(flag + temp + flag[:-1] + '1')

def destuffing(data, flag):
    temp = data.replace(flag, '')
    newdata = temp.split(flag[:-1] + '1')[:-1]
    for j in range(0, len(newdata)):
        iterFlag = False
        count = 0
        i = 0
        while i < len(newdata[j]):
            if (not iterFlag) and newdata[j][i] == flag[count]:
                iterFlag = True
                count = 1
            elif iterFlag and count == 6 and newdata[j][i] == '0':
                count = 1
                newdata[j] = newdata[j][:i] + newdata[j][i+1:]
                i-=1
            elif iterFlag and count < 6 and newdata[j][i] == flag[count]:
                count+=1
            else:
                count = 0
                iterFlag = False
                if newdata[j][i] == '0':
                    i-=1
            i+=1
    return newdata

def crc(data):
    crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
    crc16.update(data.encode('utf-8'))
    return data + bin(int(crc16.hexdigest(), 16))[2:].zfill(16)

def decrc(data):
    data = [data[:-16], data[-16:]]
    crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
    crc16.update(data[0].encode('utf-8'))
    if bin(int(crc16.hexdigest(), 16))[2:].zfill(16) != data[1]:
        return '0'
    else:
        return data[0]


def send():
    frame = '01111110'
    with open('Z', 'r') as f:
        rawdata = f.read()
        data = []
        for i in range(0, math.ceil(len(rawdata)/32)):
            if i != math.ceil(len(rawdata)/32)-1:
                data+=[rawdata[32*i:32*(i+1)]]
            else:
                data+=[rawdata[32*i:]]
        for i in range(0, len(data)):
            data[i] = crc(data[i])
        for i in range(0, len(data)):
            data[i] = stuffing(data[i], frame)
        output = ""
        for i in data:
            output += i
        with open('W', 'w') as f2:
            f2.write(output) 

def receive():
    frame = '01111110'
    with open('W', 'r') as f:
        rawdata = f.read()
        data = destuffing(rawdata, frame)
        for i in range(0, len(data)):
            data[i] = decrc(data[i])
        output = ""
        for i in data:
            output += i
        with open('R', 'w') as f2:
            f2.write(output) 

def main():
    send()
    receive()
    with open('Z', 'r') as f:
        with open('R', 'r') as f2:
            rawdata = f.read()
            rawdata2 = f2.read()
            if rawdata == rawdata2:
                print("Works!")
main()