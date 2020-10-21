import smbus
import time

bus = smbus.SMBus(1)

'''
The following are configuration-related functions and variables, the program is executed at the end
'''

i2c_addr = 0x50   #Speech Synthesis module IIC address
date_head = 0xfd

def I2C_WriteBytes(str_):
    global i2c_addr
    for ch in str_:
        try:
            bus.write_byte(i2c_addr,ch)
            time.sleep(0.01)
        except:
            print("write I2C error")



EncodingFormat_Type = {
						'GB2312':0x00,
						'GBK':0X01,
						'BIG5':0x02,
						'UNICODE':0x03
						}
def Speech_text(str_,encoding_format):
    str_ = str_.encode('gb2312')   
    size = len(str_)+2
    DataHead = date_head
    Length_HH = size>>8
    Length_LL = size & 0x00ff
    Commond = 0x01
    EncodingFormat = encoding_format

    Date_Pack = [DataHead,Length_HH,Length_LL,Commond,EncodingFormat]

    I2C_WriteBytes(Date_Pack)

    I2C_WriteBytes(str_)

def SetBase(str_):
    str_ = str_.encode('gb2312')   
    size = len(str_)+2

    DataHead = date_head
    Length_HH = size>>8
    Length_LL = size & 0x00ff
    Commond = 0x01
    EncodingFormat = 0x00

    Date_Pack = [DataHead,Length_HH,Length_LL,Commond,EncodingFormat]

    I2C_WriteBytes(Date_Pack)

    I2C_WriteBytes(str_)

def TextCtrl(ch,num):
    if num != -1:
        str_T = '[' + ch + str(num) + ']'
        SetBase(str_T)
    else:
        str_T = '[' + ch + ']'
        SetBase(str_T)


ChipStatus_Type = {
                    'ChipStatus_InitSuccessful':0x4A,#Initialization successful
                    'ChipStatus_CorrectCommand':0x41,#Receive the correct command frame
                    'ChipStatus_ErrorCommand':0x45,#Receive unrecognized command frame
                    'ChipStatus_Busy':0x4E,#Chip busy status
                    'ChipStatus_Idle':0x4F #Chip idle state                  
                }

def GetChipStatus():
    global i2c_addr
    AskState = [0xfd,0x00,0x01,0x21]
    try:
        I2C_WriteBytes(AskState)
        time.sleep(0.05)
    except:
        print("I2CRead_Write error")


    try:
        Read_result = bus.read_byte(i2c_addr)
        return Read_result
    except:
        print("I2CRead error")

Style_Type = {
                'Style_Single':0,#0, one-by-one style
                'Style_Continue':1#1, synthesis normally 
                }#Composition style settings[f?]

def SetStyle(num):
    TextCtrl('f',num)
    while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
        time.sleep(0.002)   


Language_Type = {
                'Language_Auto':0,#0,Automatically determine the language
                'Language_Chinese':1,#1, Arabic numerals, units of measure, special symbols, Chinese synthetic
                'Language_English':2 #2, Arabic numerals, units of measure, special symbols, English synthesis
                }#Synthetic language settings[g?]

def SetLanguage(num):
	TextCtrl('g',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)

Articulation_Type = {
                'Articulation_Auto':0,#0, Automatically determine the pronunciation of the word
                'Articulation_Letter':1,#1, Letters pronunciation way
                'Articulation_Word':2#2, Word pronunciation way
                }#Set word pronunciation way[h?]

def SetArticulation(num):
	TextCtrl('h',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


Spell_Type = {
                'Spell_Disable':0,#0, Not recognize Chinese Pinyin
                'Spell_Enable':1#1, it will recognize "Pinyin + 1 digit (tone)" as Chinese Pinyin, for example: hao3
                }#Set the recognition of Chinese Pinyin [i?]

def SetSpell(num):
	TextCtrl('i',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


Reader_Type = {
                'Reader_XiaoYan':3,#3, Set pronunciation artificial Xiaoyan (female,recommended speakers)
                'Reader_XuJiu':51,#51, Set pronunciation artificial Xujiu(male,recommended speakers)
                'Reader_XuDuo':52,#52, Set pronunciation artificial Xuduo(male)
                'Reader_XiaoPing':53,#53, Set pronunciation artificial Xiaoping (female)
                'Reader_DonaldDuck':54,#54, Set pronunciation artificial Donald Duck
                'Reader_XuXiaoBao':55 #55, Set pronunciation artificial XuXiaobao (kids)             
                }#Select speaker[m?]

def SetReader(num):
	TextCtrl('m',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


NumberHandle_Type = {
                'NumberHandle_Auto':0,#0, Automatically determine
                'NumberHandle_Number':1,#1, For the number of digital processing
                'NumberHandle_Value':2#2, Digital value for processing
                }#Set the digital processing policy [n?]

def SetNumberHandle(num):
	TextCtrl('n',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)



ZeroPronunciation_Type = {
                'ZeroPronunciation_Zero':0,#0,Read “zero”
                'ZeroPronunciation_O':1#1, Read Read as “o”
                }#"0" pronunciation method[o?]

def SetZeroPronunciation(num):
	TextCtrl('o',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)



NamePronunciation_Type = {
                'NamePronunciation_Auto':0,#0, automatically determine the pronunciation of the last name
                'NamePronunciation_Constraint':1#1, compulsory use of surname pronunciation rules
                }#Set name pronunciation strategy [r?]


def SetNamePronunciation(num):
	TextCtrl('r',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)

#Speed setting[s?] ? Set speaking speed (0~10)
def SetSpeed(speed):
	TextCtrl('s',speed)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


#Intonation setting[t?] ? Set speaking intonation (0~10)
def SetIntonation(intonation):
	TextCtrl('t',intonation)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)

#Volume setting[v?] ? Set speaking volume (0~10)
def SetVolume(volume):
	TextCtrl('v',volume)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


OnePronunciation_Type = {
                'OnePronunciation_Yao':0,#0, when the composite number "1" is read as unity
                'OnePronunciation_Yi':1#1, when the composite number "1" is read as one
                }#Set the pronunciation of "1" in the number [y?]

def SetOnePronunciation(num):
	TextCtrl('y',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


Rhythm_Type = {
                'Rhythm_Diasble':0,
                'Rhythm_Enable':1
                }

def SetRhythm(num):
	TextCtrl('z',num)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)

#Restore the default parameters of synthesis
def SetRestoreDefault():
	TextCtrl('d',-1)
	while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
		time.sleep(0.002)


'''
The program execution part
'''
SetArticulation(Articulation_Type["Articulation_Word"])

SetReader(Reader_Type["Reader_XiaoPing"])
SetVolume(10)
Speech_text("hello yahboom intelligent Technology",EncodingFormat_Type["GB2312"])
while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
    time.sleep(0.1)  


SetReader(Reader_Type["Reader_XuDuo"])
Speech_text("Welcome to use yahboom intelligent technology voice broadcast module",EncodingFormat_Type["GB2312"])
while GetChipStatus() != ChipStatus_Type['ChipStatus_Idle']:
    time.sleep(0.1)   


while True:
    time.sleep(0.01)

