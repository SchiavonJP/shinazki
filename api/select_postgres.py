import os
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import psycopg2


class handler(BaseHTTPRequestHandler):

    postgres_host = os.environ.get("POSTGRES_HOST")
    postgres_dbname = os.environ.get("POSTGRES_DBNAME")
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")

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
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(str(result).encode())
        return
