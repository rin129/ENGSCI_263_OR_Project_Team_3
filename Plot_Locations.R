#Import libraries needed
library(leaflet)

#Read in Locations csv as a data frame
locations = read.csv("WoolworthsLocations.csv")
#Mutating type of supermarket to work for the icons. 
locations$Type[locations$Type == "Countdown Metro"] <- "Countdown_Metro"
locations$Type[locations$Type == "Distribution Centre"] <- "Distribution_Centre"

IconsList <- iconList(Countdown = makeIcon("https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png", iconWidth = 24, iconHeight =32),
                       Countdown_Metro = makeIcon("https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png", iconWidth = 24, iconHeight =32),
                       Distribution_Centre = makeIcon("https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png", iconWidth = 24, iconHeight =32),
                       FreshChoice = makeIcon("https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png", iconWidth = 24, iconHeight =32),
                       SuperValue = makeIcon("https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png", iconWidth = 24, iconHeight =32))

#Create an instance of the leaflet object locations, the markers are coloured based on what type of location they are. 

leaflet(data = locations) %>% addTiles() %>% addMarkers(lng = ~ Long, lat = ~ Lat, icon = ~ IconsList[Type])
