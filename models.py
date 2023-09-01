""" User
-
user_id PK int
Name string INDEX
Address string
email string
password string
phone int 


Trips
-
trip_id PK int
user_id int FK >- User.user_id
destination_id int FK >- Destination.dest_id
iten_id int FK >- Itinerary.iten_id


Destination
-
dest_id PK int
name string
comment_id int FK >- Comments.comment_id


Itinerary
-
iten_id PK int
dates string
comments NULL string
budget NULL int


Comments
-
comment_id PK int
user_id int FK >- User.user_id
destination_id int FK >- Destination.dest_id


users_trips
- 
user_id int PK FK >- User.user_id
trip_id int PK FK >- Trips.trip_id


users_comments
-
user_id int PK FK >- User.user_id
comment_id int PK FK >- Comments.comment_id


 """