## Assignment 4 - Visualizing Spatial Data
#### Due: 10-14-2020 (Wednesday @ 4:30 p.m.)


### Overview

- Using the Github repo here: https://github.com/portofportlandgis/portmap which contains much (if not all) of the necessary functionality to do many of the things required by this project. 
- Add a backend api (like flask) and any additional features requested from below.  
- The data sources the author used are references to json files stored on another server, you will replace those get requests with data from your flask api if needed.
- The code in the repo is organized like many typical web apps with `assets` folder holding much of the code. 
- In particular, you will need to pay attention to the following files and folders: 

| File                | Description                                                                                |
| :------------------ | :----------------------------------------------------------------------------------------- |
| assets/js/map.js    | This is where your javascript will go. It gets loaded into `index.html` with a script tag. |
| assets/json/        | This is a json folder for local data files.                                                |
| assets/flask_api.py | This is your python flask app.                                                             |
| index.html          | If you need to add html or change styles (which you shouldn't probably need to) put here.  |

- See a directory structure example below:

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/portmap_important_files.png" width="200">

## Requirements

This repo has almost everything I wanted us to do for this project. But I'm not going to act like I didn't find it because if fulfills so many of our needs for a future project. So, this will take some effort on your part, but it is grad school soooooo get ready to study. I'm going to create some vids on adding functionality, and will see how many issues I run into. If they start amassing,  I will reconsider this approach. Also, I'm giving a lot of leeway in your approach, but at the end of the day, I expect you to put effort into this project which means removing many of the existing functions if you are not using them directly. Like, the print button for example. Definitely keep a version of the code with all of its capabilities, but don't leave erroneous code in the project because you're too lazy to clean the code base. Or ensure all code is in easily identifiable locations and commented so its easy to find and read. 

#### Points:

- The repo already has the ability to place points onto the map. 
  - Add the ability to save those points to a json file and reload them later.
  - Add a text box that allows you to put a lat/lon in the box, and a submission will find nearest neighbors from any one of our many data sets (earthquakes, ufos, volcanoes, plane crashes). Or click the map to get results. I would create a menu item, with a modal that would have input elements to let the user choose a data set to search, and how big to make the query (radius or number of neighbors for example).

#### Lines: 

- The repo has line drawing capability already. Instead of saving the lines to a json file, add the ability to choose a starting and ending point both from separate dropdown menus (like cities). When the second point is chosen, a line will get drawn and a distance calculated between the two chosen points will be displayed in some clear manner.

#### Minimum Area Bounding Box

- Draw a rectangle on the map somewhere. This will query the backend and find all points (again from whatever data file) within the bounding rectangle and display them in some manner. 

#### Minimum Area Polygon

- Draw a polygon around a cluster of points (again, it could be fake data, or any one of the many data files we have) and the polygon will "snap tight" like a rubber band around the points inside the polygon. You do not have to use the "draw" component in mapbox. You could simply use a menu item that displays a modal that lets a user "click" the map within a set of points, and a tightly bound polygon could appear around the points.

#### GeoJson

- Upload or paste a GeoJson file into a textarea and display it on the map.

#### View Railroads

- Add a flask route to return all railroads within a given US State and then display the railroads withing the state. Any railroads that spill into neighboring states is ok.

#### Layers

- You need to keep track of everything you add to your map, so you can remove it if necessary. Create a modal that will display all the added layers (checkbox with a list of layernames) and allow them to be removed with a delete button. Havng ability to chang layer colors would be nice.



