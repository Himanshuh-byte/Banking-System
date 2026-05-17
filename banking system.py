import random
from datetime import datetime


# ─────────────────────────────────────────────
#  Account Class
# ─────────────────────────────────────────────
class Account:
    def __init__(self, name, acc_no, ifsc, balance=0.0):
        self.name = name
        self.acc_no = acc_no
        self.ifsc = ifsc
        self._balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        self._balance += amount
        return self._balance

    def debit(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def credit(self, amount):
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return
        if not self.debit(amount):
            print("Insufficient balance.")
            return
        return self._balance

    def display(self):
        print("=" * 40)
        print(f"  Account No : {self.acc_no}")
        print(f"  Name       : {self.name}")
        print(f"  IFSC       : {self.ifsc}")
        print(f"  Balance    : ₹{self._balance:,.2f}")
        print("=" * 40)


# ─────────────────────────────────────────────
#  Bank Class
# ─────────────────────────────────────────────
class Bank:
    def __init__(self):
        self.accounts = {}
        self.used_acc_numbers = set()
        self.transactions = []

    def generate_acc_no(self):
        while True:
            acc_no = random.randint(100000, 999999)
            if acc_no not in self.used_acc_numbers:
                self.used_acc_numbers.add(acc_no)
                return acc_no

    def create_account(self, name, ifsc):
        acc_no = self.generate_acc_no()
        acc = Account(name, acc_no, ifsc)
        self.accounts[acc_no] = acc
        print(f"\n✅ Account created successfully!")
        print(f"   Account No: {acc_no}")
        print(f"   Name      : {name}")
        print(f"   IFSC      : {ifsc}")

    def get_account(self, acc_no):
        return self.accounts.get(acc_no)

    def deposit(self, acc_no, amount):
        acc = self.get_account(acc_no)
        if acc:
            result = acc.deposit(amount)
            if result is not None:
                print(f"✅ Deposited ₹{amount:,.2f}  |  New Balance: ₹{result:,.2f}")
        else:
            print("❌ Account not found.")

    def withdraw(self, acc_no, amount):
        acc = self.get_account(acc_no)
        if acc:
            result = acc.withdraw(amount)
            if result is not None:
                print(f"✅ Withdrawn ₹{amount:,.2f}  |  New Balance: ₹{result:,.2f}")
        else:
            print("❌ Account not found.")

    def transfer(self, sender_acc_no, receiver_acc_no, receiver_name, receiver_ifsc, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            amount = float(amount)
        except ValueError:
            print("❌ Invalid amount format.")
            return

        sender = self.get_account(sender_acc_no)
        receiver = self.get_account(receiver_acc_no)

        if not sender or not receiver:
            print("❌ Account not found.")
            self.transactions.append((sender_acc_no, receiver_acc_no, amount, "FAILED", timestamp))
            return

        if receiver.name.lower() != receiver_name.lower() or receiver.ifsc.lower() != receiver_ifsc.lower():
            print("❌ Receiver verification failed.")
            self.transactions.append((sender_acc_no, receiver_acc_no, amount, "FAILED", timestamp))
            return

        if amount <= 0:
            print("❌ Invalid amount.")
            return

        if not sender.debit(amount):
            print("❌ Insufficient balance.")
            self.transactions.append((sender_acc_no, receiver_acc_no, amount, "FAILED", timestamp))
            return

        receiver.credit(amount)
        print(f"\n✅ Transfer Successful!")
        print(f"   Transferred ₹{amount:,.2f} to {receiver.name}")
        print(f"   Your New Balance: ₹{sender._balance:,.2f}")
        self.transactions.append((sender_acc_no, receiver_acc_no, amount, "SUCCESS", timestamp))

    def show_transactions(self):
        if not self.transactions:
            print("\n📋 No transactions found.")
            return
        print("\n📋 Last 5 Transactions:")
        print("-" * 75)
        print(f"{'Time':<22} {'From':>8} → {'To':<8} {'Amount':>12}  {'Status'}")
        print("-" * 75)
        for t in self.transactions[-5:]:
            sender, receiver, amount, status, time = t
            status_icon = "✅" if status == "SUCCESS" else "❌"
            print(f"{time:<22} {sender:>8} → {receiver:<8} ₹{amount:>10,.2f}  {status_icon} {status}")
        print("-" * 75)


# ─────────────────────────────────────────────
#  Main Program
# ─────────────────────────────────────────────
def main():
    bank = Bank()

    print("\n" + "=" * 50)
    print("        🏦  WELCOME TO PYTHON BANK  🏦")
    print("=" * 50)

    while True:
        print("\n┌─────────────────────────────────┐")
        print("│         MAIN MENU               │")
        print("├─────────────────────────────────┤")
        print("│  1. Create Account              │")
        print("│  2. Deposit                     │")
        print("│  3. Withdraw                    │")
        print("│  4. Display Account             │")
        print("│  5. Transfer Funds              │")
        print("│  6. View Transactions           │")
        print("│  7. Exit                        │")
        print("└─────────────────────────────────┘")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            name = input("Enter name: ").strip()
            ifsc = input("Enter IFSC code: ").strip()
            if not ifsc:
                print("❌ IFSC cannot be empty.")
                continue
            bank.create_account(name, ifsc)

        elif choice == '2':
            try:
                acc_no = int(input("Enter account number: "))
                amt = float(input("Enter amount: "))
            except ValueError:
                print("❌ Invalid input.")
                continue
            bank.deposit(acc_no, amt)

        elif choice == '3':
            try:
                acc_no = int(input("Enter account number: "))
                amt = float(input("Enter amount: "))
            except ValueError:
                print("❌ Invalid input.")
                continue
            bank.withdraw(acc_no, amt)

        elif choice == '4':
            try:
                acc_no = int(input("Enter account number: "))
            except ValueError:
                print("❌ Invalid input.")
                continue
            acc = bank.get_account(acc_no)
            if acc:
                acc.display()
            else:
                print("❌ Account not found.")

        elif choice == '5':
            try:
                sender_acc = int(input("Enter your account number: "))
                receiver_acc = int(input("Enter receiver account number: "))
                receiver_name = input("Enter receiver name: ").strip()
                receiver_ifsc = input("Enter receiver IFSC: ").strip()
                amt = float(input("Enter amount: "))
            except ValueError:
                print("❌ Invalid input.")
                continue
            bank.transfer(sender_acc, receiver_acc, receiver_name, receiver_ifsc, amt)

        elif choice == '6':
            bank.show_transactions()

        elif choice == '7':
            print("\n👋 Thank you for using Python Bank. Goodbye!\n")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()