# music-networks
CS 194-31 Final Project

|branch_name   | description  |
|---|---|
| final | final_submission code  |
| dev  | preliminary results 10/12  |
| master  | initial trials November work  |


## How the website works
When you enter an artist and song, a call is made to the [heroku database](https://surumen-mixtape.herokuapp.com/getTracks?).
For example, for Rihanna's song, Diamonds, the query would look like this on the database
https://surumen-mixtape.herokuapp.com/getTracks?artist=rihanna&song=diamonds 
