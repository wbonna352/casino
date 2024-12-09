CREATE PUBLICATION debezium_publication FOR ALL TABLES;
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');
