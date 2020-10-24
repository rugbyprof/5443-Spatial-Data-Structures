## Assignment 3 - Flask Spatial API
#### Due: 10-02-2020 (Friday @ 5:30 p.m.)


For this assignment, you will use flask to query a spatial data structure for N points closest to a mouse click, and display those points on a map. This is just to get you started for our bigger project. You can use an R-Tree or a KD-Tree it doesn't matter. I have a few links below of where you can find the resources to implement your spatial data structure. It doesn't matter which one you pick to start, because you will eventually will implement them both and will run comparisons on differing queries between the those structures and more. 

### Resources for R-Tree and KD-Tree

Both R-Tree's and KD-Tree's store spatial data by continuously dividing the space into smaller and smaller sections. The basic difference is that KD-Trees divide each sub-space into quadrants, and R-Tree keeps creating smaller and smaller bounding boxes. Both of these have subtle differences when performing queries on our points. Here is a pretty good overview of both trees along with nearest neighbor and range queries.

- Article about `range queries` and `nearest neighbor queries`  
  - https://blog.mapbox.com/a-dive-into-spatial-search-algorithms-ebd0c5e39d2a


And here are a couple of implementations for both types of trees. Please post other implementations of either tree on slack if you find them. We want to stay within the `scipy` / `pandas` world since that will be the vast majority of documentation that we find and they both use `dataframes` to store data.

- Kdtree:
  - With code for tree:
    - https://scipy-cookbook.readthedocs.io/items/KDTree_example.html
  - Using scipy:
    - http://library.isr.ist.utl.pt/docs/scipy/spatial.html

- Rtree
  - Using libspatialindex lib:
    - https://libspatialindex.org/en/latest/
    - https://toblerity.org/rtree/index.html#home
  - With geopandas:
    - https://geoffboeing.com/2016/10/r-tree-spatial-index-python/


### Requirements

- Your app should display a basic map. 
- With a single click of the mouse, a request should be made to your flask api and performa a Nearest Neighbor query using either of the spatial trees from above.
- The radius doesn't matter, but whatever data you use, and depending on where you click, try to ensure non-empty results.
- For example, earthquake data points tends to be on coast lines. This kind of information is good to put in your readme for when I test your app ... or when you show how it works to the class.
- After each click, for now, do not worry about removing previous results, but that should be something you should think about for future versions.

### Deliverables

- Create a folder called `A03` in your assignments folder.
- Add your flask app code.
- Add your front end html.
- Add any data files OR at least a link to them in your readme if they are too large to upload to github (> 50MB).
- Create a readme in accordance with [this](../../Resources/R01/README.md).
- Be prepared to discuss and show the class your app.