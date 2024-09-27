import flet as ft
import peewee as pw

db = pw.SqliteDatabase('Banco de matrículas')

class individuo(pw.Model):
        nome = pw.CharField()
        descrição = pw.TextField()
        idade = pw.IntegerField()
        data = pw.DateField()
        mensalidade = pw.IntegerField
        class Meta:
                databse = db

def tabelas():
    db.commit()
    db.create_tables([individuo])

class Task(ft.Column):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Editar",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Deletar Task",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Atualizar Task",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_task = ft.TextField(hint_text="Nome?", expand=True)
        self.descrição = ft.TextField(hint_text='Descrição', expand=True)
        self.idade = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

        self.tasks = ft.Column()
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[ self.new_task,
                   self.descrição,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add_clicked),
                ],
            ),
            self.tasks,
        ]

    def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

def main(page:ft.Page):
    minha_aplicacao = TodoApp()
    page.title = 'Gerenciador'
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    page.add(minha_aplicacao)

ft.app(target = main)
