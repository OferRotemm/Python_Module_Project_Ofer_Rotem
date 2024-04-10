

class Books :
    def __init__(self, name, author, year_published, type, num_of_copies=1) :
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type # 1 – up to 10 days, 2 – up to 5 days, 3 – up to 2 days
        self.num_of_copies = num_of_copies
        self.maximum_loan = self.max_calc()
    
    def max_calc(self):
        if self.type == 1:
            return 10
        elif self.type == 2:
            return 5
        elif self.type == 3:
            return 2