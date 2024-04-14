// install node.js through nvm: https://hackmd.io/@elzuoc/ryLptv-0a?utm_source=preview-mode&utm_medium=rec
// code runner: https://www.youtube.com/watch?v=LqXzpj2jfOU

// Task 1
function findAndPrint(messages, currentStation){
    // your code here
    let line_list={
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

    let current = Object.keys(line_list).find(key => line_list[key] === currentStation);
    let messages_n = {};
    for (let key in messages) {
        let value = messages[key];
        let stationNumber = Object.keys(line_list).find(station => value.includes(line_list[station]));
        // let stationName=Object.values(line_list).find(stationName => value.includes(stationName));
        let distance = Math.abs(stationNumber-current);

        if (0 < distance && distance < 1 && (current==="19" || stationNumber==="19")) {
            distance=999;
        }
        //value.includes() method returns true if the station name is found in the value string, otherwise false.
        //If a key is found where its corresponding station name is included in the value string, find() returns that key (station number). If no such key is found, find() returns undefined.
        messages_n[key] = parseFloat(distance);
    }
    let min=Math.min(...Object.values(messages_n)); //Math用來計算單個數字，Object.values回傳array，因此要加...隔開
    console.log(Object.keys(messages_n).find(key => messages_n[key]===min));
}
const messages={
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Leslie":"I'm at home near Xiaobitan station.",
    "Vivian":"I'm at Xindian station waiting for you."
};
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian



// Task 2
// your code here, maybe
// 1. create empty template for 24 hours available consultant list
const schedule={};
for (let n = 0; n <=23; n++) {
    schedule[n]=[];
}

function book(consultants, hour, duration, criteria){
    // your code here
    // 2. Extract names and sort by price or rate (criteria)
    const sortedNames = consultants
        .map(consultant => consultant.name) // Extract names
        // Sort by criteria: http://www.eion.com.tw/Blogger/?Pid=1170、https://dotblogs.com.tw/lance_blog/2019/03/07/201504
        .sort((name1, name2) => {
            const consultant1 = consultants.find(consultant => consultant.name === name1);
            const consultant2 = consultants.find(consultant => consultant.name === name2);
            if(criteria==="price"){
                return consultant1[criteria] - consultant2[criteria];
            }else{
                return consultant2[criteria] - consultant1[criteria];
            }
        });
    
    // 3. update consultants in the template
    // Collect all names into a single array
    const allNames = Object.values(schedule).flatMap(names => names);

    // Convert the array into a Set to remove duplicates
    const unique = [...new Set(allNames)];

    // if consultants doesn't exist in the schedule list, then put it into the schedule
    for(let newName of sortedNames){
        if(!unique.includes(newName)){
            for (let n = 0; n <=23; n++) {
                schedule[n].push(newName);
            }
        }
    }
    // console.log(schedule);

    // 4. find if the consultant of sortedNames is available in the wanted hour
    let total=0;
    for(let ideal of sortedNames){
        let empty_pr=0;
        for(let h = hour; h < (hour+duration); h++){
            // 若任意時段想要的consultant沒空則跳出迴圈
            if(!schedule[h].includes(ideal)){
                empty_pr=1;
                break;
            }
        }
        total+=empty_pr;

        if(empty_pr===0){
            console.log(ideal);
            // remove consultant from the member of schedule[h]
            for(let h = hour; h < (hour+duration); h++){
                schedule[h] = schedule[h].filter(member => member !== ideal);
            }
            // console.log(schedule);
            break;
        }
    }
    if(total===consultants.length){console.log("No Service")};
}

const consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
];
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John



// Task 3
function func(){
    // your code here
    let middle_list="";
    // 1. find middle name of all people
    // arguments object directly without declaring individual parameter names, and by removing unnecessary checks.
    for (let n = 0; n < arguments.length; n++) {
        let name=arguments[n];
        let middle_n = /*條件*/(name.length % 2 === 0) ? /*true*/ (name.length / 2) : /*false*/ Math.floor(name.length / 2);
        let middle=name[middle_n];
        middle_list=middle_list+name[middle_n];
        // console.log(name,middle_n,middle,middle_list);
    }

    const charMap = {}; //object
    
    // 2. Count occurrences of each character
    for (let char of middle_list) {
        charMap[char] = (charMap[char] || 0) + 1;
        //It checks if the current character char already exists as a key in the charMap. If it does, it increments the count of occurrences by 1.
        //If it doesn't exist (charMap[char] evaluates to undefined), it initializes the count to 0 before incrementing it by 1.
    }

    // 3. Filter out characters that occur only once
    const uniqueChars = Object.keys(charMap).filter(char => charMap[char] === 1);

    ///// final
    if(uniqueChars.length===1){
        console.log(arguments[middle_list.indexOf(uniqueChars[0])]); //find the position of uniqueChars[0] in middle_list
    }else{
        console.log("沒有");
    }
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安



// Task 4
function getNumber(index){
    // your code here
    let floor=Math.floor(index/3);
    let mod=index%3;
    result=7*floor+4*mod;
    console.log(result);
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70