#coding: utf-8

import sys
from array import *
import os
import copy
import pickle
import re
import io
import time
import xml.parsers.expat


# 3 handler functions
def start_element(name, attrs):
	if(name=='key'):
		if(attrs['ln']=='tb'):
			dt.keyTib='{}'.format(attrs['key'])
		else:
			n=Pref[4]
			#str=attrs['key']+':|:'+attrs['ln']+':|:TD'
			dt.value+=attrs['key']+MARK+n+END_MARK		
	
	if(name=='rec'):	
		dt.value=''
		#print ('Start element:', name, attrs)

def end_element(name):
	if(name=='rec'):
		n=Pref[4]
		if(len(dt.keyTib)>1 and len(dt.value)>3):
			#dt.rep(dt.keyTib,dt.value,':|:'+n)
			#print (dt.keyTib)
			dt.add(dt.keyTib,dt.value)
	
def char_data(data):
	pass
		#print ('Character data:', repr(data))

def loadXML(name):
			if(len(Pref)<5):
				for i in range(5):
					Pref.append('')
			Pref[4]=name
			p = xml.parsers.expat.ParserCreate()
			p.StartElementHandler = start_element
			p.EndElementHandler = end_element
			p.CharacterDataHandler = char_data
			with open(pathSave+'XML_DICT/'+name+'.xml') as f:
				p.ParseFile(f)


def test(name,d_):
	d_.get(name)
	print (d_.res)

def loadDB(dt,pDictData):
	print ('load lext files in dictionary')
	if(os.path.isdir(pDictData)):
		listD=os.listdir(pDictData)
	else: 
		print (pDictData+" is not valoid path")
	for line in listD:
		if(line[0]=='.'):
			continue
		print (line)		
		dt.loadTXT(pDictData+line,'')
		dt.saveInd()
		
	

def exportAction(sender):
	path=fileView['textfield2'].text
	path=pathMain+path
	fileView.x=1024
	dk.export(path)


def selectAction(request):
	if('action' in request):
		action=request['action']
		if (len(action)>0 and action[0]=='export'):
			export()
			return

def dictionary(sender):
	js='readStr()'
	if(mainDictView.x==0):
		textAll=dictView.eval_js(js)
	else:
		textAll=textIn.eval_js(js)
	str=htmlToText(textAll)
	str+='་'
	str=str.replace('་་','་')
	print (str)
	searchText.text=str	
	if(len(str)>1):
		dictEntry()

def fullRep(sender):
	str=searchText.text
	if(len(str)>0):
		str+='་'
		str=str.replace('་་','་')
		searchText.text=str	
		dictReport()
		printHtml(dt.data[0])
			
	dt.mainMode=FULL_REPORT	
	js='readText()'
	textAll=textIn.eval_js(js)
	#textIn.text is unicode, it is need convert it in utf-8
	textAll='{}'.format(textAll)
	textAll=htmlToText(textAll)
	dt.data[0]=textAll
	dictReport()
	printHtml(dt.data[0])
	#searchBtn.title='Word From Text'
	dt.mainMode=DICT_REPORT_TEXT
	#t2=time.time()
	#printHtml(report+'\n done in {} sec'.format(t2-t1))

	
def translate(sender):
	str=searchText.text
	if(len(str)>0 and str[0]=='?'): #parse request as CGI query request
				request=urlparse.parse_qs(str[1:])
				selectAction(request)
				return
	if(len(str)>0):
		str+='་'
		str=str.replace('་་','་')
		searchText.text=str
		dictEntry()
		return
		
	dt.mainMode=TRANSLATE			
	js='readText()'
	textAll=textIn.eval_js(js)
	#textIn.text is unicode, it is need convert it in utf-8
	textAll='{}'.format(textAll)
	textAll=htmlToText(textAll)
	dt.data[0]=textAll
	dictReport()
	printHtml(dt.data[0])
	dt.mainMode=DICT_REPORT_TEXT
	#t2=time.time()
	#printHtml(report+'\n done in {} sec'.format(t2-t1))
		
			
def dictEntry():
	"""report from all dictionaries in database"""
	mainDictView.x=0
	mainDictView.height=1024
	textAll=searchText.text
	textAll='{}'.format(textAll)
	textAll+='་'
	textAll=textAll.replace('་་','་')
	dt.history.append(textAll)
	dk.get(textAll)
	res=''
	res+='['+linkDict(textAll)+linkEdit('='+dk.res)+']་<hr>'
	dt.get(textAll)
	dt.formatReport()
	res+=dt.res
	printHTML_(res)
	
def wordReport():
	#dictReport()
	pass
	
def dictReport():
	report=''
	textAll=dt.data[0]
	#textAll='བ་དག་གི་འབྲས་བུའི་མཆོག་མཐར་ཐུག་པ་ནི་རང་བཞིན་རྫོགས་པ་ཆེན་པོའི་ཆོས་ཀྱི་རྣམ་གྲངས་ལས་འོད་གསལ་རྡོ་རྗེ་སྙིང་པོའི་ཐེག་པ་བླ་ན་མེད་པ་འདི་ཡིན་ཏེ་།་\n'
	textAll=textAll.replace(' ','\n')
	text=textAll.split('\n')
	d=dk.dictKey
	reportT=''
	n=0
	
	for n in range(0,len(text)-1):
		src=text[n]
		s=src
		reportN=text[n+1]
		rd={} #dictionary of words result
		lng=len(s)
		if(lng<2):
			continue
		if(re.search('་', reportN) == None and re.search('།', reportN) == None):
			reportT=reportN
		if(re.search('་', s) == None and re.search('།', s) == None):
			if(re.search('[\d\[<]',src)!=None):
				report+='<br><d>'+src+'</d>'
			continue
		s=unicode(s)
		s=re.sub(u'[ _\d\ "	\'\*\(\)\{\}\[\]@•#\%\&༄༅༔༴༡༢༣༤༥༦༧༨༩༠༎།༑༈༌༐༏༼༽ऀ-ॿ]',u"་",s)
		s=re.sub(u'ཿ',u'ཿ་',s)
		s=s+u'་།'
		s=re.sub(u'་[་]+',u"་",s)
		s=re.sub(u'([^་])འོ་',r"\1་(точка)་",s)
		#s=re.sub(u'([^་])འམ་',r"\1་[འམ=или]་",s)
		s=re.sub(u'ག་གོ་།',u"ག་(точка)་",s)
		s=re.sub(u'ང་ངོ་།',u"ང་(точка)་",s)
		s=re.sub(u'ད་དོ་།',u"ད་(точка)་",s)
		s=re.sub(u'ན་ནོ་།',u"ན་(точка)་",s)
		s=re.sub(u'བ་བོ་།',u"བ་(точка)་",s)
		s=re.sub(u'མ་མོ་།',u"མ་(точка)་",s)
		s=re.sub(u'ར་རོ་།',u"ར་(точка)་",s)
		s=re.sub(u'ལ་ལོ་།',u"ལ་(точка)་",s)
		s=re.sub(u'ས་སོ་།',u"ས་(точка)་",s)
		s=re.sub(u'་ཏོ་།',u"་(точка)་",s)
		s=re.sub(u'་པའང་',u"་པ་[འང=уступ.]་",s)
		s=re.sub(u'་བའང་',u"་བ་[འང=очень]་",s)
		s='{}'.format(s)

		l=s.split('་')
		res=''
		resD=''
		
				
		lng=len(l)
		start=0
		end=lng-1
		
		i=lng
		count=0
		#t1=time.time()
		
		while start<lng :
			#make query string decrease end
			end=lng
			while end>-1 :
				j=start
				line=''
				while j < end:
					line+=l[j]+'་'
					j+=1
				count+=1
				if (count >1000):
					#print (line+' {} {}'.format(start,end))
					break
				ld=line+'\n'
				if(ld in d):
					dk.get(line)
					#c=str(dk.res)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					if('__' in c):
						res+='['+linkDict(line)+linkEdit('='+c)+']་<br></c><c>'
						end-=1
						continue
					res+='['+linkDict(line)+linkEdit('='+c)+']་'
					if(dt.mainMode==FULL_REPORT and start==0 and end==lng-1):
						end-=1
						continue
					start=end-1
					break
				#next check big dictionary report
				if(len(line)>3 and ld in dt.dictKey):
					resD+='['+linkDict(line)+linkEdit('=')+'] '
				ln=line+'@'
				l1=ln.replace('འི་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-འི་')+linkEdit('=g.p')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('ས་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-ས་')+linkEdit('=i.p.')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('ར་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-ར་')+linkEdit('=d.l.')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):	
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('འོ་@','འ་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+'](точка)་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				l1=ln.replace('འམ་@','་')
				ld=l1+'\n'
				if(ld in d):
					dk.get(l1)
					c=dk.res
					if(EMPTY_MARK in c):
						end-=1
						continue
					res+='['+linkDict(l1)+linkEdit('='+c)+']་['+linkDict('-འམ་')+linkEdit('=или')+']་'
					rd[l1]=1
					start=end-1
					break
				#next check big dictionary report
				if(len(l1)>3 and ld in dt.dictKey):
					resD+='['+linkDict(l1)+linkEdit('=')+'] '
				end-=1
				if(end==start):
					res+=line
					break
			start+=1
			res=res.replace(':|:YP','')	
		
		if(re.search('lt',src)!=None):
			src='<d>'+src+'</d>'
		else:
			src='<tib contentEditable>'+src+'</tib>'
		report+=src+'\n<d>'+reportT+'</d><br>\n<w>'+res+'\n'
		if(len(resD)>10):
			report+='<r>'+resD+'</r>'	
		report+='</w><br><br>\n'
		reportT=''
		if(dt.mainMode==FULL_REPORT):
			res=''
			for line in l:
				ld=line+'་\n'
				key=line+'་'
				if(ld in d):
					dk.get(key)
					c=dk.res
					res+='['+linkDict(key)+linkEdit('='+c)+']་'	
			res=res.replace(':|:YP','')		
			report+='<br><c>'+res+'</c>\n<br>'	
			
		#print (report)
		#sys.exit()
		#return
	dt.data[0]=report
	
def linkDict(line):
	s=''
	id='s{}'.format(dt.id)
	s='<r id="'+id+'" onClick="set(\''+id+'\')">'+line+'</r>'
	dt.id+=1
	return s
	
def linkText(line):
	s=''
	id='s{}'.format(dt.id)
	s='<t id="'+id+'" onClick="edit(\''+id+'\')">'+line+'</t>'
	dt.id+=1
	return s

'''
def linkEdit(line):
	#line=re.sub('^[^:]*:\|:','=',line)
	s=''
	id='s{}'.format(dt.id)
	l=line
	line=line.replace('@','')
	line=line.replace('*','')
	line=line.replace('%','')
	if(l!=line):
		s='<t id="'+id+'" onClick="edit(\''+id+'\')" onBlur="v(\''+id+'\')">'+line+'</t>'
	else:
		s='<t id="'+id+'" onClick="edit(\''+id+'\')" onBlur="v(\''+id+'\')"><r>'+line+'</r></t>'
	dt.id+=1
	return s
'''

def linkEdit(line):
	#line=re.sub('^[^:]*:\|:','=',line)
	s=''
	id='s{}'.format(dt.id)
	l=line
	line=line.replace('@','')
	line=line.replace('*','')
	line=line.replace('%','')
	
	s='<t id="'+id+'" style="color:white" onClick="edit(\''+id+'\')" onBlur="v(\''+id+'\')">'+line+'</t>'
	
	dt.id+=1
	return s	

def convertDict():
	with open(pathSave+"allDict_uni.txt",'w') as f:
		with open(pathSave+"allDict_rus16.js",'r') as file:
			for line in file:
				if(('","","' in line)==False):
					continue
				str=line.replace('["','')
				str=str.replace('","","',' @ ')
				str=str.replace('"],','')
				f.write(str)
										 
def previousPage(sender):
	global Pref
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r", newline="\n") as f:
		textFile=f.readlines()
	c=pageIndex.text
	i=0
	if('#' in c):
		for line in textFile:
			if(c in line):
				break
			i+=1
		i=i/pageSize
	else:
		i=eval(c)-1
	if(i<0):
		i=len(textFile)/pageSize
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	Pref[2]=pageIndex.text
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	searchBtn.title='Translate'
	dt.mainMode=TRANSLATE
	searchText.text=''
	savePref()
	printHtml(text)


def nextPage(sender):
	global Pref
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
	c=pageIndex.text
	i=0
	if('#' in c):
		for line in textFile:
			if(c in line):
				break
			i+=1
		i=i/pageSize
	else:
		i=eval(c)+1
	if(i>len(textFile)/pageSize):
		i=0
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	Pref[2]=pageIndex.text
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	searchBtn.title='Translate'
	dt.mainMode=TRANSLATE
	searchText.text=''
	savePref()
	printHtml(text)
	
	
def printHtml(text):
	#with open(pathSave+pageStyle,"r") as f:
	htmlPage=Pref[0]
	str=htmlPage.replace('@@@TEXT@@@',text)
	str=str.replace( chr(0),' ')
	textIn.load_html(str)	

def printHTML_(text):
	#with open(pathSave+pageStyle,"r") as f:
	htmlPage=Pref[0]
	str=htmlPage.replace('@@@TEXT@@@',text)
	dictView.load_html(str)	

def openText():
	pathField=fileView['textfield1']
	path=pathField.text	
	path=pathMain+'{}'.format(path)
	if(os.path.isfile(path)):
		
		with open(pathSave+pageStyle,"r") as f:
			htmlPage=f.read()
			Pref[0]=htmlPage
		with open(path,"r",newline="\n") as f:
			textFile=f.readlines()
			if(len(textFile)<1):
				str='no text'
			else:
				if(len(textFile[0])>1024):
					str='too long line'
				else:
					c=pageIndex.text
					i=eval(c)
					page=textFile[i*pageSize:i*pageSize+pageSize]
					#pageIndex.text='{}'.format(i)
					str='<br>'.join(page)
					if(len(str)>90000):
						str='too long line'
				
			text='<t id="t1" onClick="edit(\'t1\')">'+str+'</t>'
			str=htmlPage.replace('@@@TEXT@@@',text)
			str=str.replace( chr(0),' ')
			textIn.load_html(str)	
			#print (str)
	else:
		print ('not open '+ path)
		menu(1)
		
def copyText(sender):
	pathField=fileView['textfield1']
	path=pathField.text	
	path=pathMain+'{}'.format(path)
	if(os.path.isfile(path)):
		with open(path,"r") as f:
			textFile=f.read()
		dialogs.share_text(textFile)
	
def menu(sender):
	path=fileView['textfield1'].text
	path=re.sub('/[/]+','/',path)
	fileView['textfield1'].text=path
	tbl=fileView['tableview1']
	tblD=fileView['tableview2']
	path=os.path.dirname(path)
	if(os.path.isdir(pathMain+path)):
		listD=os.listdir(pathMain+path)
	else:
		path='/'
		listD=os.listdir(pathMain)
		fileView['textfield1'].text='/'
	l=[]
	ld=['...']
	for line in listD:
		if(os.path.isdir(pathMain+path+'/'+line)):
			ld.append(line)
		else:
			l.append(line)
	tbl.data_source.items=l
	tblD.data_source.items=ld
	fileView.x=0
	
def openDir(sender):
	path=fileView['textfield1'].text
	path=path.replace('#','/')
	path=os.path.dirname(path)
	tbl=fileView['tableview1']
	tblD=fileView['tableview2']
	dir=tblD.data_source.items[tblD.selected_row[1]]
	if(dir=='...'):
		path=os.path.dirname(path)
		dir=''
	listD=os.listdir(pathMain+path+'/'+dir)
	c=path+'/'+dir+'/'
	c=c.replace('#','/')
	c=re.sub('//+','/',c)
	fileView['textfield1'].text=c
	l=[]
	ld=['...']
	for line in listD:
		if(os.path.isdir(pathMain+path+'/'+dir+'/'+line)):
			ld.append(line)
		else:
			l.append(line)
	tbl.data_source.items=l
	tblD.data_source.items=ld

def openFile(sender):
	global Pref
	tbl=fileView['tableview1']
	line=tbl.data_source.items[tbl.selected_row[1]]
	fileView.x=1024
	path=fileView['textfield1'].text
	path=os.path.dirname(path)
	fileView['textfield1'].text=path+'/'+line
	Pref[1]=path+'/'+line
	Pref[2]='0'
	pageIndex.text='0'
	savePref()
	openText()
		
def closeMenu(sender):
	fileView.x=1024

def replaceRegExpFile(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	pathRep=fileView['textfield3'].text
	pathRep=pathMain+'{}'.format(pathRep)
	with open(pathRep,"r") as f:
		str=f.read()
		dataRegExp=str.split('\n:|:\n')
		
	path=os.path.dirname(path)
	listD=os.listdir(path)
	for line in listD:
		print (line)
		if(os.path.isdir(path+'/'+line)):
			pass
		else:
			print ('start '+line)
			with open(path+'/'+line,"r") as f:
				text=f.read()
				for l in dataRegExp:
					c=l.split(' --> ')
					if(len(c)<2):
						print ('not valid re '+l)
					else:
						text=re.sub(c[0],c[1],text)
			with open(path+'/'+line,"w") as f:	
				f.write(text)	
			print ('done '+line	)

	
def replaceRegExp(sender):
	pass	

def replaceRegExpText(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	textSrc=fileView['textfield4'].text
	textSrc='{}'.format(textSrc)
	textRep=fileView['textfield5'].text
	textRep='{}'.format(textRep)
	a=re.compile(textSrc,re.M)
	with open(path,"r") as f:
		textFile=f.read()
		textFile=unicode(textFile)
		c=chr(0xA0)
		textFile=re.sub(c,' ',textFile)
		textFile='{}'.format(textFile)
		#s=textFile[0:32]
		#s=unicode(s)
		#i=0
		#while i<len(s):
		#	print ('{0:x}'.format(ord(s[i])))
		#	i+=1
		
		textFile=re.sub(a,textRep,textFile)
		#textFile=textFile.replace(textSrc,textRep)
		#textFile=textFile.replace(' ','\n')
		#textFile=re.sub('།','།\n',textFile)
		#textFile=re.sub(r'\n[\n]+','\n',textFile)
		#textFile=re.sub(r'།\n[ ]*།\n','།\n།',textFile)
		#textFile=re.sub(r' ','\n',textFile)
		
	with open(path,"w") as f:	
		f.write(textFile)		
	openText()
	fileView.x=1024
	
	
def searchInDharmabook(sender):
	path=pathSave+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	res=''
	i=0

	with open(path,"r") as f:
		for line in f:
			str=line[0:1024]
			if(text in str):
				l=len(str)
				str=str[0:str.rfind(' ')]
				if(len(str)==l):
					str=str[0:str.rfind('¶')]
				res+=str+'\n'
				i+=1
			if(i>300):
				break		
	with open(pathSave+'res_dharmabook.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
		
def searchInDharmabookFullText(sender):
	path=pathSave+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	res=''
	searchCount=0

	with open(path,"r") as f:
		for line in f:
			index=line.find(text)
			if(index!=-1):
				str=line[0:256]
				if(str.rfind(' ')!=-1):
					str=str[0:str.rfind(' ')]
				else:
					if(str.rfind('¶')!=-1):
						str=str[0:str.rfind('¶')]
					else:
						if(str.rfind('་')!=-1):
								str=str[0:str.rfind('་')]
				#print ('{0:d}'.format(len(resList))+' found '+str)
				res+='\n================================\n'+str+'\n____________________________________\n'
	
			while(index!=-1):	
					str=line[index-512:index]
					l=len(str)
					if(str.find(' ')!=-1):
						str=str[str.find(' '):l]
					else:
						if(str.find('¶')!=-1):
							str=str[str.find('¶'):l]
						else:
							if(str.find('་')!=-1):
								str=str[str.find('་'):l]
					res+=str
					
					str=line[index:index+512]
					if(str.rfind(' ')!=-1):
						str=str[0:str.rfind(' ')]
					else:
						if(str.rfind('¶')!=-1):
							str=str[0:str.rfind('¶')]
						else:
							if(str.rfind('་')!=-1):
								str=str[0:str.rfind('་')]
					res+=str+'\n\n'
					searchCount+=1
					if(searchCount>300):
						break		
					index=line.find(text,index+len(text))
			if(searchCount>300):
					break 
	res=unicode(res)
	c=chr(0xA0)
	res=re.sub(c,' ',res)
	res='{}'.format(res)		
	res=res.replace('¶','\n')
	res=res.replace('། ','།\n')
	res=res.replace('༔ ','༔ \n')
	with open(pathSave+'res_dharmabookFullText.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
		
		
def exportTextByID(sender):
	path=pathSave+"XML_DICT/DHARMABOOK.tab"	
	text=fileView['textfield6'].text
	text='{}'.format(text)
	with open(path,"r") as f:
		for line in f:
			str=line[0:128]
			if(text in str):
				with open(pathSave+'res_dharmabookText.txt',"w") as f:
					f.write(line)  
				break	
		fileView.x=1024


def searchInFolder(sender):
	print ('search')
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	print (path)
	str=fileView['textfield6'].text
	str='{}'.format(str)
	res=''	
	path=os.path.dirname(path)
	listD=os.listdir(path)
	i=0
	for line in listD:
		if(os.path.isdir(path+'/'+line)):
			pass
		else:
			with open(path+'/'+line,"r") as f:
				for l in f:
					if (str in l):
						res+=line+'\n'+l+'\n'
						i+=1
						if(i>100):
							res=res.replace('\n\n','\n')
							with open(pathSave+'res.txt',"w") as f:
								f.write(res)
							return
	res=res.replace('\n\n','\n')
	with open(pathSave+'res_1.txt',"w") as f:
		f.write(res)

def searchInFileText(sender):
	path=fileView['textfield1'].text
	text=fileView['textfield6'].text
	text='{}'.format(text)
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
	i=0
	for line in textFile:
		if(text in line):
			break
		i+=1
	i=i/pageSize
	page=textFile[i*pageSize:i*pageSize+pageSize]
	pageIndex.text='{}'.format(i)
	text='<t id="t1" onClick="edit(\'t1\')">'+'<br>'.join(page)+'</t>'
	printHtml(text)
	fileView.x=1024
	
def searchInFile(sender):	
	path=fileView['textfield1'].text
	text=fileView['textfield6'].text
	text='{}'.format(text)
	path=pathMain+'{}'.format(path)
	res='test'
	searchCount=0

	with open(path,"r",newline="\n") as f:
		textLines=f.readlines()
		i=1
		l=len(textLines)-1
		while(i<l):
			index=textLines[i].find(text)
			if(index!=-1):
				res+=textLines[i-1]+textLines[i]+textLines[i+1]+'\n༄།།\n'
				searchCount+=1
			i+=1
	print (searchCount)
	with open(pathSave+'res_dharmabookTextSearch.txt',"w") as f:
		f.write(res) 		
		fileView.x=1024
		


def close(sender):
	dt.close()	
	view.close()
	savePref()

def cmpLines(a,b):
	a_=len(a.split(' @ ')[0])
	b_=len(b.split(' @ ')[0])
	if(a_>b_):
		return -1
	elif(a_<b_):
		return 1
	else:
		return 0
	

def saveDict(text):
	dictNew=list()
	text=re.sub(r'<[^>]*>','',text)
	text=text.replace('«','༼')
	text=text.replace('{','༼')
	text=text.replace('»','༽')
	text=text.replace('}','༽')
	lines=text.split('[')
	for l in lines:
		if ('=' in l):
			continue
		if ('/' in l):
			#print (l)
			c=l.split(']')
			d=c[0].split('/')
			if(len(d)>1):
				key=d[0]+'་'
				key=key.replace('་་','་')
				if (d[1]=='-'):
					dk.rem(key)
					continue
				if(len(d[0])<3 or len(d[1])<3):
					continue
				value=d[1]+'%'
				value=value.replace('@%','%')
				value=value.replace('*%','%')
				value=value.replace('%%','%')
				dk.put(key,value)
	dk.saveInd()
		
def htmlToText(textAll):
	textAll=textAll.replace('\n','')
	textAll=textAll.replace('<br>','\n')
	textAll=textAll.replace('<div>','\n')
	textAll=textAll.replace('&nbsp','')
	textAll=textAll.replace('<c>','@')
	textAll=textAll.replace('<r>','@')
	#textAll=textAll.replace('[','@')
	textAll=re.sub(r'@.*','@',textAll)
	textAll=textAll.replace('@\n','')
	textAll=re.sub(r'<[^>]*>','',textAll)
	return textAll

def save(sender):
	f = open(pathSave+'_pref.txt',"w")
	pickle.dump(Pref, f)
	f.close()	
		
	#textIn.text is unicode, it is need convert it in utf-8
	#need rewrite with codecs 
	js='readText()'
	if(mainDictView.x==0):
		textAll=dictView.eval_js(js)
		textAll='{}'.format(textAll)
		saveDict(textAll)
		return
	
	textAll=textIn.eval_js(js)
	#textIn.text is unicode, it is need convert it in utf-8
	textAll='{}'.format(textAll)
	saveDict(textAll)

def clearSearch(sender):
	searchText.text=''
		
def closeDictView(sender):
	if(len(dt.history)>0):
		dt.history.pop()
		if(len(dt.history)>0):
			searchText.text=dt.history[len(dt.history)-1]
			dt.history.pop()
			dictEntry()
		else:
			mainDictView.x=1024
	else:
		mainDictView.x=1024
	
def setCommentaryTag(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	with open(path,"r",newline="\n") as f:
		textFile=f.readlines()
												  
	for key in dk.keyList:
		key=key.rstrip('\n')
		dk.get(key)
		c=dk.res
		if('__' in c):
			i=0
			key=key.rstrip('་')
			for line in textFile:
				s=unicode(line)
				s=re.sub(u'[ _\d\ "	\'\*\(\)\{\}\[\]@•#\%\&༄༅༔༴༡༢༣༤༥༦༧༨༩༠༎།༑༈༌༐༏༼༽ऀ-ॿ]',u"་",s)
				s=re.sub(u'་[་]+',u"་",s)
				s='{}'.format(s)
				if(key in s):
					textFile[i]='#_'+textFile[i]
					break
				i+=1
	with open(path,"w") as f:
		f.writelines(textFile)
			
def buildSummary(sender):
	path=fileView['textfield1'].text
	path=pathMain+'{}'.format(path)
	res=''
	with open(path,"r") as f:
		for line in f:
			if('#' in line):
				res+=line	
	fileView['textfield1'].text='Dictionary/_res.txt'
	path=pathMain+'Dictionary/_res.txt'
	with open(path,"w") as f:
		f.write(res)
	openText()
	

def fileCopy(path1,path2):
	print (copy)
	f=open(path1, 'r',newline="\n")
	t=f.readlines()
	#print (len(t))
	f.close()
	f=open(path2, 'w',newline="\n")
	f.writelines(t)
	f.close()
	
def sortDict(name):
	print ('load {}'.format(name))
	with open(pathSave+'XML_DICT/'+name+'.txt') as f:
		str=f.read()
		f.close()
		str=str.replace('\r','\n')
		d=str.split('\n')
		print (len(d))
		d.sort()
		i=0
		s=list()
		l=''
		for line in d:
			i+=1
			line=line.replace('*','@')
			line=re.sub('[\n\r\t ]*$','',line)
			if(l==line):
				continue
			
			#print (line+'/')
			#print (len(line))
			#if(i==10):
				#break	
				
			l=line
			s.append(line+'\n')
		f=open(pathSave+'XML_DICT/'+name+'_new.txt', 'w')
		f.writelines(s)	
		f.close()
		print (len(s))
		print ('done')
		
def loadPref():
	global Pref
	p=pathSave+'_pref_dict.txt'
	try:
		io.open(p,'r')
	except IOError:
		savePref()
	with open(p,'r') as f:
		Pref=pickle.load(f)
	while len(Pref) < 5:
		Pref.append('')
	fileView['textfield1'].text=Pref[1]
	if(Pref[2]==''):
		Pref[2]='0'
	pageIndex.text=Pref[2]
		
def savePref():
	global Pref
	p=pathSave+'_pref_dict.txt'
	with open(p,'w') as f:
		pickle.dump(Pref,f)
