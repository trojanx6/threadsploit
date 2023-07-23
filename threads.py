import re
import requests as req
import json
from colorama import Fore,Style
import subprocess
import importlib.util

required_modules = {
    'requests',
    'colorama'
}

# Eksik modülleri kontrol etme ve yükleme işlemi
for module in required_modules:
    spec = importlib.util.find_spec(module)
    if spec is None:
        subprocess.check_call(['pip', 'install', module])
    else:
        pass

class colors:
    Red = Fore.RED + Style.BRIGHT #kirmizi
    Gren = Fore.GREEN + Style.BRIGHT #yesil
    blue= Fore.BLUE + Style.BRIGHT # mavi
    yellow= Fore.YELLOW + Style.BRIGHT
    magenta = Fore.MAGENTA + Style.BRIGHT # mor
    cyan = Fore.CYAN + Style.BRIGHT # acik mavi
    white = Fore.WHITE + Style.BRIGHT # beyaz
class App():
    def __init__(self) -> None:
        self.banner()
        self.username =input("UserName:").strip()
        self.instagram_url = "https://www.instagram.com/"
        self.threads_url = "https://www.threads.net/api/graphql"
        self.response = req.get('https://www.threads.net/@instagram')
        self.token_key_position = self.response.text.find('\"token\"')
        self.token = self.response.text[self.token_key_position + 9:self.token_key_position + 31]
        self.get_user_id()
        self.user_info_data()
        self.parse()
        self.thread()
        self.write()

    def get_user_id(self):
        """
        The id information of the user whose information is requested is obtained.
        :return: int
        """

        get_request = req.get(self.instagram_url + self.username)
        serachs = re.search('"user_id":"(\d+)",',get_request.text).group()
        id = re.search('\d+',serachs).group()
        return id





    def user_info_data(self):

        resp = req.post(
            url=self.threads_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-IG-App-ID': '238260118697367',
                'X-FB-LSD': self.token,
                'Sec-Fetch-Site': 'same-origin',
            },
            data={
                'lsd': self.token,
                'variables': json.dumps({
                    'userID': self.get_user_id(),
                }),
                'doc_id': '23996318473300828',
            },
        )
        return resp.json()

    def parse(self):
        """
        username info parse
        :return: list
        """
        data = self.user_info_data()
        try:
            path = data["data"]["userData"]["user"]
            username = path["username"]
            pic_p = path["hd_profile_pic_versions"][-1]["url"]
            biography = path["biography"]
            full_name = path["full_name"]
            follower_count = path["follower_count"]
            bio_link = path["bio_links"][0]["url"]
            return [username,pic_p,biography,full_name,follower_count,bio_link]
        except TypeError:
            print("data not found")
        except KeyError as error:
            print(error,"not found")


    def thread(self):
        """
        retrieves the post links of the entered user
        :return: list
        """
        request_ = req.post(url=self.threads_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-IG-App-ID': '238260118697367',
                'X-FB-LSD': self.token,
                'Sec-Fetch-Site': 'same-origin',
            },
            data={
                'lsd': self.token,
                'variables': json.dumps({
                    'userID': self.get_user_id(),
                }),
                'doc_id': '6858205827546926',
            },
            )
        path = request_.text
        path = json.loads(path)
        code_listesi = []
        threads = path["data"]["mediaData"]["threads"]
        for thread in threads:
            for item in thread["thread_items"]:
                code = item["post"]["code"]
                code_listesi.append(f"https://threads.net/@{self.username}/post/"+code)


        return code_listesi

    def write(self):
        user_profil_info = self.parse()
        user_profil_post = self.thread()
        print(f"""
[ + ] {colors.Gren}Username:{user_profil_info[0]}
[ + ] {colors.Gren}Full Name:{user_profil_info[3]}
[ + ] {colors.Gren}Followers:{user_profil_info[-2]}
[ + ] {colors.Gren}Profil Photo:{user_profil_info[1]}
[ + ] {colors.Gren}Bio Link:{user_profil_info[-1]}
[ + ] {colors.Gren}Bio:{user_profil_info[2]}
[ + ] {colors.Gren}Thread:{user_profil_post}
        """)

    def banner(self):
        print(f"""{colors.magenta}
███████████ █████                                       █████                   ████            ███   █████   
░█░░░███░░░█░░███                                       ░░███                   ░░███           ░░░   ░░███    
░   ░███  ░  ░███████   ████████   ██████   ██████    ███████   █████  ████████  ░███   ██████  ████  ███████  
    ░███     ░███░░███ ░░███░░███ ███░░███ ░░░░░███  ███░░███  ███░░  ░░███░░███ ░███  ███░░███░░███ ░░░███░   
    ░███     ░███ ░███  ░███ ░░░ ░███████   ███████ ░███ ░███ ░░█████  ░███ ░███ ░███ ░███ ░███ ░███   ░███    
    ░███     ░███ ░███  ░███     ░███░░░   ███░░███ ░███ ░███  ░░░░███ ░███ ░███ ░███ ░███ ░███ ░███   ░███ ███
    █████    ████ █████ █████    ░░██████ ░░████████░░████████ ██████  ░███████  █████░░██████  █████  ░░█████ 
   ░░░░░    ░░░░ ░░░░░ ░░░░░      ░░░░░░   ░░░░░░░░  ░░░░░░░░ ░░░░░░   ░███░░░  ░░░░░  ░░░░░░  ░░░░░    ░░░░░  
                                                                       ░███                                    
                                                                       █████                                   
                                                                      ░░░░░                                    """)
App()


