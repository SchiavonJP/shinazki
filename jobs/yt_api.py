# from Google import Create_Service
import json
import os
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from pydantic import BaseModel
import psycopg2

# Separar em um arquivo de configuração
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=["./settings.toml", ".secrets.toml"])
pyproject = Dynaconf(settings_files=["./pyproject.toml"])
settings.client_id = os.environ["CLIENT_ID"]
settings.client_secret = os.environ["CLIENT_SECRET"]
settings.project_id = os.environ["PROJECT_ID"]
settings.postgres_password = os.environ["POSTGRES_PASSWORD"]


class Music(BaseModel):
    name: str
    videoId: str


class Youtube:
    def __init__(self, api_name, api_version):
        self.api_name = api_name
        self.api_version = api_version

    def get_authenticated_service(self):
        # Sim isso é uma gambiarra, mas é o que eu consegui fazer
        c = {
            "web": {
                "client_id": settings.client_id,
                "project_id": settings.project_id,
                "auth_uri": settings.auth_uri,
                "token_uri": settings.token_uri,
                "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url,
                "client_secret": settings.client_secret,
                "redirect_uris": [settings.redirect_uris],
                "javascript_origins": [settings.javascript_origins],
            }
        }
        with open("aux.json", "w") as fp:
            json.dump(c, fp)
        flow = flow_from_clientsecrets(
            "aux.json",
            scope=[settings.scope],
            message="Error loading client secret file: %s",
        )

        storage = Storage("%s-oauth2.json" % self.api_name)
        credentials = storage.get()

        if credentials is None or credentials.invalid:

            credentials = run_flow(flow, storage)

        return build(self.api_name, self.api_version, credentials=credentials)

    def get_channel_detatils(self, channel_id):
        self.service = self.get_authenticated_service()
        request = self.service.channels().list(part="contentDetails", id=channel_id)
        channel_request = (
            self.service.channels()
            .list(part="snippet,contentDetails,statistics", id=channel_id)
            .execute()
        )
        list_videos = []
        for channel in channel_request["items"]:
            # From the API response, extract the playlist ID that identifies the list
            # of videos uploaded to the authenticated user's channel.
            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            print("Videos in list %s" % uploads_list_id)

            # Retrieve the list of videos uploaded to the authenticated user's channel.
            playlistitems_list_request = self.service.playlistItems().list(
                playlistId=uploads_list_id, part="snippet", maxResults=50
            )

            while playlistitems_list_request:
                playlistitems_list_response = playlistitems_list_request.execute()

                # Print information about each video.
                for playlist_item in playlistitems_list_response["items"]:
                    list_videos.append(
                        Music(
                            name=playlist_item["snippet"]["title"],
                            videoId=playlist_item["snippet"]["resourceId"]["videoId"],
                        )
                    )
                    """ title = playlist_item["snippet"]["title"]
                    video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                    
                    print("%s (%s)" % (title, video_id))
 """
                playlistitems_list_request = self.service.playlistItems().list_next(
                    playlistitems_list_request, playlistitems_list_response
                )
                # print(list_videos)
                """ with open("musics.txt", "w") as f:
                    f.write("\n".join([video for video in list_videos])) """
                self.save_postgres(list_videos)
        return None

    def connect_postgres(self, list_videos):
        try:
            conn = psycopg2.connect(
                host=settings.postgres_host,
                database=settings.postgres_dbname,
                user=settings.postrgres_user,
                password=settings.postgres_password,
            )
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def save_postgres(self, list_videos):
        conn = self.connect_postgres(list_videos)
        try:
            for video in list_videos:
                save_new_videos_sql = f"""
                        INSERT INTO music_videos 
                        VALUES ('{video.videoId}', '{video.name.replace("'", "")}') 
                        ON CONFLICT DO NOTHING
                    """
                cur = conn.cursor()
                cur.execute(save_new_videos_sql)
                conn.commit()
            cur.close()
        finally:
            if conn is not None:
                conn.close()
                print("Database connection closed.")


if __name__ == "__main__":
    youtube = Youtube(
        api_name="youtube",
        api_version="v3",
    )
    channel_id = settings.channel_id
    response = youtube.get_channel_detatils(channel_id)
