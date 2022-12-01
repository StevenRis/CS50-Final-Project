# Race_Place - cars' setups for Dirt Rally 2.0

# Live: <https://extremely-elated-possum-gadget.wayscript.cloud/home>
# Description:
&nbsp;
My project is called **Race_Place** and is dedicated to racing game **Dirt Rally 2.0**.
This project was created as the [final project](https://cs50.harvard.edu/x/2022/project/) for the course [CS50's Introduction to Computer Science](https://www.edx.org/course/cs50s-introduction-to-computer-science).

&nbsp;
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

## Using **Race_Place**
### Logging includes
Race_Place provides basic functionalities for users to  **register**, **log in**, **change password**, **log out**.

### Home Page
&nbsp;
![Image of homepage](/screenshots/home-page.png)
Once registered and logged in, users will be redirected to home page, where they can click on the **choose your vehicle** button to view all existing vehicles.

&nbsp;

## Vehicles page
&nbsp;
![Image of vehicle page](/screenshots/listofcars.png)

When users select the interested vehicle they will be redirected to the locations page with the list of available locations for the selected vehicle. 

![Image of location page](/screenshots/listoflocations.png)

Available location means a car setup for that location. Every location can have more than one setup.

When users select interested location, for example Spain, they are redirected to the setup page for that location. There users can view existing setups for that location, in our case its Spain.

![Image of setup page](/screenshots/carsetup.png)

&nbsp;

If users are signed in they can add the setup they like to favorites clicking on the like button. If they are not signed in the modal window will appear.

![Image of setup page](/screenshots/clickAddFav.png)

&nbsp;
### Account page
After signning in or registering users can check what setups they have in favorites opening the **My Account** page.
![Image of setup page](/screenshots/accountpage.png)

On the **My account** page users can select a setup to view it or to delete.

&nbsp;
## The Database
**Race_Place** utilizes **SQL**. 
Database was created using the schema below:
```
CREATE TABLE cars 
(
    id INTEGER, brand TEXT NOT NULL,
    model TEXT NOT NULL,
    class TEXT NOT NULL, 
    car_image TEXT NOT NULL,
    PRIMARY KEY (id)
)


CREATE TABLE locations 
(
    id INTEGER, 
    location_name TEXT NOT NULL,
    location_image TEXT NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
)

CREATE TABLE favorite_setups
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    setup_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(setup_id) REFERENCES "setupsOld"(id)
)

CREATE TABLE setups 
(
    id INTEGER NOT NULL PRIMARY KEY,
    cars_id INTEGER NOT NULL,
    locations_id INTEGER NOT NULL,
    surface TEXT,
    tyres TEXT,
    conditions TEXT,
    toeAngleFront TEXT,
    camberAngleFront TEXT,
    toeAngleRear TEXT,
    camberAngleRear TEXT,
    brakingForce TEXT,
    brakeBias TEXT,
    frontLSDDrivingLock TEXT,
    frontLSDBrakingLock TEXT,
    frontLSDPreload' TEXT,
    centreLSDDrivingLock' TEXT,
    centreLSDBrakingLock' TEXT,
    centreLSDPreload' TEXT,
    frontVisDif TEXT,
    centerVisDif TEXT,
    rearVisDif TEXT,
    rearLsdDrivLock TEXT,
    rearLsdBrakeLock TEXT,
    rearLSDPreload TEXT,
    gear1 TEXT,
    gear2 TEXT,
    gear3 TEXT,
    gear4 TEXT,
    gear5 TEXT,
    gear6 TEXT,
    finalDrive TEXT,
    note TEXT,
    optimalShift TEXT,
    slowBumpFront TEXT,
    fastBumpFront TEXT,
    bumpZoneDivFront TEXT,
    slowReboundFront TEXT,
    slowBumpRear TEXT,
    fastBumpRear TEXT,
    bumpZoneDivRear TEXT,
    slowReboundRear TEXT,
    rideHeightFront TEXT,
    springRateFront TEXT,
    rollBarFront TEXT,
    rideHeightRear TEXT,
    springRateRear TEXT,
    rollBarRear TEXT,
    FOREIGN KEY(cars_id) REFERENCES cars(id),
    FOREIGN KEY(locations_id) REFERENCES locations(id)
)
```