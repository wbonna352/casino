CREATE PUBLICATION debezium_publication FOR TABLE players;
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');
