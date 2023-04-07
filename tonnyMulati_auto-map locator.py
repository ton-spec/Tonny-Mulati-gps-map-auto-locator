
import gpsd
import folium
from folium.plugins import MarkerCluster, MeasureControl

try:
    # Connect to the local GPS daemon
    gpsd.connect()

    # Get the GPS data
    packet = gpsd.get_current()

    # Check if the data is valid
    if packet.mode >= 2:
        # Get the current latitude and longitude coordinates
        current_latitude = packet.lat
        current_longitude = packet.lon

        # create a map centered on your current location
        m = folium.Map(location=[current_latitude, current_longitude], zoom_start=12)

        # add markers for businesses near your current location
        marker_cluster = MarkerCluster().add_to(m)

        # ask user to input new marker for the nearby location and popup text
        new_marker_location = input("Enter the location of the new marker (latitude,longitude): ")
        new_marker_popup = input("Enter the text for the popup of the new marker: ")

        # add new marker to the map
        try:
            latitude, longitude = map(float, new_marker_location.split(','))
            folium.Marker(
                location=[latitude, longitude],
                popup=new_marker_popup,
                icon=folium.Icon(color="cadetblue")
            ).add_to(marker_cluster)
        except ValueError:
            print("Invalid latitude or longitude")

        # add a layer control to the map for switching between different layers
        folium.LayerControl().add_to(m)

        # add a search bar to the map for searching for places
        folium.plugins.Search().add_to(m)

        # add a full screen button to the map for expanding to full screen view
        folium.plugins.Fullscreen().add_to(m)

        # add a measure control to the map for measuring distances and areas
        measure_control = MeasureControl(
            position='topleft',
            primary_length_unit='miles',
            primary_area_unit='sqmeters'
        )
        m.add_child(measure_control)

        # display the map
        m

    else:
        print("Sorry, no GPS signal. Try again!")
except gpsd.NoGPSDataError:
    print("No GPS data available")
except gpsd.gpscommon.SocketError:
    print("Unable to connect to GPS daemon")
