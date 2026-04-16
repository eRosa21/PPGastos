import flet as ft

def main(page: ft.page):

    def add_task(e):
        print("R$: "+ new_task.value)

    new_task = ft.TextField(hint_text="R$: ")
    new_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click = add_task)


    page.add(new_task, new_button)

ft.app(target = main)
 