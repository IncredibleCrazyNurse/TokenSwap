import matplotlib.pyplot as plt
import numpy as np

class TokenSwap:
    def __init__(self, reserve_x, reserve_y, fee=0.003, lp_share=0.5):
        self.reserve_x = reserve_x # トークンXの流通量
        self.reserve_y = reserve_y # トークンYの流通量
        self.k = reserve_x * reserve_y # 定積数
        self.fee = fee # スワップ手数料率
        self.lp_share = lp_share # 手数料のLPシェア (50%なら0.5)
        self.lp_earnings = 0 # LPへの累積支払い額

    def swap(self, input_amount, input_token):
        if input_token == "X":
            output_amount = self.get_output_amount(input_amount, self.reserve_x, self.reserve_y)
            self.reserve_x += input_amount
            self.reserve_y -= output_amount
        elif input_token == "Y":
            output_amount = self.get_output_amount(input_amount, self.reserve_y, self.reserve_x)
            self.reserve_y += input_amount
            self.reserve_x -= output_amount
        else:
            raise ValueError("Invalid input token. Must be 'x' or 'y'.")
        return output_amount

    def get_output_amount(self, input_amount, input_reserve, output_reserve):
        input_amount_with_fee = input_amount * (1 - self.fee)
        fee_collected = input_amount * self.fee
        self.distribute_fee(fee_collected)
        new_input_reserve = input_reserve + input_amount_with_fee
        new_output_reserve = self.k / new_input_reserve
        return output_reserve - new_output_reserve

    def distribute_fee(self, fee_collected):
        lp_payment = fee_collected * self.lp_share
        self.lp_earnings += lp_payment
        reserve_payment = fee_collected * (1 - self.lp_share)
        if self.reserve_x < self.reserve_y:
            self.reserve_x += reserve_payment / 2
            self.reserve_y += reserve_payment / 2

    def get_price(self):
        return self.reserve_y / self.reserve_x

    def display_pool_status(self):
        print(f"\nCurrent Pool Status:")
        print(f"Reserve X: {self.reserve_x}")
        print(f"Reserve Y: {self.reserve_y}")
        print(f"LP Earnings: {self.lp_earnings:.2f}")
        print(f"Price of Y (in X): {self.get_price():.5f}")
        self.plot_pool_state()

    def plot_pool_state(self):
        """現在のプール状態をプロット"""
        x = np.linspace(self.reserve_x * 0.5, self.reserve_x * 2, 1000) # 範囲を調整する
        y = self.k / x

        plt.figure(figsize=(4, 4))
        plt.plot(x, y, label="x * y = k (Pool Curve)")
        plt.scatter([self.reserve_x], [self.reserve_y], color="red", label="Current State")
        plt.xlabel("Reserve X")
        plt.ylabel("Reserve Y")
        plt.title("Token Swap Pool State")
        plt.legend()
        plt.grid(True)
        plt.show()

# Initial settings
initial_x = 10000
initial_y = 10000

# Create an instance of the TokenSwap class
swap = TokenSwap(initial_x, initial_y)

# User interface
print("=== Token Swap Simulator ===")
print("Initial pool status:")
swap.display_pool_status()

try:
    while True:
        print("\n[Options]")
        print("1. Swap Token X -> Token Y")
        print("2: Swap Token Y -> Token X")
        print("3. View pool status")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            input_amount = float(input("Enter the amount of Token X to swap: "))
            output_amount = swap.swap(input_amount, "X")
            print(f"You swapped {input_amount:.2f} Token X for {output_amount:.2f} Token Y.")
        elif choice == "2":
            input_amount = float(input("Enter the amount of Token Y to swap: "))
            output_amount = swap.swap(input_amount, "Y")
            print(f"You swapped {input_amount:.2f} Token Y for {output_amount:.2f} Token X.")
        elif choice == "3":
            swap.display_pool_status()
        elif choice == "4":
            swap.display_pool_status()
            print("Exiting session.")
            break
        else:
            print("Invalid choice. Please select again.")

except ValueError:
    print("Session interrupted.")


