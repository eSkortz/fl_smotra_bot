from config import retry_async
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete


class DBWorkerAsync:
    def __init__(self, engine) -> None:
        """
        Initializes the DBWorkerAsync instance with an asynchronous database engine.

        This constructor method sets up a DBWorkerAsync instance by assigning an asynchronous SQLAlchemy engine
        to it. The engine is used for performing asynchronous database operations within the class methods. It's
        important to provide a properly configured asynchronous SQLAlchemy engine compatible with the target database.

        Parameters:
            engine (SQLAlchemy Async Engine): An asynchronous SQLAlchemy Engine object that provides connectivity
        to the database.

        Returns:
            None: This method does not return anything. It initializes the DBWorkerAsync instance.
        """
        self.engine_async = engine

    @retry_async(5)
    async def select_execute(self, stmt):
        """
        Asynchronously executes a SELECT statement and returns all fetched results.

        This method executes a given SQL SELECT statement asynchronously using SQLAlchemy's
        async_session. It opens an asynchronous session, executes the statement, and fetches all results.
        The method is decorated with 'retry_async', indicating that it will retry the operation up to 5 times
        in case of failure.

        Parameters:
            stmt (SQLAlchemy Statement): An SQL SELECT statement to be executed.

        Returns:
            list: A list of result objects fetched from the database.
        """
        async_session = async_sessionmaker(self.engine_async, expire_on_commit=True)
        async with async_session() as session:
            result = await session.execute(stmt)
            return result.all()

    @retry_async(5)
    async def session_scalars(self, stmt):
        """
        Asynchronously executes a SQL statement and returns all scalar results.

        This method executes a provided SQL statement asynchronously and fetches all scalar results using
        SQLAlchemy's async_session. It is decorated with 'retry_async', allowing for up to 5 retry attempts
        on failure.

        Parameters:
            stmt (SQLAlchemy Statement): An SQL statement to be executed.

        Returns:
            list: A list of scalar results obtained from the database.
        """
        async_session = async_sessionmaker(self.engine_async, expire_on_commit=True)
        async with async_session() as session:
            result = await session.scalars(stmt)
            return result.all()

    @retry_async(5)
    async def session_execute_commit(self, stmt):
        """
        Asynchronously executes a SQL statement and commits the transaction.

        This method opens an asynchronous session, executes the provided SQL statement, and commits the
        transaction. It is decorated with 'retry_async' and allows up to 5 retry attempts in case of failure.

        Parameters:
            stmt (SQLAlchemy Statement): An SQL statement to be executed and committed.

        Returns:
            None: This method does not return anything.
        """
        async_session = async_sessionmaker(self.engine_async, expire_on_commit=True)
        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()

    async def custom_orm_select(
        self,
        cls_from,
        where_params: list = None,
        sql_limit: int = None,
        join_on: list or dict = None,
        order_by: list = None,
        distinct: bool = None,
        group_by: list = None,
    ) -> list:
        """
        Asynchronously performs a custom SELECT operation with various optional parameters.

        This method constructs and executes a SELECT statement asynchronously using the provided class list,
        optional WHERE clauses, limit, and JOIN conditions. It supports both single and multiple class queries.

        Parameters:
        - cls_from (list): List of ORM classes to select from.
        - where_params (list, optional): Optional WHERE clause conditions.
        - sql_limit (int, optional): Optional limit on the number of records fetched.
        - join_on (list | dict, optional): Optional JOIN conditions.
        - order_by (list, optional): Optional sorting conditions.
        - distinct (bool, optional): Indicates the use of DISTINCT in the query.
        - group_by (list, optional): Optional GROUP BY conditions.

        Returns:
        - list: A list of result objects or scalars fetched from the database.
        """
        stmt = select(*cls_from) if isinstance(cls_from, list) else select(cls_from)

        if join_on:
            stmt = (
                stmt.join(*join_on)
                if isinstance(join_on, list)
                else stmt.join(**join_on)
            )

        if where_params:
            stmt = stmt.where(*where_params)

        if sql_limit:
            stmt = stmt.limit(sql_limit)

        if order_by:
            stmt = stmt.order_by(*order_by)

        if distinct:
            stmt = stmt.distinct()

        if group_by:
            stmt = stmt.group_by(*group_by)

        if isinstance(cls_from, list):
            return await self.select_execute(stmt)
        return await self.session_scalars(stmt)

    @retry_async(5)
    async def custom_orm_bulk_update(self, cls_to, data: list):
        """
        Asynchronously performs a bulk update operation on a specified ORM class with the given data.

        This method opens an asynchronous session, executes a bulk UPDATE operation on the specified ORM class
        using the provided data list, and commits the transaction. It is decorated with 'retry_async'
        and allows up to 5 retry attempts on failure.

        Parameters:
        - cls_to (ORM Class): The ORM class on which the bulk update is to be performed.
        - data (list): A list of dictionaries containing the data to be updated.

        Returns:
        None: This method does not return anything.
        """
        async_session = async_sessionmaker(self.engine_async, expire_on_commit=True)
        async with async_session() as session:
            await session.execute(update(cls_to), data)
            await session.commit()

    async def custom_insert_do_nothing(
        self,
        cls_to,
        index_elements: list[str],
        data: list[dict],
    ):
        """
        Asynchronously inserts data into a table with a 'DO NOTHING' conflict resolution.

        This method constructs and executes an asynchronous INSERT statement that inserts data into a table
        with a 'DO NOTHING' conflict resolution. It is useful when you want to avoid inserting duplicate
        records based on specific index elements.

        Parameters:
        - cls_to (ORM Class): The ORM class representing the table.
        - index_elements (list[str]): List of index elements used to determine conflicts.
        - data (list[dict]): List of dictionaries containing the data to be inserted.

        Returns:
        None: This method does not return anything.
        """
        stmt = (
            insert(cls_to)
            .values(data)
            .on_conflict_do_nothing(index_elements=index_elements)
        )
        await self.session_execute_commit(stmt)

    async def custom_upsert(
        self, cls_to, index_elements: list[str], data: list[dict], update_set: list[str]
    ):
        """
        Asynchronously performs an upsert operation (insert or update) on the specified ORM class.

        This method constructs and executes an asynchronous 'upsert' statement that inserts or updates records
        based on conflict resolution. It utilizes the provided ORM class, index elements, data, and fields to update
        in case of a conflict.

        Parameters:
        - cls_to (ORM Class): The ORM class on which to perform the upsert operation.
        - index_elements (list[str]): List of index elements used to determine conflicts.
        - data (list[dict]): List of dictionaries containing the data to be inserted or updated.
        - update_set (list[str]): List of fields to update in case of a conflict.

        Returns:
        None: This method does not return anything.
        """
        stmt = insert(cls_to).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements=index_elements,
            set_={x: getattr(stmt.excluded, x) for x in update_set},
        )
        await self.session_execute_commit(stmt)

    async def custom_insert(self, cls_to, data: list[dict]):
        """
        Asynchronously inserts multiple records into a specified table in the database.

        This function uses an asynchronous session to insert a list of records into the specified table.
        It opens a session, executes the insert operation with the provided data, and commits the transaction.
        If an exception occurs during the process, it prints the exception.

        Parameters:
        - cls_to (Class): The class corresponding to the table into which data is to be inserted.
        - data (list[dict]): A list of dictionaries, where each dictionary represents a record to be inserted.

        Returns:
        None: This function does not return anything. It either successfully inserts the records
        or prints an exception if an error occurs.
        """
        stmt = insert(cls_to).values(data)
        await self.session_execute_commit(stmt)

    async def custom_orm_delete(self, cls_from, where_params: list = None):
        """
        Asynchronously deletes records from a specified table in the database based on optional conditions.

        This function uses an asynchronous session to delete records from a table. If no conditions are provided,
        it deletes all records. If conditions are specified using the 'where_params' list, it adds a WHERE clause
        to the delete statement to filter records based on the given conditions.

        Parameters:
        - cls_from (Class or list): The class or list of classes corresponding to the table(s) from which records
        are to be deleted.
        - where_params (list, optional): A list of conditions to filter records for deletion.
        Each condition should be a valid SQLAlchemy expression to be used in the WHERE clause.

        Returns:
        None: This function does not return anything. It either successfully deletes the records
        or prints an exception if an error occurs.
        """
        stmt = delete(*cls_from) if isinstance(cls_from, list) else delete(cls_from)
        if where_params:
            stmt = stmt.where(*where_params)
        await self.session_execute_commit(stmt)
