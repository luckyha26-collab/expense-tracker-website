class Expense:
    def __init__(self, amount, category, date, description=None):
        self.amount = amount  # float
        self.category = category  # str
        self.date = date  # str in YYYY-MM-DD format
        self.description = description  # str, optional

    def validate(self):
        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            raise ValueError("Amount must be a positive number.")
        if not isinstance(self.category, str) or not self.category:
            raise ValueError("Category must be a non-empty string.")
        if not isinstance(self.date, str) or not re.match(r'\d{4}-\d{2}-\d{2}', self.date):
            raise ValueError("Date must be in YYYY-MM-DD format.")
        # Add more validation rules as needed

    def __repr__(self):
        return f"<Expense(amount={self.amount}, category='{self.category}', date='{self.date}', description='{self.description}')>",
