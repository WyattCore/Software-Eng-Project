# Software-Eng-Project

  1. Download project as .zip file, extract the files to desired destination, navigate to the extracted folder and copy the /path/to/Software-Eng-Project/
  - Open terminal and change the directory to run the code:
  ```
  cd /path/to/Software-Eng-Project/
  ```

  2. Run the file 'traffic_generator.py' in a separate bash terminal first
  ```
  python3 src/traffic_generator.py
  ```
  - Input equipment IDs that you would like, this generates UDP traffic & simulates game units.

  3. Install required libraries:
  ```    
  sudo apt-get install python3-tk
  sudo apt install python3-pip
  python3 -m pip install typing
  python3 -m pip install Pillow
  pip install psycopg2-binary
  pip install pygubu
  ```
  - Run the program:
  ```
  python3 src/main.py
  ```
*NOTE: If it throws an unique constraint error while inserting players, run the following in SQL(view step 5):
  ```
  ALTER TABLE players ADD CONSTRAINT unique_user_id UNIQUE (id);
  ALTER TABLE players ADD CONSTRAINT unique_codename UNIQUE (codename);
  ```

  4. For player input, use the TAB key to register entry spaces.
  - When you are finished registering the first team's players use the mouse to click on the first entry space for the other team's equipment ID and proceed with the same process.
  - Enter your equipment IDs the same as ones you entered in the traffic generator.
  - To clear all entries press the F12 key. 
  - When all players are entered via TAB key, click the continue button with mouse OR press F5 key. 
  - When ready to start the game, use the mouse to click the 'Start Game' button.

  5. To view the database, input in terminal:
  ```
  psql photon
  select * from players;
  ```
 _______________________________________
| GitHub Username  | Real Name          |
|------------------|--------------------|
| axyliang         | Axyl Liang         |
| KrispyKremeMan   | Wyatt Core         |
| LisbethEch       | Lisbeth Echeverria |
| touzongvang      | Touzong Vang       |
| yonatanruark     | Yonatan Rubio Lugo |
 _______________________________________
