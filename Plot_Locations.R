#Import libraries needed
library(leaflet)

#Read in Locations csv as a data frame
locations = read.csv("WoolworthsLocations.csv")

#Creating function so we can colour the locations based on what type it is
colorFact = colorFactor(c("red", "green", "blue", "black", "yellow"), domain = c("Countdown", "Countdown Metro", "Distribution Centre", "FreshChoice", "SuperValue"), ordered = TRUE)

#Create an instance of the leaflet object locations, the markers are coloured based on what type of location they are. 
#Included a legend to the plot
#Included adaptive clustering to this plot
leaflet(data = locations) %>% addTiles() %>% addCircleMarkers(stroke = FALSE, radius = 8, color = ~colorFact(Type), fillOpacity = 0.8, clusterOptions = markerClusterOptions()) %>% 
  addLegend("bottomright", pal = colorFact, values = ~Type, title = "Types of Locations")

#Same as above, but no adaptive clustering
#leaflet(data = locations) %>% addTiles() %>% addCircleMarkers(stroke = FALSE, radius = 8, color = ~colorFact(Type), fillOpacity = 0.8) %>% 
  #addLegend("bottomright", pal = colorFact, values = ~Type, title = "Types of Locations")

