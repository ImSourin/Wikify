# Wikify
## Introduction
Wikify is a REST API service with CRUD operations on extracting information from a Wikipedia page.
## Installation
1. Download the project zip and extract it. The download link is :<br>
   `https://github.com/ImSourin/Wikify/archive/master.zip`
2. Change your current working directory to the project directory.
3. Install all the required packages using the following command:<br>
   `pip install -r requirements.txt`
4. To use the api service, two things can be done.
    Either the hosted server can be used or the local server can be hosted and used.
   1. For using the hosted service, simply run the following command after changing the directory to Wikify/test.<br>
    `python test.py`
   2. For using the locally hosted server, first host the server by running the following command.<br>
    `python run.py`
    Then, move to the test directory and open the test.py file. **Uncomment** the line `url = localurl` and in the test directory run the following command:<br>
    `python test.py`
## Initial State
* The table initially contains 2 entries :
  * name : "Scahin_Tendulkar", params : [api_urls.references.reference_lists[0].id, thumbnail.width, namespace.id] 
  * name : "Stack_Overflow", params : [api_urls.references.reference_lists[0].id, thumbnail.width, namespace.id]
## Working
1. The `insert` method (`POST` requests) receives request for inserting a new entry in the database.
    It receives a name and may or may not receive any fields in the form of a json object.
    It creates a new table entry if the database constraints are all satisfied.
2. The `delete` method (`DELETE` requests) receives a name for deleteion from the table. If such a name exists in 
    the table, then the table entry is deleted or else an error is thrown.
3. The `update` method (`PUT` requests) receives a request to update a table entry. It receives a json object containing add
    and remove params along with name. The params in add are added to the table entry params and the ones 
    in the remove section removed from the table entry params.
4. The `query` method (`GET` requests) receives a query of the user in the form of a json object containing name and parameter list for 
    which data values are needed. It checks for any error in the request and if not serves the request. 