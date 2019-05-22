CREATE TABLE "User" (
	"id" serial NOT NULL,
	"first_name" TEXT NOT NULL,
	"last_name" TEXT NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"last_visit" TIMESTAMP NOT NULL,
	CONSTRAINT User_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Message" (
	"id" serial NOT NULL,
	"dialog_id" integer NOT NULL,
	"content_id" integer NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"to_id" integer NOT NULL,
	CONSTRAINT Message_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Content" (
	"id" serial NOT NULL,
	"content" TEXT NOT NULL,
	CONSTRAINT Content_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Dialog" (
	"id" serial NOT NULL,
	"name" serial NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	CONSTRAINT Dialog_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "DialogsUsers" (
	"user_id" integer NOT NULL,
	"dialog_id" integer NOT NULL,
	"permission" integer
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Ban_List" (
	"id" serial NOT NULL,
	"to_id" integer NOT NULL,
	CONSTRAINT Ban_List_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Authentication" (
	"user_id" integer NOT NULL,
	"login" TEXT NOT NULL,
	"password" TEXT NOT NULL
) WITH (
  OIDS=FALSE
);




ALTER TABLE "Message" ADD CONSTRAINT "Message_fk0" FOREIGN KEY ("dialog_id") REFERENCES "Dialog"("id");
ALTER TABLE "Message" ADD CONSTRAINT "Message_fk1" FOREIGN KEY ("content_id") REFERENCES "Content"("id");
ALTER TABLE "Message" ADD CONSTRAINT "Message_fk2" FOREIGN KEY ("to_id") REFERENCES "User"("id");



ALTER TABLE "DialogsUsers" ADD CONSTRAINT "DialogsUsers_fk0" FOREIGN KEY ("user_id") REFERENCES "User"("id");
ALTER TABLE "DialogsUsers" ADD CONSTRAINT "DialogsUsers_fk1" FOREIGN KEY ("dialog_id") REFERENCES "Dialog"("id");

ALTER TABLE "Ban_List" ADD CONSTRAINT "Ban_List_fk0" FOREIGN KEY ("id") REFERENCES "User"("id");

ALTER TABLE "Authentication" ADD CONSTRAINT "Authentication_fk0" FOREIGN KEY ("user_id") REFERENCES "User"("id");

