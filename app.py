import time

import env
import instagram
import spotify


class App:
    def __init__(self):
        self.instagram = instagram.Client()
        self.spotify = spotify.Client()

        self.running = True
        self.lastTrackId = None

    def start(self):
        self.spotify.login()
        self.instagram._login()

        while self.running:
            currentPlayback = self.spotify.getCurrentPlayback()
            if not currentPlayback:
                print(currentPlayback)
                self.wait(10)
                continue

            if currentPlayback['is_playing'] is False:
                self.wait(60)
                continue

            if currentPlayback['item']['type'] != 'track':
                raise Exception(f"Unsupported item type: {currentPlayback['item']['type']}")
            
            track = currentPlayback['item']
            timeLeft = track['duration_ms'] - currentPlayback['progress_ms']
            
            if track['id'] == self.lastTrackId:
                self.wait(timeLeft / 1000)
                continue

            self.lastTrackId = track['id']

            print(f"Playing {track['name']} by {track['artists'][0]['name']}, next in {timeLeft/1000}s")            
            self.instagram.setStatus(
                f"🎶 {track['name']} by {track['artists'][0]['name']}"
            )

            self.wait(timeLeft / 1000)

    def wait(self, seconds):
        print(f"Waiting {seconds} seconds...")
        time.sleep(seconds)


if __name__ == '__main__':
    App().start()