import os
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import psycopg2


class handler(BaseHTTPRequestHandler):
    
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    project_id = os.environ.get("PROJECT_ID")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    private_key_id = os.environ.get("PRIVATE_KEY_ID")
    private_key = os.environ.get("PRIVATE_KEY").replace("\\n", "\n")
    client_email = os.environ.get("CLIENT_EMAIL")
    client_x509_cert_url = os.environ.get("CLIENT_X509_CERT_URL")
    
    def connect_postgres(self):
        try:
            conn = psycopg2.connect(
                host=self.postgres_host,
                database=self.postgres_dbname,
                user=self.postgres_user,
                password=self.postgres_password,
            )
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def select_postgres(self):
        conn = self.connect_postgres()
        try:
            save_new_videos_sql = f"""
                    SELECT video_id, "name"
                    FROM public.music_videos;
                """
            cur = conn.cursor()
            cur.execute(save_new_videos_sql)
            result_select = cur.fetchall()
            cur.close()
            return result_select
        finally:
            if conn is not None:
                conn.close()
                print("Database connection closed.")

    def do_GET(self):
        result = self.select_postgres()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str(result).encode())
        return
