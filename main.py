import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = "Список покупок"

    main_db.init_db()

    tasks_column = ft.Column()
    counter_text = ft.Text()
    filter_type = "all"

    def load_tasks():
        tasks_column.controls.clear()

        tasks = main_db.get_tasks(filter_type)
        if not tasks:
            tasks_column.controls.append(ft.Text("Список пуст"))    

        for task in tasks:
            task_id, task_text, completed = task

            checkbox = ft.Checkbox(
                value=bool(completed),
                label=task_text,
                on_change=lambda e, i=task_id: toggle(i)
            )

            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                on_click=lambda e, i=task_id: delete(i)
            )

            tasks_column.controls.append(ft.Row([checkbox, delete_btn]))

        update_counter()
        page.update()

    def add(e):
        if task_input.value.strip() == "":
            return

        main_db.add_task(task_input.value)

        task_input.value = ""
        load_tasks()

    def toggle(task_id):
        tasks = main_db.get_tasks("all")
        for t in tasks:
            if t[0] == task_id:
                new_status = 0 if t[2] else 1
                main_db.update_task(task_id, completed=new_status)
                break
        load_tasks()

    def delete(task_id):
        main_db.delete_task(task_id)
        load_tasks()

    def delete_completed(e):
        main_db.delete_completed_tasks()
        load_tasks()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_tasks()

    def update_counter():
        tasks = main_db.get_tasks("all")
        done = sum(1 for t in tasks if t[2])
        total = len(tasks)
        counter_text.value = f"Куплено: {done} / {total}"

    task_input = ft.TextField(hint_text="Введите товар", expand=True)

    add_btn = ft.ElevatedButton("ADD", on_click=add)

    filters = ft.Row([
        ft.TextButton("Все", on_click=lambda e: set_filter("all")),
        ft.TextButton("Купленные", on_click=lambda e: set_filter("completed")),
        ft.TextButton("Не купленные", on_click=lambda e: set_filter("uncompleted")),
    ])

    delete_completed_btn = ft.ElevatedButton(
        "Удалить купленные",
        on_click=delete_completed
    )

    page.add(
        ft.Text("Список покупок", size=24),
        ft.Row([task_input, add_btn]),
        filters,
        counter_text,
        delete_completed_btn,
        tasks_column
    )

    load_tasks()


ft.run(main, view=ft.AppView.WEB_BROWSER)