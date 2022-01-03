from os import name
from norma_mine import normalise,list_NSWs,tokenize_basic
from nltk import text, word_tokenize
import xlwt
import pandas as pd
# text = ["On", "the", "13", "Feb.", "2007", ",", "Theresa", "May", "MP", "announced",
# "on", "ITV", "News", "that", "the", "rate", "of", "childhod", "obesity", "had", "risen",
# "from", "7.3-9.6%", "in", "just", "3", "years", ",", "costing", "the", "Gov.", "£20m", "."]
f=open('FM_datasets.txt','r',encoding='utf-8')
word=f.read().split('\n')
f.close
# # word='“In the time  of 24/11/21, at Ososa bridge on Ijebu-Ode/Sagamu expressway.“A total of seven persons were involved, all male adults. One person was injured and unfortunately, two deaths were recorded,” Ogun FRSC spokesperson, Florence Okpe told newsmen.According to Okpe, a Toyota Camry with the license plate SMK-08HK and a Lexus RX 330 with the license plate MUS-370GV were involved.According to Okpe, high speed was the likely cause of the mishap, which “led to a rear collision.”“The injured victim was taken to State Hospital, Ijebu-Ode and the dead were deposited at State Hospital Mortuary, Ijebu Ode.“A heavy capacity crane has recovered the crashed vehicle out of the river.“The Sector Commander warned against excessive speed among motorists, especially when approaching a bridge, bend etc.“He also commiserated with the family of the crash victims and enjoined them to contact FRSC Ijebu-Ode for more information,” she added.'
# Input='the 15th July, 2005 was the happiest day of late'
# empty_dict={}
# # Input=word[0]
# result=tokenize_basic(Input)
# output=list_NSWs(result,verbose=True)

# for atom in output:
#     for key in atom:
#         if atom[key][0] != atom[key][-1]:
#             empty_dict[atom[key][0]]=atom[key][-1]

def NSW(word):
    empty_dict={}
    for j in range(len(word)):
        Input=word[j]
        result=tokenize_basic(Input)
        output=list_NSWs(result,verbose=True)

        for atom in output:
            for key in atom:
                if atom[key][0] != atom[key][-1]:
                    empty_dict[atom[key][0]]=atom[key][-1]
    return empty_dict


def export_excel(export):
   #建立一个工作簿
    xls = xlwt.Workbook()
    sht1 = xls.add_sheet('Sheet1')
    xls.save('./mydata.xls')
    #向其中灌入数据
    key=list(export.keys())
    values=list(export.values())
    result_excel = pd.DataFrame()
    result_excel["Original"] = key
    result_excel["NSW"] = values
    result_excel.to_excel('./mydata.xls')

if __name__ == '__main__':
    export_excel(NSW(word))