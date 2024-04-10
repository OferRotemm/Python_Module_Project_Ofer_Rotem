import library

def library_menu():
    my_library = library.Library()
    my_library.open_library()
    while True:
        print("Choose an action:")
        action = input("""
        To add a new customer - pressure 1
        To add a new book - pressure 2
        To Loan a book - pressure 3
        To return a book - pressure 4
        To display all books - pressure 5
        To display all customers - pressure 6
        To display all loans - pressure 7
        To display late loans - pressure 8
        To display loans by customer - pressure 9
        To display loans by book - pressure 10
        To display book details - pressure 11
        To display customer details - pressure 12
        To remove book - pressure 13
        To remove customer - pressure 14
        To exit - pressure 15

        """)

        if action == '1' :
            name = input("Enter the customer name: ")
            city = input("Enter the customer address: ")
            birth_date = input("Enter customers birth date: ")
            my_library.add_new_customer(name, city, birth_date)

        if action == '2' :
            name = input("Enter the book name: ")
            author = input("Enter the book's author name: ")
            year_published = input("Enter the book year of publishe: ")
            type = int(input("Enter the book type - 1, 2 or 3: "))
            num_of_copies = int(input("Enter  number of copies: "))
            my_library.add_new_book(name, author, year_published, type, num_of_copies)

        if action == '3' :
            customer_id = input("Enter the customer id: ")
            book_name = input("Enter the book name: ")
            my_library.loan_a_book(customer_id, book_name)

        if action == '4' :
            customer_id = input("Enter the customer id: ")
            book_name = input("Enter the book name: ")
            my_library.return_a_book(customer_id, book_name)
            
        if action == '5' :
            my_library.display_all_books()
            
        if action == '6' :
            my_library.Display_all_customers()
            
        if action == '7' :
            my_library.display_all_loans()
            
        if action == '8' :
            my_library.display_late_loans()
            
        if action == '9' :
            customer_id = input("Enter the customer id: ")
            my_library.display_loans_by_customer(customer_id)
            
        if action == '10' :
            book_name = input("Enter the book name: ")
            my_library.display_loans_by_book(book_name)
            
        if action == '11' :
            book_name = input("Enter the book name: ")
            my_library.display_book_details(book_name)
            
        if action == '12' :
            customer_id = input("Enter the customer id: ")
            my_library.display_customer_details(customer_id)
            
        if action == '13' :
            book_name = input("Enter the book name: ")
            my_library.remove_book(book_name)
            
        if action == '14' :
            customer_id = input("Enter the customer id: ")
            my_library.remove_customer(customer_id)
            
        if action == '15' :
            my_library.save_library()
            break



library_menu()
            