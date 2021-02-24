# RARE Publishing Platform API 

> Nashville Software School Group Project for Indomitable Icicles 

## The Concept

This server code pairs with the Rare Publishing Platform React App which can be found here https://github.com/nss-day-cohort-44/rare-indomitable-icicles

The Rare App allows users to login/logout, make, view, edit, and comment their own posts, as well as the posts of other users.

The following Entity Relationship Diagram details the layout of our data tables:

![IciclesERD.png](IciclesERD.png)

## Features

* Full CRUD endpoints for Users, Posts, Tags, Categories, Comments.
* Query endpoints to return data lists by various id categories.
* Access and control of database through SQLite statements.

## Setting Up Database

### Pulling down the Server-Side Repo. 
 
> Note: This project is meant to run simultaneously with the Client-Side Repo found here: https://github.com/nss-day-cohort-44/rare-rabid-sharks  
 
> Depending on which repo you start with, you may already have the following directories set up.  
> This project requires Python  
 
### To Begin installing the Server-Side Repo, complete the following steps: 
 
1. Create a directory from which to deploy the application. 
	
```mkdir RARE ```
 
2. Within RARE, create two sub-directories, CLIENT and SERVER 

```mkdir CLIENT ```
	
```mkdir SERVER ```
 
3. Navigate into the SERVER sub-directory. 
 
```cd CLIENT ```
 
4. Enter the following commands: 
	
```git clone git@github.com:nss-day-cohort-44/rare-rabid-sharks.git .``` <-- note the single 	
dot preceded by a single space.  
 
5. Create a virtual environment: 
```pipenv shell```

6. Once the virtual environment is created, install the 3rd-party software. 

```pipenv install autopep8 watchgod ```

7. Enter in the following command to start your new data server written in Python: 

```watchgod request_handler.main ```

> If there are no errors in the code, you will see the following, terse output:  
 
```watchgod request_handler.main [09:34:37] watching "/Users/.../workspace/python-server" and reloading "request_handler.main" on changes…``` 

## Create/Seed the Database

We have provided an SQL script for you to run to build the database. There some INSERT statements they provided. You may create as many INSERT statements as needed to seed the database to your satisfaction.

```sql
CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');
```

## Screenshots

![myPosts.png](myPosts.png)


## A guided workflow, if it so interests you

1. Register a new account. **Do not use any sensitive credentials. This is not a secure application!** 
1. Make a post of your own or view other users posts and comment on them.
1. Edit or delete any of your own posts or comments.
1. Add, edit, or delete Categories for your posts.
1. Add, edit, or delete Tags for your posts.

## Technologies Used

This application was built using Python, Postman, and SQLite3  

## Author

NSS Cohort 44 Indomitable Icicles Team (Jasmin Kaset, Matthew Machurek, Erica Phillips, Leo Rondeau, Benjamin Schweizer)
