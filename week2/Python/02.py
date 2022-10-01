def avg(data):

    #變數設置
    total_salary = 0
    average_salary = 0
    n = 0

    #判斷員工數是否為0
    if (data["employees"] != 0):

        #利用for迴圈拿出列表中的字典
        for i in data["employees"]:
            name = i["name"]
            managers = i["manager"]
            salary = i["salary"]

            #判斷 manager 是否為 False 後 計算False員工個數與總薪資
            if(managers == False):
                n = n + 1
                total_salary = total_salary + salary

            #計算平均薪資
            average_salary = total_salary / n
        
        print("average_salary = ", average_salary)

    else:
        print("average_salary = ", average_salary)

            
                
    
    
avg({
    "employees": [
        {
            "name": "John",
            "salary": 30000,
            "manager": False
        },
        {
            "name": "Bob",
            "salary": 60000,
            "manager": True
        },
        {
            "name": "Jenny",
            "salary": 50000,
            "manager": False
        },
        {
            "name": "Tony",
            "salary": 40000,
            "manager": False
        }
    ]
})