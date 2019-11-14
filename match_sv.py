import os
import csv
import sys
import uuid

infile1=sys.argv[1]#BD file
infile2=sys.argv[2]#CRS filtered file

randCode=str(uuid.uuid4()).split('-')[0]

com1='grep -v "^#" '+infile1+' |cut -f1,2,4,5,7|sort> '+randCode+'_tmp_breakdancer_noHeader'
os.system(com1)
BD=list(csv.reader(open(randCode+'_tmp_breakdancer_noHeader','rb'),delimiter='\t'))
CRS=list(csv.reader(open(infile2,'rb'),delimiter='\t'))

Pos=[]
output=[]
for i in BD:
	chrBD1=i[0]
	chrBD2=i[2]
	range_insert=[]
	upper1=int(i[1])+1000000
	lower1=int(i[1])-1000000
	if lower1<0:
		lower1=0
	upper2=int(i[3])+1000000
        lower2=int(i[3])-1000000
        if lower2<0:
                lower2=0
	for j in CRS:
		chrCRS1=j[3].strip('chr')
		chrCRS2=j[8].strip('chr')
		ind=CRS.index(j)
		v1=''
		v2=''
		if int(j[4])>lower1 and int(j[4])<upper1\
and int(j[9])>lower2 and int(j[9])<upper2:
			if chrBD1==chrCRS1 and chrBD2==chrCRS2:
				diff1=str(abs(int(i[1])-int(j[4])))
				diff2=str(abs(int(i[3])-int(j[9])))
				v1='validated'+';'+i[4]+';'+j[4]+';'+j[9]+';'+i[1]+'('+diff1+');'+i[3]+'('+diff2+')'
				del CRS[ind]
		
		o='\t'.join(j)+'\t'+str(v1)
		output.append(o)

outfile1=open(randCode+'_tmp_outfile','w')

output=list(set(output))
for ele in output:
	outfile1.write('%s\n' % ele)
outfile1.close()
file3=list(csv.reader(open(randCode+'_tmp_outfile','rb'),delimiter='\t'))
for i in file3:
	if i[-1].startswith('validated'):
		print '\t'.join(i)
	else:
		pass

