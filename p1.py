import io
import os
import re
from io import StringIO

import requests
from nltk.tokenize import sent_tokenize
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def get_texts(base_url, filename, url=True):
    if os.path.exists(filename):
        contents = ""
        with open(filename, encoding="utf-8") as f:
            for line in f.readlines():
                contents += line
            return contents;
    if url:
        r = requests.get(base_url)
        f = io.BytesIO(r.content)
    else:
        f = open(base_url, 'rb')
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Open the url provided as an argument to the function and read the content
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(f,
                                  pagenos,
                                  maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=False):
        interpreter.process_page(page)
    f.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    file = open(filename, "w", encoding="utf-8")
    file.write(str)
    file.close()
    return str


def save_sentences(texts, file_name, language='english'):
    file = open(file_name, "w", encoding="utf-8")

    text = re.sub(r"[\n]{2,}", '. ', texts, flags=re.MULTILINE)
    text1 = re.sub(r"[\.]{2,}", '. ', text, flags=re.MULTILINE)
    text2 = re.sub(r"\n", ' ', text1, flags=re.MULTILINE)
    tokenized_text = sent_tokenize(text2, language)
    for token in tokenized_text:
        if not token.isdigit():
            if token:
                print(tokenized_text.index(token))
                s00 = re.sub(r'\s+$', '', token, flags=re.MULTILINE)
                s0 = re.sub(r'[\s]{2,}', ' ', s00, flags=re.MULTILINE)
                s = re.sub(
                    r'(^\s+|⇒|›|●||❒||•| ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||»|▶|■|||)[\s]?',
                    '', s0, flags=re.MULTILINE)
                s1 = re.sub(r'^(([0-9]+\.)|(.))$', '', s, flags=re.MULTILINE)
                s2 = re.sub(r'((page|stranica)[\s][0-9]*$)|(^»?[\s](page|stranica)[\s][0-9]*$)', '', s1,
                            flags=re.MULTILINE)
                s20 = re.sub(r'^\(*.*str.$', '', s2, flags=re.MULTILINE)
                s21 = re.sub(r'^[0-9]*[\.,\/]*[0-9]*\s+[a-zA-Z]?$', '', s20, flags=re.MULTILINE)
                s22 = re.sub(r'^[0-9]*\s+mm(\*[0-9])*$', '', s21, flags=re.MULTILINE)
                s15 = re.sub(r'^(\S+)$', '', s22, flags=re.MULTILINE)
                s30 = re.sub(r'^[0-9]*(\s+[0-9]*[a-zA-Z]?)*$', '', s15, flags=re.MULTILINE)
                s3 = re.sub(r'^[0-9]*[\.,\/]*[0-9]+$', '', s30, flags=re.MULTILINE)
                # s4 = re.sub(r'^[0-9]*([\.,-\/\s]*[0-9]+\.*\)*)*$', '', s3, flags=re.MULTILINE)
                s55 = re.sub(r'^(\S\s)*\S$', '', s3, flags=re.MULTILINE)
                s5 = re.sub(r'/((\r\n|\n|\r)$)|(^(\r\n|\n|\r))|^\s*$/gm', '', s55, flags=re.MULTILINE)
                s6 = re.sub("[\\n]{2,}", '\\n', s5, flags=re.MULTILINE)
                s66 = re.sub("[\s]{2,}", ' ', s6, flags=re.MULTILINE)
                if s66:
                    if len(s66) > 1:
                        file.write(s66 + "\n")
    file.close()
    print("finished saving to file")


all_texts = []

# english_main_url = r"C:\\Users\\DK\\Downloads\\2018-renault-kadjar-110908.pdf"
# english_texts = get_texts(english_main_url, 'en_reanultkadj.txt', False)
# save_sentences(english_texts, "output\en_instr1.txt")
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2018-renault-kadjar-112375.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_reanultkadj.txt', False)
# save_sentences(hr_texts, "output\hr_instr1.txt")
#
# english_main_url = r"C:\\Users\\DK\\Downloads\\2012-citroen-c-crosser-103071.pdf"
# english_texts = get_texts(english_main_url, 'en_citrcrosser.txt', False)
# save_sentences(english_texts, "output\en_instr2.txt")
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2012-citroen-c-crosser-107376.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_citrcrosser.txt', False)
# save_sentences(hr_texts, "output\hr_instr2.txt")



# english_main_url = r"C:\captur"
# english_texts = get_texts(english_main_url, 'en_rencap.txt', False)
# save_sentences(english_texts, "output\en_instr3.txt")
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2018-renault-captur-112229.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_rencap.txt', False)
# save_sentences(hr_texts, "output\hr_instr3.txt")
#
#
#
# english_main_url = r"C:\\Users\\DK\\Downloads\\2016-opel-corsa-93596.pdf"
# english_texts = get_texts(english_main_url, 'en_opelcorsa.txt', False)
# save_sentences(english_texts, "output\en_instr4.txt")
# hr_main_url = r"C:\\corsa.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_opelcorsa.txt', False)
# save_sentences(hr_texts, "output\hr_instr4.txt")
#
# english_main_url = r"C:\\Users\\DK\\Downloads\\2016-opel-astra-101430.pdf"
# english_texts = get_texts(english_main_url, 'en_opelastra.txt', False)
# save_sentences(english_texts, "output\en_instr5.txt")
# hr_main_url = r"C:\\astra.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_opelastra.txt', False)
# save_sentences(hr_texts, "output\hr_instr5.txt")
#
# english_main_url = r"C:\\Users\\DK\\Downloads\\2013-peugeot-208-101606.pdf"
# english_texts = get_texts(english_main_url, 'en_p208.txt', False)
# save_sentences(english_texts, "output\en_instr6.txt")
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2013-peugeot-208-107846.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_p208.txt', False)
# save_sentences(hr_texts, "output\hr_instr6.txt")
#
#
# english_main_url = 'http://aftersales.fiat.com/eLumData/EN/57/609_RENEGADE/57_609_RENEGADE_603.99.641_EN_01_07.14_L_LG/57_609_RENEGADE_603.99.641_EN_01_07.14_L_LG.pdf'
# english_texts = get_texts(english_main_url, 'en_jeep.txt')
# save_sentences(english_texts, "output\en_instr7.txt")
# hr_main_url = 'http://aftersales.fiat.com/eLumData/HR/57/609_RENEGADE/57_609_RENEGADE_603.99.348_HR_01_07.14_L_LG/57_609_RENEGADE_603.99.348_HR_01_07.14_L_LG.pdf'
# hr_texts = get_texts(hr_main_url, 'hr_jeep.txt')
# save_sentences(hr_texts, "output\hr_instr7.txt")
#
#
# english_main_url = 'C:\\Users\\DK\\Downloads\\OM60P18E.pdf'
# english_texts = get_texts(english_main_url, 'en_t.txt', False)
# save_sentences(english_texts, "output\en_instr8.txt")
# hr_main_url = 'C:\\Users\\DK\\Downloads\\LC150_OM_OM60M56E_(EE)-HR-web.pdf'
# hr_texts = get_texts(hr_main_url, 'hr_t.txt', False)
# save_sentences(hr_texts, "output\hr_instr8.txt")
#
#
# hr_main_url = r"C:\\citroenc4"
# hr_texts = get_texts(hr_main_url, 'hr_citrc4.txt', False)
# save_sentences(hr_texts, "output\hr_instr9.txt")
# english_main_url = r"C:\\Users\\DK\\Downloads\\2017-citroen-c4-aircross-103055.pdf"
# english_texts = get_texts(english_main_url, 'en_citrc4.txt', False)
# save_sentences(english_texts, "output\en_instr9.txt")#
#
#
#
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2017-citroen-berlingo-101789.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_citrberlingo.txt', False)
# save_sentences(hr_texts, "output\hr_instr10.txt")
# english_main_url = r"C:\\Users\\DK\\Downloads\\2017-citroen-berlingo-103027.pdf"
# english_texts = get_texts(english_main_url, 'en_citrberlingo.txt', False)
# save_sentences(english_texts, "output\en_instr10.txt")
#
#
#
# hr_main_url = r"C:\\Users\\DK\\Downloads\\2017-citroen-c3-103039.pdf"
# hr_texts = get_texts(hr_main_url, 'hr_citc3.txt', False)
# save_sentences(hr_texts, "output\hr_instr11.txt")
# english_main_url = r"C:\\Users\\DK\\Downloads\\2017-citroen-c3-103039.pdf"
# english_texts = get_texts(english_main_url, 'en_citc3.txt', False)
# save_sentences(english_texts, "output\en_instr11.txt")
#
#
#
# hr_main_url = 'http://aftersales.fiat.com/eLumData/HR/83/191_GIULIETTA/83_191_GIULIETTA_604.38.182_HR_05_07.10_L_LG/83_191_GIULIETTA_604.38.182_HR_05_07.10_L_LG.pdf'
# hr_texts = get_texts(hr_main_url, 'hr_alfa.txt')
# save_sentences(hr_texts, "output\hr_instr12.txt")
# english_main_url = 'http://aftersales.fiat.com/eLumData/EN/83/191_GIULIETTA/83_191_GIULIETTA_604.38.182_EN_05_07.10_L_LG/83_191_GIULIETTA_604.38.182_EN_05_07.10_L_LG.pdf'
# english_texts = get_texts(english_main_url, 'en_alfa.txt')
# save_sentences(english_texts, "output\en_instr12.txt")



# hr_main_url = 'https://ws.skoda-auto.com/OwnersManualService/Data/hr/Citigo_NF/11-2017/Manual/Citigo/A00_Citigo_OwnersManual.pdf'
# hr_texts = get_texts(hr_main_url, 'hr.txt')
# save_sentences(hr_texts, "output\hr_instr13.txt")
# english_main_url = 'https://ws.skoda-auto.com/OwnersManualService/Data/en/Citigo_NF/11-2017/Manual/Citigo/A00_Citigo_OwnersManual.pdf'
# english_texts = get_texts(english_main_url, 'en.txt')
# save_sentences(english_texts, "output\en_instr13.txt")

# hr_main_url = 'https://ws.skoda-auto.com/OwnersManualService/Data/hr/Superb_3U/05-2007/Manual/Superb/B5_Superb_OwnersManual.pdf'
# hr_texts = get_texts(hr_main_url, 'hr1.txt')
# save_sentences(hr_texts, "output\hr_instr14.txt")
# english_main_url = 'https://ws.skoda-auto.com/OwnersManualService/Data/en/Superb_3U/05-2007/Manual/Superb/B5_Superb_OwnersManual.pdf'
# english_texts = get_texts(english_main_url, 'en2.txt')
# save_sentences(english_texts, "output\en_instr14.txt")

# hr_main_url = r'C:\Users\DK\Downloads\2017-opel-adam-109334.pdf'
# hr_texts = get_texts(hr_main_url, 'hradam.txt', False)
# save_sentences(hr_texts, "output\hr_instr15.txt")
# english_main_url = r'C:\Users\DK\Downloads\2017-opel-adam-93498.pdf'
# english_texts = get_texts(english_main_url, 'enadam.txt', False)
# save_sentences(english_texts, "output\en_instr15.txt")

# hr_main_url = r'C:\Users\DK\Downloads\109355.pdf'
# hr_texts = get_texts(hr_main_url, 'hrcascada.txt', False)
# save_sentences(hr_texts, "output\hr_instr16.txt")
# english_main_url = r'C:\Users\DK\Downloads\2016-opel-cascada-93560.pdf'
# english_texts = get_texts(english_main_url, 'encascada.txt', False)
# save_sentences(english_texts, "output\en_instr16.txt")
#
# hr_main_url = r'C:\Users\DK\Downloads\2017-opel-combo-109373.pdf'
# hr_texts = get_texts(hr_main_url, 'hrcombo.txt', False)
# save_sentences(hr_texts, "output\hr_instr17.txt")
# english_main_url = r'C:\Users\DK\Downloads\2017-opel-combo-101437.pdf'
# english_texts = get_texts(english_main_url, 'encombo.txt', False)
# save_sentences(english_texts, "output\en_instr17.txt")
#
# hr_main_url = r'C:\Users\DK\Downloads\2015-opel-meriva-109342.pdf'
# hr_texts = get_texts(hr_main_url, 'hrmeriva.txt', False)
# save_sentences(hr_texts, "output\hr_instr18.txt")
# english_main_url = r'C:\Users\DK\Downloads\2015-opel-meriva-36922.pdf'
# english_texts = get_texts(english_main_url, 'enmeriva.txt', False)
# save_sentences(english_texts, "output\en_instr18.txt")

# hr_main_url = r'C:\Users\DK\Downloads\2016-opel-mokka-109384.pdf'
# hr_texts = get_texts(hr_main_url, 'hrmokka.txt', False)
# save_sentences(hr_texts, "output\hr_instr19.txt")
# english_main_url = r'C:\Users\DK\Downloads\2016-opel-mokka-93722.pdf'
# english_texts = get_texts(english_main_url, 'enmokka.txt', False)
# save_sentences(english_texts, "output\en_instr19.txt")

# hr_main_url = r'C:\Users\DK\Downloads\2016-opel-movano-109377.pdf'
# hr_texts = get_texts(hr_main_url, 'hrmovano.txt', False)
# save_sentences(hr_texts, "output\hr_instr20.txt")
# english_main_url = r'C:\Users\DK\Downloads\2016-opel-movano-93796.pdf'
# english_texts = get_texts(english_main_url, 'enmovano.txt', False)
# save_sentences(english_texts, "output\en_instr20.txt")
#
# hr_main_url = r'C:\Users\DK\Downloads\2013-opel-vivaro-109379.pdf'
# hr_texts = get_texts(hr_main_url, 'hrvivaro.txt', False)
# save_sentences(hr_texts, "output\hr_instr21.txt")
# english_main_url = r'C:\Users\DK\Downloads\2013-opel-vivaro-36976.pdf'
# english_texts = get_texts(english_main_url, 'envivaro.txt', False)
# save_sentences(english_texts, "output\en_instr21.txt")

# hr_main_url = r'C:\Users\DK\Downloads\2016-citroen-c-elysee-107379.pdf'
# hr_texts = get_texts(hr_main_url, 'hrelyso.txt', False)
# save_sentences(hr_texts, "output\hr_instr22.txt")
# english_main_url = r'C:\Users\DK\Downloads\2016-citroen-c-elysee-106968.pdf'
# english_texts = get_texts(english_main_url, 'enelysse.txt', False)
# save_sentences(english_texts, "output\en_instr22.txt")

# hr_main_url = r'C:\Users\DK\Downloads\2013-citroen-c8-107375.pdf'
# hr_texts = get_texts(hr_main_url, 'hrc8.txt', False)
# save_sentences(hr_texts, "output\hr_instr23.txt")
# english_main_url = r'C:\Users\DK\Downloads\2013-citroen-c8-103070.pdf'
# english_texts = get_texts(english_main_url, 'enc8.txt', False)
# save_sentences(english_texts, "output\en_instr23.txt")
#
# hr_main_url = r'C:\Users\DK\Downloads\2014-citroen-jumper-77549.pdf'
# hr_texts = get_texts(hr_main_url, 'hrjumper.txt', False)
# save_sentences(hr_texts, "output\hr_instr24.txt")
# english_main_url = r'C:\Users\DK\Downloads\2014-citroen-jumper-103097.pdf'
# english_texts = get_texts(english_main_url, 'enjumper.txt', False)
# save_sentences(english_texts, "output\en_instr24.txt")

# hr_main_url = r'C:\Users\DK\Downloads\112565.pdf'
# hr_texts = get_texts(hr_main_url, 'hrp108.txt', False)
# save_sentences(hr_texts, "output\hr_instr25.txt")
# english_main_url = r'C:\Users\DK\Downloads\112560.pdf'
# english_texts = get_texts(english_main_url, 'enp108.txt', False)
# save_sentences(english_texts, "output\en_instr25.txt")

# hr_main_url = r'C:\Users\DK\Downloads\109990.pdf'
# hr_texts = get_texts(hr_main_url, 'hrp301.txt', False)
# save_sentences(hr_texts, "output\hr_instr26.txt")
# english_main_url = r'C:\Users\DK\Downloads\110842.pdf'
# english_texts = get_texts(english_main_url, 'enp301.txt', False)
# save_sentences(english_texts, "output\en_instr26.txt")

hr_main_url = r'C:\Users\DK\Downloads\110513.pdf'
hr_texts = get_texts(hr_main_url, 'hrcrossland.txt', False)
save_sentences(hr_texts, "output\hr_instr27.txt")
english_main_url = r'C:\Users\DK\Downloads\111266.pdf'
english_texts = get_texts(english_main_url, 'encrossland.txt', False)
save_sentences(english_texts, "output\en_instr27.txt")

hr_main_url = r'C:\Users\DK\Downloads\110514.pdf'
hr_texts = get_texts(hr_main_url, 'hrgrandland.txt', False)
save_sentences(hr_texts, "output\hr_instr28.txt")
english_main_url = r'C:\Users\DK\Downloads\110521.pdf'
english_texts = get_texts(english_main_url, 'engrandland.txt', False)
save_sentences(english_texts, "output\en_instr28.txt")

hr_main_url = r'C:\Users\DK\Downloads\109366.pdf'
hr_texts = get_texts(hr_main_url, 'hrzafira.txt', False)
save_sentences(hr_texts, "output\hr_instr29.txt")
english_main_url = r'C:\Users\DK\Downloads\93731.pdf'
english_texts = get_texts(english_main_url, 'enzafira.txt', False)
save_sentences(english_texts, "output\en_instr29.txt")
