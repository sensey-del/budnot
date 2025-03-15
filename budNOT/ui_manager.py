from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.progress import Progress
import questionary
import time

console = Console()

def clear_console():
    """Очищает консоль."""
    console.clear()

def show_welcome_message():
    """Показывает приветственное сообщение."""
    console.print(Panel.fit("[bold green]Добро пожаловать в BudNOTAi![/bold green]"))
    console.print(Rule(style="bold cyan"))

def show_exit_message():
    """Показывает сообщение при выходе."""
    console.print(Panel.fit("[bold yellow]Спасибо за использование BudNOTAi![/bold yellow]"))

def display_categories(expenses):
    """Отображает список категорий."""
    table = Table(title="Категории расходов")
    table.add_column("Категория", justify="left")
    table.add_column("Процент", justify="right")
    table.add_column("Сумма", justify="right")
    total_percentage = 0
    for category, percentage in expenses.items():
        table.add_row(category, f"{percentage}%", "—")
        total_percentage += percentage
    table.add_row("[bold]Итого[/bold]", f"[bold]{total_percentage}%[/bold]", "—")
    console.print(table)

def display_results(recommendation, income):
    """Отображает рекомендации по расходам."""
    table = Table(title=f"Рекомендации по расходам (Доход: {income:.2f} руб.)")
    table.add_column("Категория", justify="left")
    table.add_column("Сумма", justify="right")
    for category, amount in recommendation.items():
        table.add_row(category, f"{amount:.2f} руб.")
    console.print(table)

def display_history(config):
    """Отображает историю доходов и расходов."""
    history = config.get("training_data", [])
    if not history:
        console.print("[bold yellow]История пуста.[/bold yellow]")
        return

    table = Table(title="История доходов и расходов")
    table.add_column("Доход", justify="right")
    categories = list(config["expenses"].keys())
    for category in categories:
        table.add_column(category, justify="right")

    for entry in history:
        row = [f"{entry['income']:.2f} руб."]
        for category in categories:
            amount = entry.get(category, "—")
            if isinstance(amount, (int, float)):
                row.append(f"{amount:.2f} руб.")
            else:
                row.append(amount)
        table.add_row(*row)

    console.print(table)

def analyze_expenses(config):
    """Анализирует средние расходы по категориям."""
    history = config.get("training_data", [])
    if not history:
        console.print("[bold yellow]Нет данных для анализа.[/bold yellow]")
        return

    categories = list(config["expenses"].keys())
    averages = {category: 0 for category in categories}
    for entry in history:
        for category in categories:
            averages[category] += entry.get(category, 0)

    for category in categories:
        averages[category] /= len(history)

    console.print("[bold cyan]Средние расходы:[/bold cyan]")
    for category, avg in averages.items():
        console.print(f"  [bold white]{category}[/bold white]: {avg:.2f} руб.")

def get_user_action(choices):
    """Запрашивает действие у пользователя."""
    return questionary.select("Выберите действие:", choices=choices).ask()

def get_category_input():
    """Запрашивает данные для новой категории."""
    category = questionary.text("Введите название категории:").ask()
    percentage = questionary.text("Введите процент для категории (от 0 до 100):").ask()
    return category, percentage

def get_income_input():
    """Запрашивает доход у пользователя."""
    return questionary.text("Введите ваш доход:").ask()

def calculate_recommendation(income, expenses):
    """Рассчитывает рекомендации по расходам."""
    recommendation = {}
    for category, percentage in expenses.items():
        amount = income * (percentage / 100)
        recommendation[category] = round(amount, 2)
    total_allocated = sum(recommendation.values())
    recommendation["Свободные деньги"] = income - total_allocated
    return recommendation

def show_loading_animation():
    """Показывает анимацию загрузки."""
    with Progress() as progress:
        task = progress.add_task("[cyan]Расчет рекомендаций...", total=100)
        while not progress.finished:
            progress.update(task, advance=10)
            time.sleep(0.1)

def get_fixed_amount_input(income):
    """Запрашивает фиксированную сумму для категории.? Добавить вопрос о необходимости..."""
    category = questionary.text("Введите название категории:").ask()
    fixed_amount = questionary.text("Введите фиксированную сумму:").ask()
    try:
        fixed_amount = float(fixed_amount)
        if fixed_amount > income:
            raise ValueError("Сумма не может превышать доход.")
        percentage = (fixed_amount / income) * 100
        return category, percentage
    except ValueError as e:
        console.print(f"[bold red]Ошибка: {str(e)}[/bold red]")
        return None, None
