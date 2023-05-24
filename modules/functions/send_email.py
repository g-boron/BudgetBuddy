import smtplib
import modules.email_credentials

MY_EMAIL = modules.email_credentials.email
MY_PASSWORD = modules.email_credentials.password
MESSAGE_ENG = f"Hi, xxx.\nWe are so happy that since today you will manage your budget better. Your " \
                   f"account was created successfully and you're ready to rock!\nSincerely,\nBudgetBuddy team"
MESSAGE_PL = f"Cześć, xxx.\nCieszymy się, że od dziś będziesz lepiej zarządzasz swoim budżetem. Twoje " \
                  f"konto użytkownika zostało utworzone prawidłowo i jesteś gotów do działania!\nZ " \
                  f"poważaniem,\nZespół BudgetBuddy"


def send_confirmation_mail_eng(provided_email, provided_login):
    user_email = provided_email
    username = provided_login
    final_message = MESSAGE_ENG.replace("xxx", username)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
        connection.starttls()
        connection.login(password=MY_PASSWORD, user=MY_EMAIL)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_email,
                            msg=f"Subject:Your account was created successfully!\n\n{final_message}")


def send_confirmation_mail_pl(provided_email, provided_login):
    user_email = provided_email
    username = provided_login
    my_email = modules.email_credentials.email
    my_password = modules.email_credentials.password
    final_message = MESSAGE_PL.replace("xxx", username)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
        connection.starttls()
        connection.login(password=my_password, user=my_email)
        connection.sendmail(from_addr=my_email, to_addrs=user_email,
                            msg=f"Subject:Twoje konto zostało poprawnie utworzone!\n\n{final_message}")


def send_notification_email(provided_login, provided_email):
    user_email = provided_email
    username = provided_login
    notification_message = f"Hi, {username}.\nWe need to inform you that you have unread new notifications. " \
                           "Open the app to check what's up!\n\nSincerely,\nBudgetBuddy team"

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
        connection.starttls()
        connection.login(password=MY_PASSWORD, user=MY_EMAIL)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_email,
                            msg=f"Subject:New notifications are waiting for you!\n\n{notification_message}")
