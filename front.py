import flet as ft

def main(page: ft.Page):

    def add_task(e):
        print("R$: "+ new_task.value)
        new_task.value = " "
        page.update()

    new_task = ft.TextField(hint_text="R$: ", expand = True )
    new_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click = add_task)


    interface = ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                new_task,
                                new_button,
                            ]
                        )
                    ]
                )

    page.add(interface)

ft.app(target = main)
 