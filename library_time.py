def monthe_len(date): # מקבל תאריך, מחזיר את מספר הימים בחודש
    if date[1] == 1 or date[1] == 3 or date[1] == 5 or date[1] == 7 or date[1] == 8 or date[1] == 10 or date[1] == 12 :
        monthe_len = 31
    elif date[1] == 4 or date[1] == 6 or date[1] == 9 or date[1] == 11 :
        monthe_len = 30
    else:
        if date[0] % 4 == 0 or (date[0] % 100 == 0 and date[0] % 400 == 0):
            monthe_len = 29
        else:
            monthe_len = 28

    return monthe_len



def next_day_count(date, days): # מקבל תאריך וקפיצה של כמה ימים, מחזיר את התאריך אחרי הקפיצה

    monthe_start_len = monthe_len(date)
    day_start = date[2]
    monthe_start = date[1]
    year_start = date[0]
    check_next_monthe = (date[0],date[1] + 1,1)
    next_monthe_len = monthe_len(check_next_monthe)
    
    if days <= 0 :
        print('Invalid days number')
        return  None
    elif day_start + days <= monthe_start_len :
        return_date = day_start + days
    else:
        count = monthe_start_len - day_start
        return_date = days - count 
        if return_date > next_monthe_len :
            print('return date too far \nCheck book type')
            return None
        else :
            if monthe_start != 12:
                monthe_start += 1    
            else :
                monthe_start = 1
                year_start += 1
            
    return (year_start,monthe_start,return_date)


import calendar

def day_in_the_week(year, monthe, day):
    today = calendar.weekday(year, monthe, day)
    if today == 0 :
        return 'Monday'
    elif today == 1 :
        return 'Tuesday'
    elif today == 2 :
        return 'Wednesday'
    elif today == 3 :
        return 'Thursday'
    elif today == 4 :
        return 'Friday'
    elif today == 5 :
        return 'Saturday'
    elif today == 6 :
        return 'Sunday'

def year_len(year): # מקבל שנה ומחזיר את מספר הימים
    if year % 4 == 0 or (year % 100 == 0 and year % 400 == 0):
        year_len = 366
    else:
        year_len = 365
    return year_len



def day_count(date1, date2): # מקבל 2 תאריכים ומחזיר את מספר הימים בינהם

    monthe_start_len = monthe_len(date1)
    day_start = date1[2]
    monthe_start = date1[1]
    year_start = date1[0]
    day_end = date2[2]
    monthe_end = date2[1]  
    year_end = date2[0]

    if date1[1] == date2[1] and date1[0] == date2[0] : # אותו חודש באותה שנה
        count = date2[2] - date1[2]
     
    elif date1[0] == date2[0]: # אותה שנה חודש שונה
        if date1[1]+1 ==date2[1]: # חודש עוקב
            count = (monthe_start_len - day_start) + day_end
        else : # לא חודש עוקב
            days = 0
            for mon in range(monthe_start+1, monthe_end):
                leng = monthe_len((1,mon,year_start))
                days += leng
            count = (monthe_start_len - day_start) + days + day_end
    
    else: # שנה שונה
        days = monthe_start_len - day_start # ימים של החודש הראשון
        for mon in range(monthe_start+1, 13): # המשך החודשים של השנה הראשונה עד דצמבר
            leng = monthe_len((1,mon,year_start))
            days += leng
        for year in range(year_start+1, year_end): # חישוב השנים בין הראשונה לאחרונה
            years = year_len(year)
            days += years
        for mon in range(1, monthe_end): # הימים של השנה האחרונה
            leng = monthe_len((1,mon,year_end))
            days += leng 
        count = days + day_end  

    return count


if __name__ == '__main__' :
    print('-----------------')
    print("Basic test " )
    print("Expected result is: 5.3.22 " )
    print("Actual result is:")
    print(next_day_count((2022,2,27), 6)) 
    print('----') 
    print("test 2 - check  45 days jump" )
    print('Expected result is: Error printing')
    print("Actual result is:")     
    print(next_day_count((2022,2,27), 45))
    print('----') 
    print("test 3 - check  0 days jump" )
    print('Expected result is: Error printing')
    print("Actual result is:")       
    print(next_day_count((2022,2,27), 0)) 
    print('----') 
    print("test 4 - check year passing" )
    print("Expected result is: 2.1.23 " )
    print("Actual result is:")      
    print(next_day_count((2022,12,27), 6))  
    print('----')     
    print("test 5 - 1 days jump" )
    print("Expected result is: 1.5.22 " )
    print("Actual result is:")      
    print(next_day_count((2022,4,30), 1))  
    print('----')     
    print("test 6 - 1 days jump on end of february" )
    print("Expected result is: 1.3.22 " )
    print("Actual result is:")      
    print(next_day_count((2022,2,28), 1))  
    print('----') 
    print("test 7 - day_in_the_week for 21,3,22" )
    print("Expected result is: Monday" )
    print("Actual result is:")
    print(day_in_the_week(2022, 3, 21))
    print('-----------------')    