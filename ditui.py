from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Selectors
from pyevolve import Initializators, Mutators
import pyevolve
import math
import time,datetime,MySQLdb
from pylab import*
start=time.time()
file_w=open('profit.txt','w')
conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="chaodata",charset="utf8")  
cursor = conn.cursor()  
sql="select * from IF888_M5 where Date >='2010-04-16' and Date <='2014-9-30';"
all_m=cursor.execute(sql)
all_row=cursor.fetchall()

def return_day():
        n=[]
        for j in range(0,60):
                if cmp(all_row[j][0],all_row[0][0])==0:
                        n.append(j)
        return n
day=len(return_day())


day_test=60
day_run=20

day_index_test=0
day_index_run=day*day_test-1
def run(list_f):
        global day_index_run
        
                
        #print day_index
        row=all_row[day_index_run:day_index_run+day*day_run]
        day_index_run=day_index_run+day*day_run-1
        m=len(row)
        print m/54.0     
        ##    for z in row:
        ##            print z
        ##       

        def Open(i):
                return row[i][3]
        def High(i):
                return row[i][4]
        def Low(i):
                return row[i][5]
        def Close(i):       
                return row[i][6]
        def Time(i):
                start=datetime.datetime(2014,1,1,0,0,0,0)+row[i][2]
                return start.strftime("%H:%M:%S")
        def Date(i):
                return row[i][0].strftime("%Y-%m-%d")
             

        def return_day_row(i):
                a=i-60
                if a<0:
                        a=0
                b=i+60
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
        high_d=[]
        close_d=[]
        open_d=[]
        low_d=[]
        l=0

        while(l<m):
            
            a=return_day_row(l)
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

                #global open_d
                return open_d[i]
        def closeD(i):
                #global close_d
                return close_d[i]
        def lowD(i):
                #global low_d
                return low_d[i]
        def highD(i):
                #global high_d
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
                                
                                if con==0:
                                        #print openD[0]
                                        s=0
                                        for num in range(0,10):
                                                a=max(highD(i-day*(1+num)),closeD(i-day*(2+num)))
                                                b=min(lowD(i-day*(1+num)),closeD(i-day*(2+num)))
                                                s=s+(a-b)
                                        avetruerange=s/10.0
                                        truehigh=max(highD(i-day),closeD(i-day*2))
                                        truelow=min(lowD(i-day),closeD(i-day*2))
                                        truerange=truehigh-truelow
                                        f=list_f[0]*openD(i-day)+list_f[1]*highD(i-day)+list_f[2]*lowD(i-day)+list_f[3]*closeD(i-day)+list_f[4]*closeD(i-day*2)
                                        f=f+list_f[5]*truehigh+list_f[6]*truelow+list_f[7]*truerange+list_f[8]*avetruerange
                                        
                                        up=Open(i)+f
                                        down=Open(i)-f
                                        ooo=Open(i)
                                        con=1
                                if High(i)>up and day_con==0:
                                        if status==0:
                                                #entry_count=entry_count+1
                                                entry_price.append(max(up,Open(i)))
                                                entry_time=Time(i)

                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                                status=1
                                                day_con=1
                                if Low(i)<down and day_con==0:
                                        if status==0:
                                                #entry_count=entry_count+1
                                                entry_time=Time(i)
                                                entry_price.append(min(down,Open(i)))
                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                                status=-1
                                                day_con=1
                                if  status==1:
                                        stop=(1-stop_percent)*entry_price[-1]
                                        if Low(i)<stop and cmp(Time(i),entry_time)!=0:
                                                exit_price.append(min(Open(i),stop))
                                                profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                                totalprofit.append(sum(profit))
                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                                status=0
                                                day_con=1
                                if  status==-1:
                                        stop=(1+stop_percent)*entry_price[-1]
                                        if High(i)>stop and cmp(Time(i),entry_time)!=0: 
                                                #exit_count=exit_count+1
                                                exit_price.append(max(Open(i),stop))
                                                profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                                totalprofit.append(sum(profit))
                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                                status=0
                                                day_con=1
                                if cmp(Time(i),"15:00:00")==0:
                                        
                                        con=0
                                        day_con=0
                                        if status==1:
                                                exit_price.append(Close(i))
                                                profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                                totalprofit.append(sum(profit))
                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                                status=0
                                        
                                        if  status==-1:
                                                #exit_count=exit_count+1
                                                exit_price.append(Close(i))
                                                profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                                totalprofit.append(sum(profit))
                                                #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                                status=0 
##                        x=range(0,len(totalprofit))
##                        plot(x,totalprofit)
##                        show()
##                        return totalprofit[-1]
                if len(totalprofit)>0:
                        return totalprofit[-1]
        return day_break(list_f)

def test():
        global day_index_test
        if day_index_test<all_row:
                
                #print day_index
                row=all_row[day_index_test:day_index_test+day*day_test]
                day_index_test=day_index_test+day*day_run-1
                m=len(row)
                print m/54.0
                #print m
                ##    for z in row:
                ##            print z
                ##       

                def Open(i):
                        return row[i][3]
                def High(i):
                        return row[i][4]
                def Low(i):
                        return row[i][5]
                def Close(i):       
                        return row[i][6]
                def Time(i):
                        start=datetime.datetime(2014,1,1,0,0,0,0)+row[i][2]
                        return start.strftime("%H:%M:%S")
                def Date(i):
                        return row[i][0].strftime("%Y-%m-%d")
                     

                def return_day_row(i):
                        a=i-60
                        if a<0:
                                a=0
                        b=i+60
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
                high_d=[]
                close_d=[]
                open_d=[]
                low_d=[]
                l=0

                while(l<m):
                    
                    a=return_day_row(l)
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

                        #global open_d
                        return open_d[i]
                def closeD(i):
                        #global close_d
                        return close_d[i]
                def lowD(i):
                        #global low_d
                        return low_d[i]
                def highD(i):
                        #global high_d
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
                                        
                                        if con==0:
                                                #print openD[0]
                                                s=0
                                                for num in range(0,10):
                                                        a=max(highD(i-day*(1+num)),closeD(i-day*(2+num)))
                                                        b=min(lowD(i-day*(1+num)),closeD(i-day*(2+num)))
                                                        s=s+(a-b)
                                                avetruerange=s/10.0
                                                truehigh=max(highD(i-day),closeD(i-day*2))
                                                truelow=min(lowD(i-day),closeD(i-day*2))
                                                truerange=truehigh-truelow
                                                f=list_f[0]*openD(i-day)+list_f[1]*highD(i-day)+list_f[2]*lowD(i-day)+list_f[3]*closeD(i-day)+list_f[4]*closeD(i-day*2)
                                                f=f+list_f[5]*truehigh+list_f[6]*truelow+list_f[7]*truerange+list_f[8]*avetruerange
                                                
                                                up=Open(i)+f
                                                down=Open(i)-f
                                                ooo=Open(i)
                                                con=1
                                        if High(i)>up and day_con==0:
                                                if status==0:
                                                        #entry_count=entry_count+1
                                                        entry_price.append(max(up,Open(i)))
                                                        entry_time=Time(i)

                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                                        status=1
                                                        day_con=1
                                        if Low(i)<down and day_con==0:
                                                if status==0:
                                                        #entry_count=entry_count+1
                                                        entry_time=Time(i)
                                                        entry_price.append(min(down,Open(i)))
                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(entry_price[-1])+"jin")
                                                        status=-1
                                                        day_con=1
                                        if  status==1:
                                                stop=(1-stop_percent)*entry_price[-1]
                                                if Low(i)<stop and cmp(Time(i),entry_time)!=0:
                                                        exit_price.append(min(Open(i),stop))
                                                        profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                                        totalprofit.append(sum(profit))
                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                                        status=0
                                                        day_con=1
                                        if  status==-1:
                                                stop=(1+stop_percent)*entry_price[-1]
                                                if High(i)>stop and cmp(Time(i),entry_time)!=0: 
                                                        #exit_count=exit_count+1
                                                        exit_price.append(max(Open(i),stop))
                                                        profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                                        totalprofit.append(sum(profit))
                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping")
                                                        status=0
                                                        day_con=1
                                        if cmp(Time(i),"15:00:00")==0:
                                                
                                                con=0
                                                day_con=0
                                                if status==1:
                                                        exit_price.append(Close(i))
                                                        profit.append((exit_price[-1]-entry_price[-1])*Lots*300-23)
                                                        totalprofit.append(sum(profit))
                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                                        status=0
                                                
                                                if  status==-1:
                                                        #exit_count=exit_count+1
                                                        exit_price.append(Close(i))
                                                        profit.append((entry_price[-1]-exit_price[-1])*Lots*300-23)
                                                        totalprofit.append(sum(profit))
                                                        #start=datetime.datetime(2014,1,1,0,0,0,0)+Time(i)
                                                        #write(Date(i).strftime("%Y-%m-%d")+" "+start.strftime("%H:%M:%S")+" "+str(exit_price[-1])+"ping_rimo")
                                                        status=0 
                        if len(totalprofit)!=0:
                                return totalprofit[-1]+100000000
                        else:
                                return 100000000
                
                genome = G1DList.G1DList(9)
                genome.setParams(rangemin=-2.0, rangemax=2.0)
                genome.initializator.set(Initializators.G1DListInitializatorReal)
                genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

                #genome.crossover.clear()
                # The evaluator function (objective function)
                genome.evaluator.set(day_break)
                #genome.evaluator.add(func_1)

                # Genetic Algorithm Instance
                ga = GSimpleGA.GSimpleGA(genome)
                ga.selector.set(Selectors.GRouletteWheel)
                ga.setMutationRate(0.98)
                ga.setPopulationSize(50)
                #ga.setCrossoverRate(0.8)
                ga.setGenerations(100)
                #ga.stepCallback.set(evolve_callback)

                # Do the evolution
                ga.evolve(10)
                best=ga.bestIndividual()
                
                return best.genomeList
while(day_index_run<all_m):
        
        p=run(test())
        file_w.write(str(p)+'\n')
        print p
cursor.close()
conn.close()
file_w.close()
end=time.time()
print end-start
