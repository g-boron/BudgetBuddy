import smtplib


class Email:
    def __init__(self):
        self.MY_EMAIL = "verify.budgetbuddy@gmail.com"
        self.MY_PASSWORD = "nwwbokinryjauuql"
        self.MESSAGE_ENG = f"Hi, xxx. We are so happy that since today you will manage your budget better. Your" \
                           f"account was created successfully and you're ready to rock!\nSincerely,\nBudgetBuddy team"
        self.MESSAGE_PL = f"Cześć, xxx. Cieszymy się, że od dziś będziesz lepiej zarządzasz swoim budżetem. Twoje" \
                           f"konto użytkownika zostało utworzone prawidłowo i jesteś gotów do działania!\nZ " \
                          f"poważaniem,\nZespół BudgetBuddy"

    def send_confirmation_mail_eng(self):
        user_email = "" # uzupełnić o wpisany przy rejestracji mail
        username = "" # uzupełnić o wpisane przy rejestracji imię
        final_message = self.MESSAGE_ENG.replace("xxx", username)
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(password=self.MY_PASSWORD, user=self.MY_EMAIL)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=user_email,
                                msg=f"Subject:Your account was created successfully!\n\n{final_message}")

    def send_confirmation_mail_pl(self):
        user_email = "" # uzupełnić o wpisany przy rejestracji mail
        username = "" # uzupełnić o wpisane przy rejestracji imię
        final_message = self.MESSAGE_PL.replace("xxx", username)
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(password=self.MY_PASSWORD, user=self.MY_EMAIL)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=user_email,
                                msg=f"Subject:Twoje konto zostało poprawnie utworzone!\n\n{final_message}")
