from datetime import datetime

now = datetime.now()
today = '%02d,%02d,%04d' % ( now.year, now.month,now.day )


class Loans :
    def __init__(self, customer_id, book_name, loandate = today) :
        self.customer_id = customer_id
        self.book_name = book_name
        self.loandate = loandate
        self.returndate = 0