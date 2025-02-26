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
  - When entering IDs, please not that the traffic generator will ask for Red Team first. On the player_entry screen, ensure that the teams align with the corresponding table. For example, the Red Teams IDs should align with the table on the right.

  3. Install required libraries:
  ```    
  sudo apt-get install python3-tk
  sudo apt install python3-pip
  sudo apt-get install python3-pygame
  python3 -m pip install typing
  python3 -m pip install Pillow
  pip install psycopg2-binary
  pip install pygubu
  pip install pygame
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
  - Example Team input below: 
  - For team 1 enter as follows:
  - Equipment ID:          User ID:       Name:
  -     1                    1            Wyatt
  -     2                    2            Jonah
  - Team 2:
  - Equipment ID:          User ID:       Name:
  -     3                    3            Isaac
  -     4                    4            Noah
  - When you are finished registering the first team's players use the mouse to click on the first entry space for the other team's equipment ID and proceed with the same process.
  - Enter your equipment IDs the same as ones you entered in the traffic generator.
  - To clear all entries press the F12 key. 
  - When all players are entered via TAB key, click the continue button with mouse OR press F5 key. 
  - When ready to start the game, use the mouse to click the 'Start Game' button OR press F5 again.

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
