
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
		'63',
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
		'administrator',
		'63',
		'123456',
		'pbkdf2:sha1:1000$TeH6nWAu$74eb40f6377417426c103c260c7cb3e10b160a70',
		'2016-06-24 11:40:53.744011',
		'2016-06-24 10:12:48.690093'
	);

COMMIT;
```