### PostgresDB

#### How to export it to sql from PostgresDB.
```bash
pg_dump -U username -h localhost databasename >> yiqing.sql
```

### How to import it into PostgresDB.
```bash
psql -U username dbname < yiqing.sql
```