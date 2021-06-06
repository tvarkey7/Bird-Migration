# Bird Migration Project
This project does not produce accurate results (in terms of what will actually happen in real life). Instead it just creates a graph with the current and new bird migration route on it. This was the project I created for my A-Level Computing coursework.

# Breakdown of what this project does
- 1) Introduction Window: Just a window that introduces the user to the program with a picture on it. 
- 2) CO2 Slider: This window has a slider where the user can enter a CO2 value that they would like to base predictions off. This value is saved to a text file to be recalled later. 
- 3) Bird Choice drop-down window: This window has a drop-down menu where the user is presented with the option to pick one of four bird routes that they would like to model. The birds all use the East Atlantic Flyway (EAF). The options are: Nightingale, Raptor, Eurasian Spoonbill and Barn Swallow. 
-  4) Basic Graph Plots window: In this window, the option to plot the chosen bird's current route on a map is given. The option to also plot a graph of the global temperature anomaly is also given. The button to skip to the next window is available, meaning that these buttons do not need to be clicked. Thes graph and map both open into a new window.
-  5) Plot CO2 Anomaly graph: This window only has one button. This button plots a graph of annual CO2 emissions. 
-  6) Enter a year window: This window has a textbox for input. This box is where you enter a year. There is a range for the year and the input is then validated before the user is allowed to continue to the next window. 
-  7) Plot Forecasted emissions: The next window has a button that when pressed plots a graph of the forecasted CO2 emissions. These emissions are predicted using linear regression. They are then stored to a file and then used to plot points on a graph. The year that was chosen by the user is then highlighted on the graph.
-  8) Plot projected routes: In the next window, there is a button. Once this button has been pressed, a map of the current route of the chosen bird and the projected route of the bird are then plotted on the same map and are different colours and labelled to differentiate them.
-  9) Save image window: The next window asks the user whether they would like to save the modelled route as an image. If no is pressed, the user is taken to the final window where they can exit the program. If yes is pressed, the image is saved to the same directory that the Python file is in. 
-  10) Option to email: If yes was pressed in the previous window, it goes to the next window that asks the user whether they would like to email the image to anyone. If no is pressed, the user is taken to the final window where they can exit the program. If they press yes, they are taken to the email entry window.
-  11) Email Entry Window: In this window, the user enters an email address. The email they enter is then validated using regular expressions. For example, the user cannot enter "@gmail1234.com123", as it will not fit the regular expression. 
-  12) Exit window: This window is the exit window, where there is a button that lets the user exit the program.
