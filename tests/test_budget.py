from modules.budget import Budget


class TestBudget:
    def setup_method(self):
        self.budget = Budget(9)
        self.old_balance = self.budget.balance

    def test_add_correct_expense(self):
        result = self.budget.add_expense('Test expense', 'Description', 1500, 1, '2023-01-01')
        new_balance = self.old_balance - 1500
        assert result == True
        assert new_balance == self.budget.balance

    def test_add_incorrect_expense(self):
        result = self.budget.add_expense('Test expense', 'Description', 1000000, 1, '2023-01-01')
        new_balance = self.old_balance - 1000000
        assert result == False
        assert new_balance != self.budget.balance

    def test_add_revenue(self):
        result = self.budget.add_revenue('Test revenue', 'Description', 2000, '2023-01-01')
        new_balance = self.old_balance + 2000
        assert new_balance == self.budget.balance