# X in 集合
# 集合1&集合2: 交集
# 集合1|集合2: 聯集，不重複取
# 集合1-集合2: 差集
# 集合1^集合2: 反交集，取不重疊的部分
# set(字串): 把字串字母拆解成集合
# dic["key"] 印出"蘋果"
# "apple" in dic
# del dic["apple"]
# dic={x:x*2 for x in 列表} 從列表的資料產生字典

# Task 1
def find_and_print(messages, current_station):
    # your code here
    line_list={
        1:"Songshan",
        2:"Nanjing",
        3:"Nanjing Sanmin",
        4:"Taipei Arena",
        5:"Nanjing Fuxing",
        6:"Songjiang Nanjing",
        7:"Zhongshan",
        8:"Beimen",
        9:"Ximen",
        10:"Xiaonanmen",
        11:"Chiang Kai-Shek Memorial Hall",
        12:"Guting",
        13:"Taipower Building",
        14:"Gongguan",
        15:"Wanlong",
        16:"Jingmei",
        17:"Dapinglin",
        18:"Qizhang",
        18.1:"Xiaobitan",
        19:"Xindian City Hall",
        20:"Xindian"
    }
    # current = next(key for key, value in line_list.items() if value == current_station)
    current = None
    for key, value in line_list.items():
        if value == current_station:
            current = key
            break

    messages_n = {}
    for key, value in messages.items():
        stationNumber = None
        for station, stationName in line_list.items():
            if stationName in value:
                stationNumber = station
                break

        distance = abs(float(stationNumber) - float(current))

        if 0<distance<1 and (current==19 or stationNumber==19):
            distance = 999

        messages_n[key]=float(distance)
    
    # get the key with minimum value in messages_n
    output=min(messages_n, key=messages_n.get)
    print(output)
    
messages={
    "Leslie":"I'm at home near Xiaobitan station.",
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Vivian":"I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian



# Task 2
# your code here, maybe
# 1. create empty template for 24 hours available consultant list
schedule={hour: [] for hour in range(0,24)}
# schedule = {n: list(consultant_list) for n in range(24)}

def book(consultants, hour, duration, criteria):
    # your code here
    # 2. Extract names and sort by price or rate (criteria)
    if criteria=="price":
        sorted_consultants = sorted(consultants, key=lambda x: x["price"])
    else:
        sorted_consultants = sorted(consultants, key=lambda x: x["rate"],reverse=True)
    sortedNames=[x["name"] for x in sorted_consultants]

    # 3. update consultants in the template
    unique=set(value for values_list in schedule.values() for value in values_list)
    # if consultants doesn't exist in the schedule list, then put it into the schedule
    for new in sortedNames:
        if new not in unique:
            for h in range(0,24):
                schedule[h].append(new)

    # 4. find if the consultant of sortedNames is available in the wanted hour
    total=0
    for ideal in sortedNames:
        empty_pr=0
        for h in range(hour, hour+duration):
            if ideal not in schedule[h]:
                empty_pr=1
                break
        total+=empty_pr

        if empty_pr==0:
            print(ideal)
            # remove ideal from schedule[h]
            for h in range(hour, hour+duration):
                schedule[h].remove(ideal)
                # print(schedule)
                # print(hour, duration, criteria)
            break
    
    if total==len(consultants):
        print("No Service")

consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John



# Task 3
def func(*data):
    # your code here
    # 1. find middle name of all people
    middle_list=""
    for i in range(len(data)):
        if len(data[i])%2==0:
            m=int(len(data[i])/2) #要int
        else:
            m=len(data[i])//2
        middle=data[i][m]
        middle_list=middle_list+middle

    # 2. Count occurrences of each character
    frequency={}
    for char in middle_list:
        if char in frequency:
            frequency[char]+=1
        else:
            frequency[char]=1

    # 3. Find out the index of the characters that occur only once
    # if any(value==1 for value in frequency.values()):
    # enumerate(): https://codeshiba.com/2023/12/04/python/enumerate/
    x=None
    for key, value in frequency.items():
        if value==1:
            x=middle_list.index(key)

    ###### final
    if x is not None:
        print(data[x])
    else:
        print("沒有")
    
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安



# Task 4
def get_number(index):
    # your code here
    floor = index // 3 # //: 無條件捨去
    mod = index % 3
    result = 7 * floor + 4 * mod
    print(result)

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70