import os
import instagrapi

import env


class Client(instagrapi.Client):
    def __init__(self):
        super().__init__()


    def _login(self):
        self.username = env.INSTAGRAM_USERNAME
        self.mfa_code = ''

        self.session_settings_path = f"{env.WORKING_DIRECTORY_PATH}/ig-{self.username}.session"

        #~ Load session settings, if exists
        if os.path.exists(self.session_settings_path):
            self.load_settings(self.session_settings_path)

        #~ Login
        if env.INSTAGRAM_2FA_SEED:
            self.mfa_code = self.totp_generate_code(env.INSTAGRAM_2FA_SEED)
        
        try:
            self.login(env.INSTAGRAM_USERNAME, env.INSTAGRAM_PASSWORD, verification_code=self.mfa_code)
        except instagrapi.exceptions.TwoFactorRequired:
            print("Instagram | 2FA is enabled. But you did not provide a 2FA seed. Please provide a 2FA seed in the .env file.")
            self.mfa_code = input("Instagram | Please enter the 2FA code: ")
            self.login(env.INSTAGRAM_USERNAME, env.INSTAGRAM_PASSWORD, verification_code=self.mfa_code)

        self.dump_settings(self.session_settings_path)

        print("Instagram | Successfully logged in as", self.username)

    def setStatus(self, status: str):
        if len(status) > 60:
            # raise Exception("Status is too long. Max 60 characters.")
            status = status[:57] + "..."

        self.send_note(status, 0)
