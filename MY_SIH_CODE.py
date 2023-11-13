import requests
import json
import time
from datetime import datetime
FMT = '%H:%M:%S'
f = open('ALL_Train_Schedule.json',) 
trn_sch = json.load(f) 
f=open('All_train_from_a_station.json')
all_trn=json.load(f)
f=open('train_arr_dept.json')
trn_arr_dept=json.load(f)
f=open('All_Station_Nearbuy.json')
stat_neig=json.load(f)
f=open('station_code_to_name.json')
code_to_name=json.load(f)
f=open('station_name_to_code.json')
name_to_code=json.load(f)

class Book_Ticket():
    routes=[]
    final_routes=[]
    def __init__(self,src,dest,date=None,train_type=None,day=None):
        self.source=src
        self.destination=dest
        self.src=self.station_name_to_code(src.upper())  #station code call
        self.dest=self.station_name_to_code(dest.upper()) 
        if self.src=="NOT" or self.dest=="NOT":  #IF STATION CODE NOT FOUND
            print("______________________________Check Your Staion Name Again________________________________")
    def display(self):
        #print("NO. OF POSSIBLE ALTERNATE ROUTE USING 1 STOPOVER =",len(self.final_routes))
        #counter=1
        #for i in self.final_routes:
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #print()
            #part1=i[0]
            #part2=i[1]
            #print("Route-",counter)
            #print()
            #print(code_to_name[part1[1][0]],"-------->",code_to_name[part1[1][1]])
            #print("Train No-",part1[0])
            #print("-------------------------------------------------------")
            #print()
            #print(code_to_name[part2[1][0]],"-------->",code_to_name[part2[1][1]])
            #print("Train No-",part2[0])
            #print()
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #counter+=1
    
        rtn_dict=dict()
        counter=1
        for i in self.final_routes:
            key="Route "+str(counter)
            rtn_dict[key]=dict()
            part1=i[0]
            part2=i[1]
            key_pass1=part1[1][0]+part1[1][1]
            rtn_dict[key][key_pass1]=dict()
            rtn_dict[key][key_pass1]['train_no']=part1[0]
            rtn_dict[key][key_pass1]['train_type']="Express"
            rtn_dict[key][key_pass1]['src']=code_to_name[part1[1][0]]
            rtn_dict[key][key_pass1]['dest']=code_to_name[part1[1][1]]
            rtn_dict[key][key_pass1]['dep_time_at_src']=trn_arr_dept[part1[0]][part1[1][0]][0]
            rtn_dict[key][key_pass1]["arr_time_at_dest"]=trn_arr_dept[part1[0]][part1[1][1]][0]
            rtn_dict[key][key_pass1]["route_dist"]=0
            key_pass1=part2[1][0]+part2[1][1]
            rtn_dict[key][key_pass1]=dict()
            rtn_dict[key][key_pass1]['train_no']=part2[0]
            rtn_dict[key][key_pass1]['train_type']="Express"
            rtn_dict[key][key_pass1]['src']=code_to_name[part2[1][0]]
            rtn_dict[key][key_pass1]['dest']=code_to_name[part2[1][1]]
            rtn_dict[key][key_pass1]['dep_time_at_src']=trn_arr_dept[part2[0]][part2[1][0]][1]
            rtn_dict[key][key_pass1]["arr_time_at_dest"]=trn_arr_dept[part2[0]][part2[1][1]][0]
            rtn_dict[key][key_pass1]["route_dist"]=0
            counter+=1
        print(rtn_dict)
    def train_no_to_station(self,trn_num):
        return [i[0] for i in trn_sch[trn_num]]
    def train_between_station(self,src,dest):
        final=[]
        #src= source staion code
        #dest= destination station code
        temp=list(set(all_trn[src]).intersection(set(all_trn[dest])))
        for i in temp:
            jun_list=self.train_no_to_station(i)
            if jun_list.index(src)<jun_list.index(dest):
                final.append(i)
        return final
    def station_name_to_code(self,name,flag=0):
        #url =" http://indianrailapi.com/api/v2/StationNameToCode/apikey/0fe3b963408929419d6d519b06fd4110/StationName/"+name+"/"
        #response = requests.get(url)
        # print(response) successfully
        #data=response.text
        # print(data[])
        #parsed=json.loads(data)
        #print(json.dumps(parsed, indent=4))
        #code=parsed['Station']['StationCode']
        try:
            #print(flag)
            if flag==0:
                code=name_to_code[name]
                #print(code)
                return code
            if flag==1:
                code=name_to_code[name]
                #print(code)
                return code
        except:
            if flag==1:
                return "NOT"
            name2=name.upper()+" "+"JN"
            flag=1
            return self.station_name_to_code(name2,flag)
    
    def poss_station(self):
        #src_stat=[self.train_no_to_station(i) for i in all_trn[self.src]]
        #dest_stat=[self.train_no_to_station(i) for i in all_trn[self.dest]]
        #src_stat_set=set()
        #dest_stat_set=set()
        #for i in src_stat:
            #for j in i:
                #src_stat_set.add(j)
        #for i in dest_stat:
            #for j in i:
                #dest_stat_set.add(j)
        src_stat_set=set(stat_neig[self.src])
        dest_stat_set=set(stat_neig[self.dest])
        final_set=src_stat_set.intersection(dest_stat_set)
        if self.src in final_set:
            final_set.remove(self.src)
        if self.dest in final_set:
            final_set.remove(self.dest)
        return list(final_set)
    
    def alternate_train(self):
        inter_stat=self.poss_station()
        for i in inter_stat:
            self.create_tuple(i)
        for i,j in self.routes:
            #print("_________MAIN LOOP___________")
            trn_list_p1=self.train_between_station(i[0],i[1])
            trn_list_p2=self.train_between_station(j[0],j[1])
            #trn_list_p1=
            #trn_list_p2=list(set(all_trn[j[0]]).intersection(set(all_trn[j[1]])))
            if trn_list_p1==None:
                continue
            if trn_list_p2==None:
                continue
            #print(trn_list_p1)
            for t in trn_list_p1:
                #print("LOOP1")
                #print(t)
                try:
                    arr,dept=trn_arr_dept[t][i[1]] 
                    #print(arr,dept,end="$$$$$$$$\n")
                    for k in trn_list_p2:
                        if t==k:
                            continue
                        #print("LOOP2")
                        #print(k)
                        arr2,dept2=trn_arr_dept[k][i[1]]
                        #print(arr2,dept2,end="$$$$$$$$\n")
                        td = datetime.strptime(arr2, FMT) - datetime.strptime(arr, FMT)
                        #print("END_LOOP2")
                        days = td.days
                        hours, remainder = divmod(td.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        # If you want to take into account fractions of a second
                        seconds += td.microseconds / 1e6
                        if days==-1:
                            continue
                        if hours<4:
                            temp=[]
                            temp.append(t)
                            temp.append(i)
                            temp2=[]
                            temp2.append(k)   
                            temp2.append(j)
                            temp3=[]
                            temp3.append(temp)
                            temp3.append(temp2)
                            self.final_routes.append(temp3)
                    #if (len(self.final_routes))>=5:
                        #break
                except:
                    continue
                #print("END_LOOP1")
        self.display()
    def create_tuple(self,i):
        temp=[]
        temp2=[]
        temp.append(self.src)
        temp.append(i)
        temp2.append(i)
        temp2.append(self.dest)
        temp3=[]
        temp3.append(temp)
        temp3.append(temp2)
        self.routes.append(temp3)
    
cus65=Book_Ticket("New Delhi","Jaipur")
cus65.alternate_train()

#for i in intern
#source to intermediate = ["tr1","tr2","tr3"]
#intermediate to desti = ["tr5","tr6","tr7"]