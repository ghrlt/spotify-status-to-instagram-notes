> THIS REPO HAS BEEN ARCHIVED ON June 13 of 2025.
> 1) because i was not using it anymore for too long,
> 2) because Instagram themself implemented that feature in their app!

>  Thanks to past users, issuers & contributors!

> <img src="https://github.com/user-attachments/assets/0c0e25ed-65c5-477e-8205-fabd7e1a5e19" height="400">


# Spotify status to Instagram notes

You like to share your Spotify activity on Discord? You ever wanted to do it on Instagram too? Well, this program is made for you.


## Installation
First, you'll need a [Spotify dev app](https://developer.spotify.com/documentation/web-api/concepts/apps), create one [here](https://developer.spotify.com/dashboard/create).
<br>**Add `http://localhost:1811/callback` as a registered Redirect URI** 

Then, clone this project into your machine:<br>
`git clone https://github.com/ghrlt/spotify-status-to-instagram-notes.git`

Go in the directory<br>
`cd spotify-status-to-instagram-notes`

Install the required packages<br>
`python3.10 -m pip install -r requirements.txt`
<br><br>

Create a file named `.env.local` and write in the following (Delete comments):
```js
// You can find this on your Spotify app page
SPOTIFY_CLIENT_ID=""
SPOTIFY_CLIENT_SECRET=""

// Put in your Instagram account credentials
INSTAGRAM_USERNAME=""
INSTAGRAM_PASSWORD=""
INSTAGRA_2FA_SEED="" // Fill only if you have 2fa enabled, and wish to auto-gen the 2fa code
```
If you switch account between prod/dev environnement, you can also use `.env.production`, `.env.production.local`, `.env.development`, `.env.development.local` files

<br>

If you wish to show notes to your close friends only, add the following line in your `.env.local` file:
```
INSTAGRAM_DEFAULT_AUDIENCE="1"
```

<br>

## Configuration
You can now start the app!<br>
`python3.10 app.py`

You'll be asked to open a webpage, it is to authenticate to Spotify. If everything go well, the last thing you should see is:
```json
{"success": true}
```
You can then close the page and return on your terminal, where you should see a confirmation message. It is then going to login to Instagram, using the credentials provided in your environnement file(s).

- If your account is protected by 2FA, but you did **not** filled the `INSTAGRAM_2FA_SEED`, you'll be asked for a 2FA code.
- If any error occurs, the program will display the error and crash.

## Working flow
The program will make a request to Spotify API to get your current playing song, format the name and artist, and post it on your Instagram notes.
To avoid spamming, and your notes and Spotify API, the programm will then wait until the estimated end of the song. It will then repeat the process.

If you are playing the same song over and over, the program will not post a new note. It will only post a new note if the song differ from the previously played one.

## Troubleshooting
- I can't login to Instagram, it says "challenge required"
    - I can't do anything about it, it's Instagram's fault. You'll have to solve the challenge manually from your Instagram app.




If you encounter any issue, please open an issue on this repository, and I'll try to help you as soon as possible.

## Contributing
If you want to contribute to this project, feel free to open a pull request, I'll be happy to review it!
