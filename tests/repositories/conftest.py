from pytest import fixture
from sqlalchemy import text

from app.db.db import DataBase
from app.repositories.users import UsersRepository


@fixture(scope='package')
def users_repo(db: DataBase) -> UsersRepository:
    return UsersRepository(db.get_session)


@fixture(scope='function')
def clean_db(db: DataBase):
    with db.get_session() as session:
        session.execute(text('''
            do $$
            DECLARE
                seq_name text; 
                statements CURSOR FOR
                    SELECT tablename FROM pg_tables
                    WHERE schemaname = 'public';
            BEGIN
                FOR stmt IN statements LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
                END LOOP;

                FOR seq_name IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP 
                EXECUTE 'SELECT setval(' || quote_literal(seq_name) || ', 1, false)'; 
                END LOOP;

            END $$ LANGUAGE plpgsql;
        '''))
        session.commit()
