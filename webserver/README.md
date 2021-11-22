Practical 6 parts 2 webserver
by TKXCHR001 and SWNNIS001

logs should state if the connection to the client ws successful or not. if not it will restart the 
services, else you will see that the connection was successful. Follow the instructions below to 
get the desired results:

ensure public device url is enabled. once all updates are complete and the service 
begins to run, click the icon next to the public device url. You should be taken to 
a new tab in the browser. 

You will be greeted with six options to choose from

log download - will download all previous entries of the sensors into a .csv file
log check - displays the last 10 entries of the sensors
sensors on - turns the sensors on(status will be confirmed on logs of balena)
sensors off - turns the sensors off(status will be confirmed on logs of balena)
status - checks the status of the sensors on the clients side(status will be confirmed on logs of balena)
Exit- terminates the server and client

for sensors on and off and status, after clicking them you should see a page
saying internal server error. dont be alarmed. just exit the current tab and go back to 
the balena tab. you should see the relevent messsages in the logs


