# Software-Eng-Project
  1. Create a Supabase account on [https://supabase.com/], create a new project and make a table named users, with id and username columns. Find the Project URL and API key and copy and paste into the dotenv file, then rename the file to '.env'.


  2. For traffic generator, run the file 'traffic_generator.py' in a separate bash terminal first
  ```bash
  python3 src/traffic_generator.py
  ```
and input equipment IDs that you would like, this generates UDP traffic & simulates game units.


  3. Install required libraries and run the program.
  ```bash     
  python3 -m pip install python-dotenv
  python3 -m pip install supabase
  python3 -m pip install tkinter
  python3 -m pip install typing
  python3 -m pip install Pillow
  python3 src/main.py
  ```

  4. Player input will use the tab key to register entry spaces, when the first team's players are finished use your mouse to click the entry space for the other team's first equipment ID and proceed with the same process. When all players are entered, click the continue button with mouse or press f5 key. Enter your equipment IDs the same as ones you entered in the traffic generator.
