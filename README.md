

# issAboveSkopje

The issAboveSkopje (Internation Space Station above Skopje) is a micro-project which checks if the ISS
is above Skopje and if so, tweets about it - and turns ON LED lights. You can find the account on Twitter (@ISSAboveSkopje).

## Getting Started

Firstly, not to get confused, I'm using a file NOT uploaded on this repo called "conf.py"
where I have stored my Twitter authentication tokens, and then I'm importing the file (conf.py) from
the issMk.py script.

You're going to need this lines added in the issMk.py or any other file and then import it in order to get
the authentication. Replace the "VALUE" with the right key from your Twitter APP.

```
CONSUMER_KEY = "VALUE"
CONSUMER_SECRET = "VALUE"
ACCESS_KEY = "VALUE"
ACCESS_SECRET =  "VALUE"
```

### Installation and configuring

The script uses Python 3 and Tweepy which is Python library for accessing the Twitter API. You can get to it with:

```
pip3 install tweepy
```

In order to set it up for your city, find the line (in the issMk.py file)
```
fetched = urllib.request.urlopen('http://spotthestation.nasa.gov/sightings/xml_files/Macedonia_None_Skopje.xml')
```
and replace it with your link (You can find it here: http://spotthestation.nasa.gov/sightings/). I'm also using a local XML file downloaded from the site for testing purposes.

### How it works

Basically, the script checks the RSS feed and compares the time (when the ISS is above) with your system time. If it is, it posts status on twitter and sends DM's to all the followers. The file ids.txt stores the ID's of all the followers and if someone wants to disable getting DM's from the account, tweets '@ISSAboveSkopje disableDM' and the script removes that ID from the list while the file
disabledUsers.txt collects full data of those who disabled the DM's (time, ID, username).

### Lighting up LED's
I'm using Arduino to get the lights ON. There is a script uploaded on this repo which you can copy and change for your own needs. How it works, basically, when the ISS is above, the script writes data to the Arduino port (1 or 0).

### Running the script

You don't really need anything else to set it up except if you want to connect Arduino but it's not necessary. You can do it with
```
sudo python3 issMk.py
```
The script will run without stopping (or until you stop it) so it's good idea to make it a background service (I'm using Raspberry Pi 2 for hosting it)


