#Random article generator.

The application allows you to get a random (based on the random module) article on the selected topic after clicking the "Get article" button.

The application consists of two pages:
1. Topic selection page.
2. Result page.
 
###Topic selection page.
The user can choose one of the displayed topics. The topics themselves are represented by buttons at the top of the page: “Geography”, “History”, “Science”, etc. After clicking on the button, its name is duplicated in the central part of the page, by default - the name of the "History" button is duplicated.
In the center of the page there is a button “Get article”. After clicking it, a python script based on the random module is executed, in which an article is selected from those offered by the wikipedia resource on the selected topic and a transition to the result page is made.

###Result page.
In the central part of the page, the text from the article is displayed, below the "Back" button is located, which moves to the previous page.
