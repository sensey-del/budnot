#!/usr/bin/env python3
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from budNOT.config_manager import load_config, save_config, clear_config, clear_incomes, clear_categories
from budNOT.ui_manager import (
    display_categories, display_results, clear_console,
    get_user_action, get_category_input, get_income_input, console,
    show_welcome_message, show_exit_message, display_history, analyze_expenses,
    calculate_recommendation, show_loading_animation, get_fixed_amount_input
)
import questionary

def main():
    config = load_config()
    show_welcome_message()

    while True:
        clear_console()
        console.print(Panel.fit("[bold cyan]Текущие данные:          [/bold cyan]"))
        if not config["expenses"]:
            console.print("[bold red]⚠ Категории расходов не заданы.[/bold red]")
        else:
            display_categories(config["expenses"])

        action = get_user_action([
            "Ввести доход и получить рекомендацию",
            "Добавить категорию",
            "Изменить категорию",
            "Удалить категорию",
            "Показать историю",
            "Средние показатели",
            "Очистить данные",
            "Выход"
        ])

        if action == "Очистить данные":
            clear_action = get_user_action([
                "Очистить доходы",
                "Очистить категории",
                "Очистить всё",
                "Назад"
            ])

            if clear_action == "Очистить доходы":
                config = clear_incomes(config)
            elif clear_action == "Очистить категории":
                config = clear_categories(config)
            elif clear_action == "Очистить всё":
                config = clear_config()
            console.print("[bold green]Данные успешно очищены![/bold green]")
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Добавить категорию":
            category, percentage_input = get_category_input()
            try:
                percentage = float(percentage_input)
                if 0 <= percentage <= 100:
                    config["expenses"][category] = percentage
                    save_config(config)
                    console.print(f"[bold green]Категория '{category}' добавлена с процентом {percentage}%.[/bold green]")
                else:
                    console.print("[bold red]Ошибка: процент должен быть в диапазоне от 0 до 100.[/bold red]")
            except ValueError:
                console.print("[bold red]Ошибка: Введите корректное числовое значение для процента.[/bold red]")
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Изменить категорию":
            if not config["expenses"]:
                console.print("[bold red]Нет категорий для изменения![/bold red]")
            else:
                category = questionary.select(
                    "Выберите категорию для изменения:",
                    choices=list(config["expenses"].keys())
                ).ask()

                if category:
                    percentage_input = questionary.text("Введите новый процент для категории (от 0 до 100):").ask()
                    try:
                        percentage = float(percentage_input)
                        if 0 <= percentage <= 100:
                            config["expenses"][category] = percentage
                            save_config(config)
                            console.print(f"[bold blue]Категория '{category}' обновлена с новым процентом {percentage}%.[/bold blue]")
                        else:
                            console.print("[bold red]Ошибка: процент должен быть в диапазоне от 0 до 100.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Ошибка: Введите корректное числовое значение для процента.[/bold red]")
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Удалить категорию":
            if not config["expenses"]:
                console.print("[bold red]Нет категорий для удаления![/bold red]")
            else:
                category = questionary.select(
                    "Выберите категорию для удаления:",
                    choices=list(config["expenses"].keys())
                ).ask()

                if category:
                    del config["expenses"][category]
                    save_config(config)
                    console.print(f"[bold yellow]Категория '{category}' удалена.[/bold yellow]")
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Ввести доход и получить рекомендацию":
            income_input = get_income_input()
            try:
                income = float(income_input)
                if income <= 0:
                    raise ValueError("Доход должен быть положительным числом.")
            except ValueError as e:
                console.print(f"[bold red]Ошибка: {str(e)}[/bold red]")
                input("Нажмите Enter, чтобы продолжить...")
                continue

            # Запрос фиксированной суммы
            fixed_category, fixed_percentage = get_fixed_amount_input(income)
            if fixed_category and fixed_percentage:
                config["expenses"][fixed_category] = fixed_percentage
                save_config(config)
                console.print(f"[bold green]Категория '{fixed_category}' добавлена с процентом {fixed_percentage:.2f}%.[/bold green]")

            show_loading_animation()
            recommendation = calculate_recommendation(income, config["expenses"])
            display_results(recommendation, income)

            save_action = questionary.select(
                "Сохранить или удалить?",
                choices=["Сохранить", "Удалить"]
            ).ask()

            if save_action == "Сохранить":
                training_data = config.get("training_data", [])
                training_data.append({"income": income, **recommendation})
                config["training_data"] = training_data
                save_config(config)
                console.print("[bold green]Рекомендации сохранены успешно![/bold green]")
            else:
                console.print("[bold yellow]Рекомендации не сохранены.[/bold yellow]")
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Показать историю":
            display_history(config)
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Средние показатели":
            analyze_expenses(config)
            input("Нажмите Enter, чтобы продолжить...")

        elif action == "Выход":
            show_exit_message()
            break

if __name__ == "__main__":
    main()
