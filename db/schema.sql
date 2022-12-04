CREATE TABLE task (
   task_id SERIAL PRIMARY KEY, 
   description VARCHAR(255),
   points INT,
   deadline DATE,
   created_on TIMESTAMP,
   updated_on TIMESTAMP
);

CREATE TABLE "user" (
   user_id INT PRIMARY KEY,
   slack_user_id VARCHAR(255)
);

CREATE TABLE assignment (
   user_id INT,  
   assignment_id INT PRIMARY KEY, 
   progress FLOAT,
   assignment_created_on TIMESTAMP,
   dassignment_updated_on TIMESTAMP,
   FOREIGN KEY(user_id)
      REFERENCES "user"(user_id),
   FOREIGN KEY(assignment_id)
      REFERENCES task(task_id)   
);

ALTER TABLE assignment
  RENAME COLUMN dassignment_updated_on TO assignment_updated_on;