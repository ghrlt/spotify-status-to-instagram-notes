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
        self.lastNoteId = None

        self.playbackFailCount = 0

    def deleteInstagramNote(
        self,
        onlyIfCreatedByThisScript=False
    ):
        currentNotes = self.instagram.get_my_notes()['items']
        if currentNotes:
            currentNote = currentNotes[0]
            if currentNote['id'] == self.lastNoteId or self.lastNoteId == None or onlyIfCreatedByThisScript:
                self.instagram.delete_note(currentNote['id'])
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
                timeLeft = 20

            if track['id'] == self.lastTrackId:
                self.wait(timeLeft / 1000)
                continue

            self.lastTrackId = track['id']

            print(f"Currently playing {track['name']} by {track['artists'][0]['name']}, next song in {timeLeft/1000}s")            
            self.instagram.setStatus(
                f"🎶 {track['name']} by {track['artists'][0]['name']}"
            )

            self.lastNoteId = self.instagram.get_my_notes()['items'][0]['id']

            self.wait(timeLeft / 1000)

    def wait(self, seconds):
        print(f"Waiting {seconds} seconds...")
        time.sleep(seconds)


if __name__ == '__main__':
    App().start()