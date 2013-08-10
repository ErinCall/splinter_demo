step("""
        create table "user" (
            id serial primary key,
            email text
        )
     """,
     """
        drop table user
     """)
