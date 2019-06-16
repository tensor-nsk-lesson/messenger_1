CREATE TABLE "users" (
	"id" serial NOT NULL,
	"first_name" TEXT NOT NULL,
	"second_name" TEXT NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"last_visit" TIMESTAMP NOT NULL,
	"is_blocked" BOOLEAN NOT NULL,
	"is_online" BOOLEAN NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	"is_confirmed" BOOLEAN NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "chat" (
	"id" serial NOT NULL,
	"name" TEXT,
	"created_at" TIMESTAMP NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	CONSTRAINT "chat_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "messages_users" (
	"id" serial NOT NULL,
	"chat_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"message_id" integer NOT NULL,
	CONSTRAINT "messages_users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "auth" (
	"user_id" integer NOT NULL,
	"login" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"email" TEXT NOT NULL,
	CONSTRAINT "auth_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "relationship" (
	"id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"user2_id" integer NOT NULL,
	"status" integer,
	CONSTRAINT "relationship_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "message" (
	"id" serial NOT NULL,
	"content" TEXT NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"section_id" integer NOT NULL,
	"is_edited" BOOLEAN NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	CONSTRAINT "message_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "permissions_users" (
	"id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"chat_id" integer NOT NULL,
	"permission" integer,
	CONSTRAINT "permissions_users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);





ALTER TABLE "messages_users" ADD CONSTRAINT "messages_users_fk0" FOREIGN KEY ("chat_id") REFERENCES "chat"("id");
ALTER TABLE "messages_users" ADD CONSTRAINT "messages_users_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "messages_users" ADD CONSTRAINT "messages_users_fk2" FOREIGN KEY ("message_id") REFERENCES "message"("id");

ALTER TABLE "auth" ADD CONSTRAINT "auth_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "relationship" ADD CONSTRAINT "relationship_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "relationship" ADD CONSTRAINT "relationship_fk1" FOREIGN KEY ("user2_id") REFERENCES "users"("id");


ALTER TABLE "permissions_users" ADD CONSTRAINT "permissions_users_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "permissions_users" ADD CONSTRAINT "permissions_users_fk1" FOREIGN KEY ("chat_id") REFERENCES "chat"("id");

