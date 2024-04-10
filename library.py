from datetime import datetime
import library_time as lt
from books import Books
from customers import Customers
from loans import Loans
import json
import pickle

now = datetime.now()
today = (now.year, now.month, now.day)

class Library:
    def __init__(self):
        self.book_li = {}
        self.customer_li = {}
        self.loans = {}
        self.num_of_customers_created = 0
        self.available_copies = {}
        self.limited_accounts = {}
        self.counter = 100
        

    def limited_accounts_check(self):
        unlimited = []
        for account in self.limited_accounts:
            if self.limited_accounts[account] <= today:
                unlimited.append(account)
        for id in unlimited :
           self.limited_accounts.pop(id) 


    def add_new_customer(self, name, city, birth_date) :
        self.num_of_customers_created += 1
        self.customer_id = '%05d' % self.num_of_customers_created
        new_customer = Customers(self.customer_id, name, city, birth_date)
        self.customer_li[new_customer.customer_id] = {'customer_id': new_customer.customer_id, 'name': new_customer.name, 'city': new_customer.city, 'birth_date': new_customer.birth_date, 'customer_loans': 0}
        print(f"{name} has been added to the library\nHis/Hers ID number is {self.customer_id}")


    def add_new_book(self, name, author, year_published, type, num_of_copies=1):
        if name in self.book_li :
            self.book_li[name]['num_of_copies'] += num_of_copies
            self.available_copies[name] += num_of_copies
            print(f"{name} already exists in the library\nThe number of copies has been updated")
        else :
            new_book = Books(name, author, year_published, type, num_of_copies)
            self.book_li[new_book.name] = {'name': new_book.name, 'author': new_book.author, 'year_published': new_book.year_published, 'type': new_book.type, 'num_of_copies': new_book.num_of_copies, 'maximum_loan_dayes': new_book.maximum_loan}
            self.available_copies[new_book.name] = new_book.num_of_copies
            print(f"{name} has been added to the library")


    def limited_customers(self,customer_id):
        if customer_id in self.limited_accounts:
            return True
        else:
            return False


    def loan_a_book(self, customer_id, book_name):
        if self.customer_li[customer_id]['customer_loans'] > 0:
            for loan in self.loans :
                if self.loans[loan]['customer_id'] == customer_id:
                    if self.loans[loan]['returndate'] < today:
                        print('The customer exceeded the loan time\nReturn the book ASAP')
                        return None

        if self.customer_li[customer_id]['customer_loans'] >= 3 :
            print('The customer loan the maximum number of books\nReturn a book to loan a new one')
            return None

        if self.limited_customers(customer_id):
            print(f"The customer's account is blocked until {self.limited_accounts[customer_id][::-1]}")
            return None
        
        if self.available_copies[book_name] == 0 :
            next_re = []
            for lone in self.loans :
                if self.loans[lone]['book_name'] == book_name:
                    if self.loans[lone]['returndate'] > today:
                        next_re.append((self.loans[lone]['returndate']))
            next_re.sort()       
            next_return = next_re[0]
            print(f'There are no available copies for this book.\n1 Copy should return on {next_return[::-1]}')
            return None
        else:
            new_lone = Loans(customer_id, book_name, loandate = today)
            max_loan = self.book_li[new_lone.book_name]['maximum_loan_dayes']
            returndate = lt.next_day_count(new_lone.loandate, max_loan)
            if lt.day_in_the_week(returndate[0],returndate[1],returndate[2]) == 'Saturday':
                returndate = lt.next_day_count((returndate), 1)
            self.counter += 1
            loan_key =  f"L{now.day}{now.month}{self.counter}"
            self.loans[loan_key] = {'customer_id': new_lone.customer_id, 'book_name':new_lone.book_name, 'loandate': new_lone.loandate, 'returndate': returndate}
            self.available_copies[new_lone.book_name] -= 1
            self.customer_li[new_lone.customer_id]['customer_loans'] += 1
            if self.counter == 999:
                self.counter = 100

                 
    def return_a_book(self, customer_id, book_name):
        returned = 0
        for lone in self.loans :
                if self.loans[lone]['customer_id'] == customer_id and self.loans[lone]['book_name'] == book_name:
                    if self.loans[lone]['returndate'] < today:
                        can_lone_again = lt.next_day_count((today), 14)
                        self.limited_accounts[customer_id] = can_lone_again
                        print(f"The customer was late returning this book.\nHis account is blocked until {can_lone_again[::-1]}")
                    returned = lone
                    self.customer_li[customer_id]['customer_loans'] -= 1
                    self.available_copies[book_name] += 1
        
        self.loans.pop(returned)


    def display_all_books(self):
        a_to_z_book_list = []
        for book in self.book_li:
            a_to_z_book_list.append(self.book_li[book]['name'])

        a_to_z_book_list.sort()
        for book in a_to_z_book_list:
            print(f"""
            ---------------
            Book name: {self.book_li[book]['name']}
            Author: {self.book_li[book]['author']}
            Published on: {self.book_li[book]['year_published']}
            Number of copies in the library: {self.book_li[book]['num_of_copies']}
            Number of available copies: {self.available_copies[book]}
            Book type: {self.book_li[book]['type']}
            Maximum loan time: {self.book_li[book]['maximum_loan_dayes']} days
            ---------------
            """)
    
    
    def Display_all_customers(self):
        answer = ""
        for customer in self.customer_li:
            print(f"""
            ---------------
            Customer id number: {self.customer_li[customer]['customer_id']}
            Customers name: {self.customer_li[customer]['name']}
            Customer address: {self.customer_li[customer]['city']}
            Customers birth date: {self.customer_li[customer]['birth_date']}
            Customer current loans: {self.customer_li[customer]['customer_loans']}""")
            if self.limited_customers(self.customer_li[customer]['customer_id']):
                answer = "Yes"
            else:
                answer = "No" 
            print(f"""            Is the customer account limited? {answer}
            ---------------""")
           

    def late_return(self, loan):
        if self.loans[loan]['returndate'] < today:
            return "Yes"
        else:
            return "No"


    def display_all_loans(self):
        for loan in self.loans:
            print(f"""
            ---------------
            Customer id: {self.loans[loan]['customer_id']}
            Book name: {self.loans[loan]['book_name']}
            Loan date: {self.loans[loan]['loandate'][::-1]}
            Return date: {self.loans[loan]['returndate'][::-1]}""")
            answer = self.late_return(loan)
            print(f"""            Late return? {answer}
            ---------------""")
            

    def display_late_loans(self):
        print("late loans:")
        for loan in self.loans:
            if self.loans[loan]['returndate'] < today :
                print(f"""
                ---------------
                Customer id: {self.loans[loan]['customer_id']}
                Book name: {self.loans[loan]['book_name']}
                Loan date: {self.loans[loan]['loandate'][::-1]}
                Scheduled return date: {self.loans[loan]['returndate'][::-1]}
                {lt.day_count(self.loans[loan]['returndate'], today)} Days late
                ---------------
                """)
        

    def display_loans_by_customer(self, customer_id):
        print(f"loans for {customer_id}:")
        for loan in self.loans:
            if self.loans[loan]['customer_id'] == customer_id :
                print(f"""
                ---------------
                Customer id: {self.loans[loan]['customer_id']}
                Book name: {self.loans[loan]['book_name']}
                Loan date: {self.loans[loan]['loandate'][::-1]}
                Scheduled return date: {self.loans[loan]['returndate'][::-1]}""")
                answer = self.late_return(loan)
                print(f"                Is the book late for return? {answer}" )
                if answer == 'Yes':
                    print(f"                {lt.day_count(self.loans[loan]['returndate'], today)} Days late")
                print('                ---------------')
        if self.customer_li[customer_id]['customer_loans'] == 0:
            print(f"{customer_id} has no loans")
            return None
    

    def display_loans_by_book(self, book_name):
        print(f"loans for '{book_name}':")
        for loan in self.loans:
            if self.loans[loan]['book_name'] == book_name :
                print(f"""
                ---------------
                Book name: {self.loans[loan]['book_name']}
                Customer id: {self.loans[loan]['customer_id']}
                Loan date: {self.loans[loan]['loandate'][::-1]}
                Scheduled return date: {self.loans[loan]['returndate'][::-1]}""")
                answer = self.late_return(loan)
                print(f"                Late return? {answer}")
                if answer == 'Yes':
                    print(f"                {lt.day_count(self.loans[loan]['returndate'], today)} Days late")
                print('                ---------------')
        if self.book_li[book_name]['num_of_copies'] == self.available_copies[book_name]:
            print(f"'{book_name}' has no loans")
            return None


    def display_book_details(self, book_name):
        late_copies = 0
        summary = []
        for loan in self.loans:
            if self.loans[loan]['book_name'] == book_name:
                if self.loans[loan]['returndate'] < today:
                    late_copies += 1
                    days_late = lt.day_count(self.loans[loan]['returndate'], today)
                    summary.append( f"{late_copies}. copy late in {days_late} days")
        if late_copies == 0 :
            answer = 'No'
        else:
            answer = 'Yes'
        print(f"""
            ---------------
            Book name: {self.book_li[book_name]['name']}
            Author: {self.book_li[book_name]['author']}
            Published on: {self.book_li[book_name]['year_published']}
            Number of copies in the library: {self.book_li[book_name]['num_of_copies']}
            Number of available copies: {self.available_copies[book_name]}
            Maximum loan time: {self.book_li[book_name]['maximum_loan_dayes']} days
            Are there any late copies? {answer}""")
        for s in summary:
            print(f'            {s}')
        print('            ---------------')
            

    def display_customer_details(self, customer_id):
            if self.customer_li[customer_id]['customer_id'] in self.limited_accounts:
                answer = "Yes"
            else:
                answer = "No"
            
            print(f"""Customer details for {customer_id}:
            ---------------
            Customer's id number: {self.customer_li[customer_id]['customer_id']}
            Customer's name: {self.customer_li[customer_id]['name']}
            Customer's address: {self.customer_li[customer_id]['city']}
            Customer's birth date: {self.customer_li[customer_id]['birth_date']}
            Customer's current loans: {self.customer_li[customer_id]['customer_loans']}
            Is the customer's account limited? {answer}""")
            sec_answer = "No"
            for loan in self.loans:
                if self.loans[loan]['customer_id'] == customer_id:
                    sec_answer = self.late_return(loan)
            print(f"""            Are there any late returns? {sec_answer}
             ---------------""")
            
      
    def remove_book(self, book_name):
        if self.book_li[book_name]['num_of_copies'] == self.available_copies[book_name]:
            self.book_li.pop(book_name)
            print("The book has been deleted from the library")
        else:
            on_loan = self.book_li[book_name]['num_of_copies'] - self.available_copies[book_name]
            print(f"There are {on_loan} copies of the book on loan\nWait for it to return to delete the book")
        

    def remove_customer(self, customer_id):
        if self.customer_li[customer_id]['customer_loans'] != 0 :
            print(f"The customer has {self.customer_li[customer_id]['customer_loans']} books that have not been returned yet\nReturn all books before deleting")
        else:
            self.customer_li.pop(customer_id)
            print("The customer has been deleted from the library")


    def save_library_json(self): # not good
        my_library_deta = {'book_li': self.book_li,
        'customer_li': self.customer_li,
        'loans': self.loans,
        'num_of_customers_created': self.num_of_customers_created,
        'available_copies': self.available_copies,
        'limited_accounts': self.limited_accounts,
        'counte': self.counter}
        with open('library_deta.json', 'w') as j:
            json.dump(my_library_deta, j)
        print("Goodbye")


    def open_library_json(self): # not good
        with open('library_deta.json', 'r') as j:
            library_deta = json.load(j)
            self.book_li = library_deta['book_li']
            self.customer_li = library_deta['customer_li']
            self.loans = library_deta['loans']
            self.num_of_customers_created = library_deta['num_of_customers_created']
            self.available_copies = library_deta[ 'available_copies']
            self.limited_accounts = library_deta['limited_accounts']
            self.counter = library_deta['counte']
        print("Good Morning\nhave a wonderful day\n")


    def save_library(self):
        my_library_deta = {'book_li': self.book_li,
                'customer_li': self.customer_li,
                'loans': self.loans,
                'num_of_customers_created': self.num_of_customers_created,
                'available_copies': self.available_copies,
                'limited_accounts': self.limited_accounts,
                'counte': self.counter}
        with open('test.pickle', 'wb') as pp:
                pickle.dump(my_library_deta, pp)
        print("Goodbye")


    def open_library(self):
        with open('test.pickle', 'rb') as pp:
                library_deta = pickle.load(pp)
                self.book_li = library_deta['book_li']
                self.customer_li = library_deta['customer_li']
                self.loans = library_deta['loans']
                self.num_of_customers_created = library_deta['num_of_customers_created']
                self.available_copies = library_deta[ 'available_copies']
                self.limited_accounts = library_deta['limited_accounts']
                self.counter = library_deta['counte']
        print("Good Morning\nhave a wonderful day\n")



if __name__ == '__main__':
    l = Library()
    print("test 1 - check: add_new_customer " )
    print("Expected result is: 3 customers on the list with 3 different id numbers " )
    print("Actual result is:")
    l.add_new_customer('Ofer', 'TLV', '23-1-82')
    l.add_new_customer('Nir', 'TLV', '23-6-12')
    l.add_new_customer('Amit', 'Kahal', '10-6-86')
    print(l.customer_li)
    l.add_new_customer('Michal', 'Jerusalem', '10-9-52')
    l.add_new_customer('Ariel', 'Haifa', '17-4-80')
    l.add_new_customer('Yael', 'Kiryat Shmona', '24-1-76')
    print('-------------')
    print("test 2 - check: add_new_book + double book + Without num of copies" )
    print("Expected result is: The Master and Margarita - 11 copies, Algebra part 2 - 1 copy " )
    print("Actual result is:")
    l.add_new_book('Gone with the Wind', 'Margaret Mitchell', 1936, 1, 10)
    l.add_new_book("Harry Potter and the Philosopher's Stone", ' J. K. Rowling', 1997, 2, 8)
    l.add_new_book("Harry Potter and the Deathly Hallows", ' J. K. Rowling', 2007, 2, 12)
    l.add_new_book("Harry Potter and the Chamber of Secrets", ' J. K. Rowling', 2002, 2, 15)
    l.add_new_book("The Catcher in the Rye", 'J. D. Salinger', 1951, 1, 6)
    l.add_new_book("The Master and Margarita", ' Mikhail Bulgakov', 1967, 1, 6)
    l.add_new_book("The Cat in the Hat", 'Dr. Seuss', 1957, 3, 16)
    l.add_new_book("Fox in Socks", 'Dr. Seuss', 1965, 3, 10)
    l.add_new_book("The Gruffalo", ' Julia Donaldson', 1999, 3, 3)
    l.add_new_book("The Gruffalo's Child", '  Dr. Seuss', 2004, 3, 3)
    l.add_new_book("Algebra part 2", 'Bnei Goren', 1976, 1)
    l.add_new_book("The Master and Margarita", ' Mikhail Bulgakov', 1967, 1, 5)
    print(l.book_li)
    print('-------------')
    print("test 3 - check: loan_a_book" )
    print("Expected result is: customer 00002 loaned 1 book, 'The Cat in the Hat' 1 less available copie " )
    print("Actual result before:")
    print(l.available_copies)
    print("Actual result after:")
    l.loan_a_book('00002', 'The Cat in the Hat')
    print(l.loans)
    print(l.available_copies)
    print('-------------')
    print("test 4 - check: loan_a_book - returndate on Saturday (loandate 21.3.22)" )
    print("Expected result is: returndate for 00004 is on 27,3,22" )
    print("Actual result is:")
    l.loan_a_book('00004', "Harry Potter and the Philosopher's Stone")
    print(l.loans)
    print('-------------')
    print("test 5 - check: loan_a_book - mor then 3 books" )
    print("Expected result is: Error printing" )
    print("Actual result is:")
    l.loan_a_book('00004', "The Catcher in the Rye")
    l.loan_a_book('00004', "Algebra part 2")
    l.loan_a_book('00004', "The Gruffalo's Child")
    print('-------------')
    print("test 6 - check: loan_a_book - no available copies" )
    print("Expected result is: Error printing and estimated return date" )
    print("Actual result is:")
    l.loan_a_book('00001', "Algebra part 2")
    print('-------------')
    print("test 7 - check: loan_a_book - Customer with late return" )
    print("Expected result is: Error printing" )
    print("Actual result is:")
    today = (2022, 3, 15)
    l.loan_a_book('00001', "The Gruffalo's Child")
    now = datetime.now()
    today = (now.year,now.month,now.day)
    l.loan_a_book('00001', "Harry Potter and the Deathly Hallows")
    print('-------------')
    print("test 8 - check: loan_a_book - no available copies for book with several copies" )
    print("Expected result is: Error printing and estimated return date on 22.3.22" )
    print("Actual result is:")
    today = (2022, 3, 21)
    l.loan_a_book('00005', "The Gruffalo's Child")
    now = datetime.now()
    today = (now.year,now.month,now.day)
    l.loan_a_book('00003', "The Gruffalo's Child")
    l.loan_a_book('00006', "The Gruffalo's Child")
    print('-------------')
    print("test 9 - check: return_a_book" )
    print("Expected result is: customer 00005 not on loans list, and num of available copies for The Gruffalo's Child is 1 " )
    print("Actual result is:")
    l.return_a_book('00005', "The Gruffalo's Child")
    print(l.loans)
    print('-------------')
    print(l.available_copies)
    print('-------------')
    print("test 10 - check: return_a_book - late return" )
    print("Expected result is: Error printing, the customer 00001 add to limited accounts list" )
    print("Actual result is:")
    l.return_a_book('00001', "The Gruffalo's Child")
    print("limited accounts list:")
    print(l.limited_accounts)
    print('-------------')
    print("test 11 - check: loan_a_book - to limited account" )
    print("Expected result is: Error printing and limit release date" )
    print("Actual result is:")
    l.loan_a_book('00001', "Harry Potter and the Philosopher's Stone")
    print('-------------')
    print("test 12 - check: limited_accounts_check" )
    print("Expected result is: before - 00006 add to limited_accounts list" )
    print("Actual result is:")
    today = (2022, 3,15)
    l.loan_a_book('00006', "Fox in Socks")
    today = (2022, 3, 20)
    l.return_a_book('00006', "Fox in Socks")
    print(l.limited_accounts)
    print('-------------')
    print("Expected result is: after - 00006 removed from limited_accounts list" )
    today = (2022, 4,3)
    l.limited_accounts_check()
    print(l.limited_accounts)
    now = datetime.now()
    today = (now.year,now.month,now.day)
    print('-------------')
    print("test 13 - check: display_all_books" )
    print("Expected result is: Nice print of  self.book_li, arranged alphabetically" )
    print("Actual result is:")
    l.display_all_books()
    print('-------------')
    print("test 14 - check: Display_all_customers" )
    print("Expected result is: Nice print of  self.customer_li, Sorted by id num" )
    print("Actual result is:")
    l.Display_all_customers()
    print('-------------')
    print("test 15 - check: display_all_loans" )
    print("Expected result is: Nice print of  self.loans" )
    print("Actual result is:")
    today = (2021, 8, 4)
    l.loan_a_book('00003', "Gone with the Wind")
    today = (2022, 3,15)
    l.loan_a_book('00006', "Fox in Socks")
    now = datetime.now()
    today = (now.year,now.month,now.day)
    l.display_all_loans()
    print('-------------')
    print("test 16 - check: display_late_loans" )
    print("Expected result is: Nice print of late loans" )
    print("Actual result is:")
    l.display_late_loans()
    print('-------------')
    print("test 17 - check: display_loans_by_customer" )
    print("Expected result is: Nice print of loans_by_customer" )
    print("Actual result is:")
    print('-------------')
    l.display_loans_by_customer('00001')
    print('-------------')
    l.display_loans_by_customer('00002')
    print('-------------')
    l.display_loans_by_customer('00003')
    print('-------------')
    l.display_loans_by_customer('00004')
    print('-------------')
    l.display_loans_by_customer('00005')
    print('-------------')
    l.display_loans_by_customer('00006')
    print('-------------')
    print("test 18 - check: display_loans_by_book" )
    print("Expected result is: Nice print of loans_by_book" )
    print("Actual result is:")
    l.loan_a_book('00003', "Fox in Socks")
    l.loan_a_book('00005', "Fox in Socks")
    l.display_loans_by_book('Gone with the Wind')
    print('-------------')
    l.display_loans_by_book("Harry Potter and the Philosopher's Stone")
    print('-------------')
    l.display_loans_by_book("Harry Potter and the Deathly Hallows")
    print('-------------')
    l.display_loans_by_book("Harry Potter and the Chamber of Secrets")
    print('-------------')
    l.display_loans_by_book("The Catcher in the Rye")
    print('-------------')
    l.display_loans_by_book("The Master and Margarita")
    print('-------------')
    l.display_loans_by_book("The Cat in the Hat")
    print('-------------')
    l.display_loans_by_book("Fox in Socks")
    print('-------------')
    l.display_loans_by_book("The Gruffalo")
    print('-------------')
    l.display_loans_by_book("The Gruffalo's Child")
    print('-------------')
    l.display_loans_by_book("Algebra part 2")
    print('-------------')
    l.display_loans_by_book("The Master and Margarita")
    print('-------------')
    print("test 19 - check: find_book_by_name" )
    print("Expected result is: Nice print of book details" )
    print("Actual result is:")
    today = (2022,1,16)
    l.loan_a_book('00005', "Gone with the Wind")
    today = (2022,2,23)
    l.loan_a_book('00004', "Gone with the Wind")
    now = datetime.now()
    today = (now.year,now.month,now.day)
    print('-------------')
    l.display_book_details('Gone with the Wind')
    print('-------------')
    l.display_book_details("Harry Potter and the Philosopher's Stone")
    print('-------------')
    l.display_book_details("Harry Potter and the Deathly Hallows")
    print('-------------')
    l.display_book_details("Harry Potter and the Chamber of Secrets")
    print('-------------')
    l.display_book_details("The Catcher in the Rye")
    print('-------------')
    l.display_book_details("The Master and Margarita")
    print('-------------')
    l.display_book_details("The Cat in the Hat")
    print('-------------')
    l.display_book_details("Fox in Socks")
    print('-------------')
    l.display_book_details("The Gruffalo")
    print('-------------')
    l.display_book_details("The Gruffalo's Child")
    print('-------------')
    l.display_book_details("Algebra part 2")
    print('-------------')
    l.display_book_details("The Master and Margarita")
    print('-------------')
    print("test 20 - check: display_customer_details" )
    print("Expected result is: Nice print of customer details" )
    print("Actual result is:")
    l.display_customer_details('00001')
    l.display_customer_details('00002')
    l.display_customer_details('00003')
    l.display_customer_details('00004')
    l.display_customer_details('00005')
    l.display_customer_details('00006')
    print('-------------')
    print("test 21 - check: remove_book - Not all copies in the library" )
    print("Expected result is: Error printing" )
    print("Actual result is:")
    l.remove_book("The Gruffalo's Child")
    print('-------------')
    print("test 22 - check: remove_book - All copies in the library" )
    print("Expected result is: Confirmation printing and 'The Gruffalo' not on the book list" )
    print("Actual result is:")
    l.remove_book("The Gruffalo")
    l.display_all_books()
    print('-------------')
    print("test 23 - check: remove_customer - Not all loans return to the library" )
    print("Expected result is: Error printing" )
    print("Actual result is:")
    l.remove_customer("00005")
    print('-------------')
    print("test 24 - check: remove_customer - All cloans return to the library" )
    print("Expected result is: Confirmation printing and '00001' not on the customers list" )
    print("Actual result is:")
    l.remove_customer("00001")
    l.Display_all_customers()
    print('-------------')
    print("test 25 - check: save_library" )
    l.save_library()
    print('-------------')
    print("test 25 - check: open_library" )
    l.open_library()
    print('-------------')
    print(l.limited_accounts)
    print('-------------')
    l.loan_a_book('00006', 'Gone with the Wind')
    print(l.limited_accounts)
    print('-------------')
    print("done")
    print('-------------')