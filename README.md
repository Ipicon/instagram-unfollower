# Instagram Unfollower

Instafram Unfollower A simple script which unfollows on Instagram all who dosen't follow you back. (Can add excluded users)

## Setup

Make sure you have Python installed and pip configured.

**Run:**
> pip install -r requirements.txt

## Run

> python unfollower.py

## Excluded users
To exluded users from being unfollowed, add one user per line in **excludes.txt**, the script will simply ignore them in the unfollowing procedure.

## Edits

### There are two occurrences you may want to edit:

- Every element which is found by xpath may change in the future, if that happend you should do either:
    - Contact me 
    - Change the code for yourself
    - Fork the update
- There is a 30 seconds time delay between each user being unfollowed, **ON PORPUSE**, so Instagram won't recognize you as a bot.
    - If you wish you can toy around with it, but if you get banned it's not my fault ¯\\\_(ツ)_/¯
