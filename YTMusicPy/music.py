import requests
import json


class Music:
    def __init__(self, ip="127.0.0.1", port=9863, auth_password=None):
        self.ip = ip
        self.port = port
        self.auth_password = auth_password
        self.request_url = f"http://{ip}:{port}/query"

    def get_track_info(self):
        return requests.get(self.request_url + "/track").json()

    def get_player_info(self):
        return requests.get(self.request_url + "/player").json()

    def get_lyrics_info(self):
        return requests.get(self.request_url + "/lyrics").json()

    def get_playlists_info(self):
        return requests.get(self.request_url + "/playlist").json()

    def get_queue_info(self, raw=False):
        if raw:
            return requests.get(self.request_url + "/queue").json()
        else:
            data = requests.get(self.request_url + "/queue").json()
            index = data['currentIndex']
            auto_mix = data['automix']
            songs = data['list']
            x = 0
            new_songs = []
            for song in songs:
                song['index'] = x
                x += 1
                new_songs.append(song)
            return {"automix": auto_mix, "currentIndex": index, 'list': songs}

    def send_command(self, command, value=None):
        headers = {"Authorization": "bearer " + str(self.auth_password)}
        data = json.dumps({"command": command, 'value': value}).encode('utf-8')
        return requests.post(self.request_url, headers=headers, data=data)

    def play_pause(self):
        self.send_command('track-play-pause')
        return True

    def play(self):
        if self.get_player_info()['isPaused']:
            self.send_command("track-play")
        else:
            return False
        return True

    def pause(self):
        if not self.get_player_info()['isPaused']:
            self.send_command("track-pause")
        else:
            return False
        return True

    def next(self):
        self.send_command('track-next')
        return True

    def previous(self):
        self.send_command('track-previous')
        return True

    def like(self):
        self.send_command('track-thumbs-up')
        return True

    def dislike(self):
        self.send_command('track-thumbs-down')
        return True

    def volume_up(self):
        self.send_command('player-volume-up')
        return True

    def volume_down(self):
        self.send_command('player-volume-down')
        return True

    def forward_ten(self):
        self.send_command('player-forward')
        return True

    def back_ten(self):
        self.send_command('player-rewind')
        return True

    def repeat(self, value=None):
        self.send_command('player-repeat', value=value)
        return True

    def shuffle(self):
        self.send_command("player-shuffle")
        return True

    def library_add(self):
        self.send_command("player-add-library")
        return True

    def set_volume(self, volume: int):
        # Warning: glitchy
        self.send_command('player-set-volume', value=volume)
        return True

    def set_time(self, time=int):
        self.send_command('player-set-seekbar', value=time)
        return True

    def select_queue(self, index: int):
        self.send_command('player-set-queue', value=index)

    def add_to_playlist(self, index:int):
        self.send_command('player-add-playlist', value=index)
