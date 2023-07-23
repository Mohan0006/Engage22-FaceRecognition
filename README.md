Steps to run the web application on the local machine :

Install all the requirements mentioned in the requirements.txt also the runserver extension

1. Clone the github repository into a folder.
2. Open the folder in vs code
3. open the terminal and run the command "py manage.py runserver"
4. open this link in your web browser http://127.0.0.1:8000/
5. now you can upload the image and can get the results Note : A face is recognised only if face detection score is greatear than 0.7 and identified only if face score is greater than 0.44. I had kept these constraints for better results. So uploading the good quality images is suggested for better results.

The Web app can only recognise loyal or repeat customers (i.e., the machine learning model is trained over the data set consisting of images of loyal customers), and for the remaining people, it shows their status as unknown.
Those loyal customers are: (I had assumed, created a data set, and trained an ML model.)
George W Bush,  
Sachin Tendulkar,  
James Anderson,  
Rohit Sharma,  
Virat Kohli,  
Robert Downey Jr,  
Barack Obama,           
Donald Trump,           
Scarlett Johansson,    
Elon Musk,            
Kapil Dev,            
Lionel Messi,          
Roger Federer,         
Cristiano Ronaldo,     
Salman Khan,           
Leonardo DiCaprio,     
Aamir Khan,            
Angelina Jolie,         
Joe Biden,              
Tom Curise 


I had uploaded the webpage "ScreenShots" in the ScreenShots folder in repository. In the "Testing Pictures" Folder You can see some pictures used for testing the webapp.

On adding /admin to home page url you will be redirected to admin login portal and after entering the credintials mentioned in acehacker form you will be redirected to the admin portal.
