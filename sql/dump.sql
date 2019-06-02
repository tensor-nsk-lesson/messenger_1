CREATE TABLE "users" (
	"id" serial NOT NULL,
	"first_name" TEXT NOT NULL,
	"second_name" TEXT NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"last_visit" TIMESTAMP NOT NULL,
	"is_blocked" BOOLEAN NOT NULL,
	"is_online" BOOLEAN NOT NULL,
	"is_deleted" BOOLEAN NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "messages" (
	"id" serial NOT NULL,
	"dialog_id" integer NOT NULL,
	"content" TEXT NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"user_id" integer NOT NULL,
	"section_id" integer NOT NULL,
	CONSTRAINT messages_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "dialogs" (
	"id" serial NOT NULL,
	"name" TEXT,
	"created_at" TIMESTAMP NOT NULL,
	CONSTRAINT dialogs_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "dialogUser" (
	"dialog_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"permission" integer DEFAULT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "authentications" (
	"user_id" integer NOT NULL,
	"login" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	CONSTRAINT authentications_pk PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "relationships" (
	"id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"status" integer,
	CONSTRAINT relationships_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "messages" ADD CONSTRAINT "messages_fk0" FOREIGN KEY ("dialog_id") REFERENCES "dialogs"("id");
ALTER TABLE "messages" ADD CONSTRAINT "messages_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "dialogUser" ADD CONSTRAINT "dialogUser_fk0" FOREIGN KEY ("dialog_id") REFERENCES "dialogs"("id");
ALTER TABLE "dialogUser" ADD CONSTRAINT "dialogUser_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "authentications" ADD CONSTRAINT "authentications_fk0" FOREIGN KEY ("user_id") REFERENCES "users"("id");

ALTER TABLE "relationships" ADD CONSTRAINT "relationships_fk0" FOREIGN KEY ("id") REFERENCES "users"("id");

