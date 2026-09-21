import flet as ft
import random
import string

def main(page: ft.Page):
    page.title = "Генератор паролей"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 420
    page.window.height = 680
    page.window.min_width = 360
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    password_length = 16
    include_upper = True
    include_lower = True
    include_digits = True
    include_symbols = True

    password_field = ft.TextField(
        value="",
        read_only=True,
        text_align=ft.TextAlign.CENTER,
        text_size=22,
        border_radius=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.PRIMARY,
        content_padding=20,
        expand=True,
    )

    length_text = ft.Text(f"Длина: {password_length}", size=16, weight=ft.FontWeight.W_500)

    def update_length(e):
        nonlocal password_length
        password_length = int(e.control.value)
        length_text.value = f"Длина: {password_length}"
        length_text.update()

    length_slider = ft.Slider(
        min=6,
        max=64,
        divisions=58,
        value=password_length,
        label="{value}",
        on_change=update_length,
        active_color=ft.Colors.PRIMARY,
    )

    def toggle_upper(e):
        nonlocal include_upper
        include_upper = e.control.value

    def toggle_lower(e):
        nonlocal include_lower
        include_lower = e.control.value

    def toggle_digits(e):
        nonlocal include_digits
        include_digits = e.control.value

    def toggle_symbols(e):
        nonlocal include_symbols
        include_symbols = e.control.value

    switch_upper = ft.Switch(label="Заглавные буквы (A-Z)", value=True, on_change=toggle_upper)
    switch_lower = ft.Switch(label="Строчные буквы (a-z)", value=True, on_change=toggle_lower)
    switch_digits = ft.Switch(label="Цифры (0-9)", value=True, on_change=toggle_digits)
    switch_symbols = ft.Switch(label="Символы (!@#$%...)", value=True, on_change=toggle_symbols)

    strength_bar = ft.ProgressBar(
        value=0.7,
        color=ft.Colors.GREEN,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        height=8,
        border_radius=4
    )
    strength_label = ft.Text("Надёжность: Хорошая", size=13, color=ft.Colors.GREEN)

    def generate_password(e=None):
        chars = ""
        if include_upper:
            chars += string.ascii_uppercase
        if include_lower:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            password_field.value = "Выберите хотя бы один тип символов!"
            password_field.update()
            return

        password = "".join(random.choice(chars) for _ in range(password_length))
        password_field.value = password
        password_field.update()

        score = 0
        if password_length >= 12:
            score += 1
        if password_length >= 16:
            score += 1
        if include_upper and include_lower:
            score += 1
        if include_digits:
            score += 1
        if include_symbols:
            score += 1

        if score <= 2:
            strength_bar.value = 0.3
            strength_bar.color = ft.Colors.RED
            strength_label.value = "Надёжность: Слабая"
            strength_label.color = ft.Colors.RED
        elif score <= 3:
            strength_bar.value = 0.6
            strength_bar.color = ft.Colors.ORANGE
            strength_label.value = "Надёжность: Средняя"
            strength_label.color = ft.Colors.ORANGE
        else:
            strength_bar.value = 0.9
            strength_bar.color = ft.Colors.GREEN
            strength_label.value = "Надёжность: Отличная"
            strength_label.color = ft.Colors.GREEN

        strength_bar.update()
        strength_label.update()

    def copy_password(e):
        if password_field.value and "Выберите" not in password_field.value:
            page.set_clipboard(password_field.value)
            page.open(
                ft.SnackBar(
                    content=ft.Text("Пароль скопирован в буфер обмена!"),
                    bgcolor=ft.Colors.GREEN_700,
                    duration=2000,
                )
            )

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        page.update()

    generate_btn = ft.Button(
        content="Сгенерировать",
        icon=ft.Icons.REFRESH,
        on_click=generate_password,
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.ON_PRIMARY,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        expand=True,
    )

    copy_btn = ft.OutlinedButton(
        content="Копировать",
        icon=ft.Icons.CONTENT_COPY,
        on_click=copy_password,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        expand=True,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Генератор паролей", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(
                icon=ft.Icons.BRIGHTNESS_6,
                tooltip="Сменить тему",
                on_click=toggle_theme,
            )
        ],
    )

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=password_field,
                    margin=ft.Margin.only(bottom=10),
                ),
                ft.Column(
                    [
                        strength_label,
                        strength_bar,
                    ],
                    spacing=6,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                length_text,
                length_slider,
                ft.Divider(height=10),
                ft.Text("Включить в пароль:", size=15, weight=ft.FontWeight.W_500),
                switch_upper,
                switch_lower,
                switch_digits,
                switch_symbols,
                ft.Divider(height=20),
                ft.Row(
                    [generate_btn, copy_btn],
                    spacing=12,
                ),
            ],
            spacing=8,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
    )

    generate_password()

if __name__ == "__main__":
    ft.run(main)