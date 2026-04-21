tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

insert_task = 'INSERT INTO tasks (task) VALUES (?)'

select_tasks = 'SELECT * FROM tasks'

select_tasks_completed = 'SELECT * FROM tasks WHERE completed = 1'

select_tasks_uncompleted = 'SELECT * FROM tasks WHERE completed = 0'

update_task = 'UPDATE tasks SET task = ? WHERE id = ?'

delete_task = 'DELETE FROM tasks WHERE id = ?'

delete_completed_tasks = 'DELETE FROM tasks WHERE completed = 1'