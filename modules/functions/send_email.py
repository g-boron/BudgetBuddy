import smtplib
import modules.email_credentials

class SendEmail:
    def __init__(self):
        pass
       

    def send_confirmation_mail_eng(self,provided_email,provided_login,message):
        user_email = provided_email
        username = provided_login
        text=message
        MY_EMAIL = modules.email_credentials.email
        MY_PASSWORD = modules.email_credentials.password
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(password=MY_PASSWORD, user=MY_EMAIL)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_email,
                                msg=f"Subject:New notifications are waiting for you!\n\n{text}")

    def send_confirmation_mail_pl(self):
        user_email = "" # uzupełnić o wpisany przy rejestracji mail
        username = "" # uzupełnić o wpisane przy rejestracji imię
        final_message = self.MESSAGE_PL.replace("xxx", username)
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(password=self.MY_PASSWORD, user=self.MY_EMAIL)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=user_email,
                                msg=f"Subject:Twoje konto zostało poprawnie utworzone!\n\n{final_message}")