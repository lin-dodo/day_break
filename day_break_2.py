import time,datetime,MySQLdb
from pylab import*

conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="chaodata",charset="utf8")  
cursor = conn.cursor()  
sql="select * from if888_m2 where Date >='2010-1-1' and Date <='2013-1-1';"
m=cursor.execute(sql)
print m
row=cursor.fetchall()
start_time=row[0][2]
mid_time=datetime.timedelta(0, 54000)#15:00:00
end_time=row[-1][2]
def Open(i):
        return row[i][3]
def High(i):
        return row[i][4]
def Low(i):
        return row[i][5]
def Close(i):
        return row[i][6]
def Time(i):
        return row[i][2]
def Date(i):
        return row[i][0]
def return_day(i):
        a=i-200
        if a<0:
                a=0
        b=i+200
        if b>m:
                b=m
        if i<0:
                i=0
        if i>m-1:
                i=m-1
        n=[]
        for j in range(a,b):
                if cmp(Date(j),Date(i))==0:
                        n.append(j)
        return n
day=len(return_day(0))
high_d=[]
close_d=[]
open_d=[]
low_d=[]
l=0

while(l<m):
        
        a=return_day(l)
        #print str(len(a))+'\n'
        b=[]
        c=[]
        for j in a:
                close_d.append(Close(a[-1]))
                open_d.append(Open(a[0]))
                b.append(High(j))
                c.append(Low(j))
        high=max(b)
        low=min(c)
        for z in a:
                high_d.append(high)
                low_d.append(low)
        l=len(high_d)
def openD(i):
        if i<0:
                i=0
        return open_d[i]
def closeD(i):
        if i<0:
                i=0
        return close_d[i]
def lowD(i):
        if i<0:
                i=0
        return low_d[i]
def highD(i):
        if i<0:
                i=0
        return high_d[i]

def day_break(list_f):
                
        
        stop_percent=0.005
        profit=[]
        totalprofit=[]
        entry_price=[]
        exit_price=[]
        Lots=1
        entry_count=-1
        exit_count=-1
        con=0
        day_con=0
        status=0
        for i in range(0,m):
                
                if i>=day*13:
                        
                        
                        #print openD(0)
                        start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                        time=start.strftime("%H:%M:%S")
                        if con==0 and Time(i)==start_time:
                                
                                #print openD[0]
                                s=0
                                dd=Date(i)
                                for num in range(0,10):
                                        dd2=Date(i-day*(1+num))
                                        dd3=Date(i-day*(2+num))
                                        a=max(highD(i-day*(1+num)),closeD(i-day*(2+num)))
                                        b=min(lowD(i-day*(1+num)),closeD(i-day*(2+num)))
                                        s=s+(a-b)
                                avetruerange=s/10.0
                                truehigh=max(highD(i-day),closeD(i-day*2))
                                truelow=min(lowD(i-day),closeD(i-day*2))
##                                for num in range(0,10):
##                                        a=max(High(i-(1+num)),Close(i-(2+num)))
##                                        b=min(Low(i-(1+num)),Close(i-day*(2+num)))
##                                        s=s+(a-b)
##                                avetruerange=s/10.0
##                                truehigh=max(High(i-1),Close(i-2))
##                                truelow=min(Low(i-1),Close(i-2))
                                truerange=truehigh-truelow
                                
                                f=list_f[0]*openD(i-day)+list_f[1]*highD(i-day)+list_f[2]*lowD(i-day)+list_f[3]*closeD(i-day)+list_f[4]*closeD(i-day*2)
                                f=f+list_f[5]*truehigh+list_f[6]*truelow+list_f[7]*truerange+list_f[8]*avetruerange
                                #print f
##                                print Open(i),1,Date(i),Time(i)
##                                print openD(i),2
                                up=round((openD(i)+f),2)
                                down=round((openD(i)-f),2)
                                ooo=openD(i)
                                #print up,ooo,down,Date(i)
                                con=1
                        if High(i)>up and day_con==0 and Time(i)<mid_time:
                                if status==0:
                                        
                                        #entry_count=entry_count+1
                                        entry_price_temp=((round(max(up,Open(i))/0.2,0)+1)*0.2)
                                        print Date(i),Time(i),"buy",entry_price_temp
                                        entry_price.append(entry_price_temp)
                                        entry_time=Time(i)

                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                        status=1
                                        day_con=1
                        if Low(i)<down and day_con==0 and Time(i)<mid_time:
                                if status==0:
                                        entry_price_temp=(round(min(down,Open(i))/0.2,0)*0.2)
                                        print Date(i),Time(i),"sell",entry_price_temp
                                        #entry_count=entry_count+1
                                        entry_time=Time(i)
                                        entry_price.append(entry_price_temp)
                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                        status=-1
                                        day_con=1
                        if  status==1:
                                stop=round((1-stop_percent)*entry_price[-1],2)
                                if Low(i)<stop and cmp(Time(i),entry_time)!=0:
                                        exit_price_temp=(int((min(Open(i),stop)/0.2)))*0.2
                                        exit_price.append(exit_price_temp)
                                        profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                        print Date(i),Time(i),"ping",exit_price_temp
                                        totalprofit.append(sum(profit))
                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                        status=0
                                        #day_con=1
                        if  status==-1:
                                stop=round((1+stop_percent)*entry_price[-1],2)
                                if High(i)>stop and cmp(Time(i),entry_time)!=0: 
                                        #exit_count=exit_count+1
                                        exit_price_temp=(int((max(Open(i),stop)/0.2))+1)*0.2
                                        exit_price.append(exit_price_temp)
                                        profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                        print Date(i),Time(i),"ping",exit_price_temp
                                        totalprofit.append(sum(profit))
                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                        status=0
                                        #day_con=1
                        if cmp(time,"15:00:00")==0:
                                
                                con=0
                                #day_con=0
                                if status==1:
                                        exit_price.append(Close(i))
                                        profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                        print Date(i),Time(i),"ping"
                                        totalprofit.append(sum(profit))
                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                        status=0
                                
                                if  status==-1:
                                        #exit_count=exit_count+1
                                        exit_price.append(Close(i))
                                        profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                        print Date(i),Time(i),"ping"
                                        totalprofit.append(sum(profit))
                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                        status=0
                        if Time(i)==end_time:
                                day_con=0
        print totalprofit[0]
        x=range(0,len(totalprofit))
        plot(x,totalprofit)
        show()                                       
        if len(totalprofit)>0:
                print len(totalprofit)
                return totalprofit[-1]

        
print day_break([-0.33,0.65,0.31,-1.24,0.81,-0.98,0.79,0.52,1.21])
##print day_break([0.273576, 2, -1.223193, -1.134341, -0.049424, 1.24246, -1.227709, 2, 0.820992])
'''print day_break([-2.0, 1.6970229326477577, -2.0, 0.6233161655684559, 0.5073484430681212, -0.16543662444872242, 1.3180439637248584,1.75748918725767, 0.43931606628460784])'''
cursor.close()
conn.close()

