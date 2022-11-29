# Race_Place
#### Video Demo:  <URL HERE>
#### Description:
My project is called **Race_Place** and is dedicated to racing game **Dirt Rally 2.0**.
The main aim of this web app is to gather the cars' setups in one place allowing user quickly search for a particular car setup for the rally stage. It's a fullstack application based on the Python and SQL database on the back-end, Bootstrap, Sass and HTML on the front-end.

 The feature of the project is that a user can make an account, search for a setup he's interested in, and add this setup to favorites.

## The project consists of the several pages:
* **Home page**
* **Vehicles**
* **Locations**
* **Setups**
* **Register**
* **Sign in**
* **My account**

At the begining of the development I started with the **layout.html**, for css styles I chose the **bootstrap** framework for its simplicity, and **python** on the backend. 

When I finished the basic layout of the *front-end* I started to build the *back-end*.
For saving information of vehicles, locations, users and setups I created a **SQL** database called "database.db". This database includes tables such as:
* cars
* locations
* setups
* users
* favorite setups

These tables mentioned above are connected with each other by foreign keys, so it allowed me to fetch the information the user wants to get, for example to display the setup for a particular location and car. The setup page has table design for better readability.

If the user likes the setup, he may add it to favorites clicking the on "heart" button on the setup page. if the user is **not** registred, the modal window will appear, where he may register or sign in. If the user **is** registered the setup will be added to favorites. To see what the user has in favorites he needs to open **My account**, where are cards of favorite setups, he added previously.