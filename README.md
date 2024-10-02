# Software-Eng-Project

  1. Download project as .zip file, extract the files to desired destination, navigate to the extracted folder and copy the /path/to/Software-Eng-Project/,
then open terminal and change the directory to run the code:
     ```
     cd /path/to/Software-Eng-Project/
     ```

  2. Run the file 'traffic_generator.py' in a separate bash terminal first
  ```
  python3 src/traffic_generator.py
  ```
and input equipment IDs that you would like, this generates UDP traffic & simulates game units.

  3. Install required libraries and run the program.
  ```    
  sudo apt-get install python3-tk
  python3 -m pip install typing
  python3 -m pip install Pillow
  pip install psycopg2-binary
  pip install pygubu
  python3 src/main.py
  ```

  4. Player input will use the tab key to register entry spaces, when the first team's players are finished use your mouse to click the entry space for the other team's first equipment ID and proceed with the same process. When all players are entered, click the continue button with mouse or press f5 key. Enter your equipment IDs the same as ones you entered in the traffic generator.

  5. To view the database, input in terminal
  ```
   psql photon
  ```
then
  ```
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
