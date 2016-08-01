
# Create User and DateBase 

```sql
CREATE ROLE "narwhal" LOGIN PASSWORD '1234qwer';

CREATE DATABASE "narwhal"  WITH OWNER "narwhal" ENCODING 'UTF8';
```

# Create Administrator

```sql
BEGIN;

INSERT INTO "public"."user"
VALUES
	(
		'1',
		'Administrator',
		'管理员',
		'male',
		'administrator',
		'127',
		'123456',
		'pbkdf2:sha1:1000$TeH6nWAu$74eb40f6377417426c103c260c7cb3e10b160a70',
		'2016-06-24 11:40:53.744011',
		'2016-06-24 10:12:48.690093'
	);

COMMIT;
```

```sql
BEGIN;

INSERT INTO "public"."user"
VALUES
	(
		'1',
		'xiongfei',
		'熊飞',
		'male',
		'leader',
		'127',
		'123456',
		'pbkdf2:sha1:1000$TeH6nWAu$74eb40f6377417426c103c260c7cb3e10b160a70',
		'2016-06-24 11:40:53.744011',
		'2016-06-24 10:12:48.690093'
	);

COMMIT;
```

```sql
BEGIN;

INSERT INTO "public"."user"
VALUES
	(
		'1',
		'zhaojiagang',
		'赵家刚',
		'male',
		'director',
		'127',
		'123456',
		'pbkdf2:sha1:1000$TeH6nWAu$74eb40f6377417426c103c260c7cb3e10b160a70',
		'2016-06-24 11:40:53.744011',
		'2016-06-24 10:12:48.690093'
	);

COMMIT;
```

```sql
INSERT INTO "public"."support"(
	"parent_id",
	"creator_id",
	"name",
	"isDirectory",
	"createTime"
)
VALUES
	(
		NULL,
		'1',
		'ROOT',
		't',
		'2016-07-31 00:00:00'
	) RETURNING *;
```