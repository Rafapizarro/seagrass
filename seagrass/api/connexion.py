import os

from supabase import Client, create_client


class DBConnexion:
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("Missing Supabase credentials: Check SUPABASE_URL and SUPABASE_KEY")

    def get_connexion(self):
        supabase: Client = create_client(self.url, self.key)
        return supabase
