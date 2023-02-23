USE board;

INSERT INTO user(id, username, password) VALUES ("3f06af63-a93c-11e4-9797-00505690773f", "hogil", "1234");

INSERT INTO post(title, brief_description, user_id) VALUES("hi", "Great view!", "3f06af63-a93c-11e4-9797-00505690773f");

INSERT INTO post_content(post_id, content, large_content) VALUES(1, "Greate view! Have a nice day.", "0x89504E470D0A1A0A");

INSERT INTO comment(id, content, user_id, post_id) VALUES(1, "So Amazing!", "3f06af63-a93c-11e4-9797-00505690773f", 1);