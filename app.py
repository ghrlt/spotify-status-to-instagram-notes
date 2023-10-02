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
        self.lastSetNoteId = None

        self.playbackFailCount = 0

    def deleteInstagramNote(
        self,
        onlyIfCreatedByThisScript=False
    ):
        note = self.instagram.getOurNote()

        if onlyIfCreatedByThisScript:
            print("Instagram | Deleting note, if created by this script")
            if note.id == self.lastSetNoteId:
                self.instagram.deleteNote(note.id)
                print("Instagram | Deleted note")
            else:
                print("Instagram | Note was not created by this script, skipping")
        else:
            print("Instagram | Deleting note")
            self.instagram.deleteNote(note.id)
            print("Instagram | Deleted note")


    def start(self):
        self.spotify.login()
        self.instagram._login()

        while self.running:
            currentPlayback = self.spotify.getCurrentPlayback()
            if not currentPlayback:
                print("Spotify | Not playing / Not available")
                self.wait(10)
                self.playbackFailCount += 1

                if self.playbackFailCount >= 3:
                    print("Spotify | Failed to get playback 3 times, deleting note")
                    self.deleteInstagramNote(onlyIfCreatedByThisScript=True)
                    self.playbackFailCount = 0

                continue

            if currentPlayback['is_playing'] is False:
                print("Spotify | Not playing")
                self.deleteInstagramNote(onlyIfCreatedByThisScript=True)

                self.wait(60)
                continue

            if currentPlayback['item']['type'] != 'track':
                raise Exception(f"Unsupported item type: {currentPlayback['item']['type']}")
            
            track = currentPlayback['item']
            timeLeft = track['duration_ms'] - currentPlayback['progress_ms']
            if timeLeft <= 0:
                # Sometimes, the progress_ms is higher than/equal to the duration_ms..
                # So let's just avoid spamming Spotify API
                timeLeft = 2000

            if track['id'] == self.lastTrackId:
                self.wait(timeLeft / 1000)
                continue

            self.lastTrackId = track['id']

            print(f"Currently playing {track['name']} by {track['artists'][0]['name']}, next song in {timeLeft/1000}s")            
            self.instagram.setStatus(
                f"🎶 {track['name']} by {track['artists'][0]['name']}",
                audience=env.INSTAGRAM_DEFAULT_AUDIENCE
            )

            self.lastSetNoteId = self.instagram.getOurNote().id

            self.wait(timeLeft / 1000)

    def wait(self, seconds):
        print(f"Waiting {seconds} seconds...")
        time.sleep(seconds)


if __name__ == '__main__':
    App().start()