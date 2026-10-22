import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TUITION_RATE = 459.54
LAB_FEE_PER_SUBJECT = 3429.30
HANDS_ON_FEE_PER_SUBJECT = 2341.86
MIN_DOWN_PAYMENT = 3500.00
EXAM_PAYMENTS = [
    ("1st Prelim", 0.15), ("1st Grading", 0.25),
    ("2nd Prelim", 0.15), ("Midterm", 0.30), ("Finals", 0.15),
]
ORANGE, INK, MUTED = "#F58220", "#292929", "#6B7280"
PALE_ORANGE, BORDER = "#FFF3E8", "#F0D8C5"

LOGO = "bctlogoss.png"
PROGRAMMERS = [
    {"name": "Jhon Patrick Tacio", "course": "BSIT-3",
     "school": "Baguio College of Technology", "birthday": "09/17/2006",
     "photo": "jhon.jpg"},
    {"name": "Jay Edmar Alcantara", "course": "BSIT-3",
     "school": "Baguio College of Technology", "birthday": None,
     "photo": "edmar.jpeg"},
    {"name": "Rolly Elefante", "course": "BSIT-3",
     "school": "Baguio College of Technology", "birthday": None,
     "photo": "rolly.jpeg"},
]

IMG_CONTAIN = getattr(getattr(ft, "ImageFit", None), "CONTAIN", None) or ft.BoxFit.CONTAIN
IMG_COVER = getattr(getattr(ft, "ImageFit", None), "COVER", None) or ft.BoxFit.COVER


def peso(value):
    return f"₱{value:,.2f}"


def main(page: ft.Page):
    page.title = "BCT Tuition Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ORANGE)
    page.bgcolor = "#FFFFFF"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.width, page.window.height = 390, 844
    page.window.min_width, page.window.min_height = 320, 600

    nav = {"current": "home", "previous": "home"}

    def field(label, hint, icon):
        return ft.TextField(label=label, hint_text=hint,
            keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=icon,
            border_color=BORDER, focused_border_color=ORANGE, border_radius=12,
            filled=True, bgcolor="#FFFFFF", text_size=15)

    units = field("Total units enrolled", "Enter 10–25", ft.Icons.MENU_BOOK)
    labs = field("Subjects with laboratory", "Enter 1–5", ft.Icons.SCIENCE)
    hands = field("Hands-on subjects", "Enter 1–5", ft.Icons.COMPUTER)
    status = ft.Text(size=13)
    result_area = ft.Column(spacing=12, visible=False)

    def row(label, amount, bold=False):
        return ft.Row([
            ft.Text(label, expand=True, size=14, color=INK,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL),
            ft.Text(peso(amount), size=14, color=INK,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
           vertical_alignment=ft.CrossAxisAlignment.START)

    def calculate(e):
        status.value = ""
        status.color = "#C62828"
        result_area.visible = False
        try:
            u = int(units.value.strip())
            l = int(labs.value.strip())
            h = int(hands.value.strip())
        except (ValueError, AttributeError):
            status.value = "Please enter whole numbers in all fields."
            page.update()
            return

        if not 1 <= u <= 25:
            status.value = "Units must be between 1 and 25."
        elif u < 10:
            status.value = "Error: You must enroll in at least 10 units."
        elif not 1 <= l <= 5:
            status.value = "Laboratory subjects must be from 1 to 5."
        elif not 1 <= h <= 5:
            status.value = "Hands-on subjects must be from 1 to 5."
        elif l > u or h > u:
            status.value = "LAB or hands-on subjects cannot exceed total units."
        else:
            tuition = u * TUITION_RATE
            lab_fee = l * LAB_FEE_PER_SUBJECT
            hands_fee = h * HANDS_ON_FEE_PER_SUBJECT
            total = tuition + lab_fee + hands_fee
            down = min(MIN_DOWN_PAYMENT, total)
            balance = total - down
            assessment = [
                row("Tuition fee", tuition),
                row(f"Laboratory fee · {l} subject(s)", lab_fee),
                row(f"Hands-on fee · {h} subject(s)", hands_fee),
                ft.Divider(color=BORDER, height=18),
                row("TOTAL ASSESSMENT", total, True),
            ]
            breakdown = [
                row("Down payment", down, True),
                row("Remaining balance", balance),
                ft.Divider(color=BORDER, height=18),
            ]
            breakdown.extend(row(f"{name} · {pct:.0%}", balance * pct)
                             for name, pct in EXAM_PAYMENTS)
            result_area.controls = [
                ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.RECEIPT_LONG, color=ORANGE, size=22),
                        ft.Text("Assessment", size=19, weight=ft.FontWeight.BOLD, color=INK)], spacing=8),
                    *assessment,
                ], spacing=12), bgcolor="#FFFFFF", border=ft.border.all(1, BORDER),
                    border_radius=16, padding=18),
                ft.Container(content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, color=ORANGE, size=22),
                        ft.Text("Payment Breakdown", size=19, weight=ft.FontWeight.BOLD, color=INK)], spacing=8),
                    *breakdown,
                ], spacing=12), bgcolor="#FFFFFF", border=ft.border.all(1, BORDER),
                    border_radius=16, padding=18),
                ft.Text("Only the tuition, laboratory, and hands-on fees specified in the project are included.",
                    size=11, color=MUTED, italic=True),
            ]
            result_area.visible = True
            status.value = "Assessment calculated successfully."
            status.color = "#27834A"
        page.update()

    def clear(e):
        units.value = labs.value = hands.value = ""
        status.value = ""
        result_area.visible = False
        page.update()

    def go(name):
        if name != nav["current"]:
            nav["previous"] = nav["current"]
            nav["current"] = name
        render()

    def go_back(e=None):
        target = nav["previous"] if nav["previous"] != nav["current"] else "home"
        nav["current"], nav["previous"] = target, "home"
        render()

    def menu_button():
        return ft.PopupMenuButton(
            icon=ft.Icons.MENU, icon_color="#FFFFFF", icon_size=28,
            tooltip="Menu",
            items=[
                ft.PopupMenuItem(text="About App", icon=ft.Icons.INFO_OUTLINE,
                                 on_click=lambda e: go("about")),
                ft.PopupMenuItem(text="How to Use", icon=ft.Icons.HELP_OUTLINE,
                                 on_click=lambda e: go("howto")),
                ft.PopupMenuItem(text="Programmers Profile", icon=ft.Icons.PEOPLE_OUTLINE,
                                 on_click=lambda e: go("profile")),
            ])

    def logo_image(size):
        return ft.Image(src=LOGO, width=size, height=size,
                        fit=IMG_CONTAIN,
                        error_content=ft.Icon(ft.Icons.SCHOOL, color="#FFFFFF", size=size * 0.6))

    def header(title, subtitle, with_menu=False, logo_size=104):
        top_row = ft.Row([menu_button()] if with_menu else [],
                         alignment=ft.MainAxisAlignment.START)
        return ft.Container(content=ft.Column([
            top_row,
            logo_image(logo_size),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD,
                    color="#FFFFFF", text_align=ft.TextAlign.CENTER),
            ft.Text(subtitle, size=11, weight=ft.FontWeight.W_500,
                    color="#FFF5EC", text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=ORANGE, padding=ft.padding.only(left=12, right=12, top=10, bottom=24),
            border_radius=ft.border_radius.only(bottom_left=24, bottom_right=24))

    def card(icon, title, body_controls):
        return ft.Container(content=ft.Column([
            ft.Row([ft.Icon(icon, color=ORANGE, size=22),
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=INK)], spacing=8),
            *body_controls,
        ], spacing=10), bgcolor="#FFFFFF", border=ft.border.all(1, BORDER),
            border_radius=16, padding=18)

    def exit_button():
        return ft.ElevatedButton("Exit", icon=ft.Icons.ARROW_BACK, on_click=go_back,
            bgcolor=ORANGE, color="#FFFFFF", expand=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=16))

    def sub_screen(title, cards):
        return ft.Column([
            header(title, "BAGUIO COLLEGE OF TECHNOLOGY", logo_size=80),
            ft.Container(content=ft.Column([*cards, ft.Row([exit_button()])], spacing=14),
                         padding=ft.padding.only(left=16, right=16, top=18, bottom=24)),
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def home_view():
        form_card = ft.Container(content=ft.Column([
            ft.Text("Enrollment Details", size=19, weight=ft.FontWeight.BOLD, color=INK),
            ft.Text("Fill in your current enrollment information.", size=12, color=MUTED),
            units, labs, hands,
            ft.Row([
                ft.ElevatedButton("Calculate", icon=ft.Icons.CALCULATE, on_click=calculate,
                    bgcolor=ORANGE, color="#FFFFFF", expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=16)),
                ft.OutlinedButton("Clear", on_click=clear,
                    style=ft.ButtonStyle(color=ORANGE, side=ft.BorderSide(1, ORANGE),
                        shape=ft.RoundedRectangleBorder(radius=12), padding=16)),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            status,
        ], spacing=14), bgcolor=PALE_ORANGE, border_radius=16, padding=18,
            margin=ft.margin.only(left=16, right=16, top=18, bottom=16))

        return ft.Column([
            header("TUITION FEE CALCULATOR", "BAGUIO COLLEGE OF TECHNOLOGY", with_menu=True),
            form_card,
            ft.Container(content=result_area, padding=ft.padding.only(left=16, right=16, bottom=24)),
            ft.Container(content=ft.Text("BCT • Student Assessment", size=11, color=MUTED),
                alignment=ft.alignment.center, padding=ft.padding.only(bottom=16)),
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def about_view():
        return sub_screen("ABOUT APP", [
            card(ft.Icons.INFO_OUTLINE, "BCT Tuition Fee Calculator", [
                ft.Text("This app helps Baguio College of Technology students "
                        "estimate their tuition assessment for the semester based on "
                        "the number of units, laboratory subjects, and hands-on subjects "
                        "they are enrolled in.", size=14, color=INK),
                ft.Text("It also shows the down payment, the remaining balance, "
                        "and how the balance is divided across the exam periods "
                        "(1st Prelim, 1st Grading, 2nd Prelim, Midterm, Finals).",
                        size=14, color=INK),
            ]),
            card(ft.Icons.CALENDAR_MONTH, "App Details", [
                ft.Text("Created: October 2026", size=14, color=INK),
                ft.Text("Version: 1.0", size=14, color=INK),
            ]),
        ])

    def howto_view():
        steps = [
            "Enter your total units enrolled (10 to 25).",
            "Enter how many of your subjects have a laboratory (1 to 5).",
            "Enter how many of your subjects are hands-on (1 to 5).",
            "Tap Calculate to see your assessment and payment breakdown.",
            "Tap Clear to erase everything and start over.",
        ]
        step_rows = [
            ft.Row([
                ft.Container(content=ft.Text(str(i), color="#FFFFFF", size=12,
                                             weight=ft.FontWeight.BOLD),
                             bgcolor=ORANGE, width=24, height=24, border_radius=12,
                             alignment=ft.alignment.center),
                ft.Text(s, size=14, color=INK, expand=True),
            ], vertical_alignment=ft.CrossAxisAlignment.START, spacing=10)
            for i, s in enumerate(steps, start=1)
        ]
        return sub_screen("HOW TO USE", [
            card(ft.Icons.HELP_OUTLINE, "Step by step", step_rows),
            card(ft.Icons.LIGHTBULB_OUTLINE, "Good to know", [
                ft.Text("• You must enroll in at least 10 units.", size=14, color=INK),
                ft.Text("• Laboratory and hands-on subjects cannot be more than your total units.",
                        size=14, color=INK),
                ft.Text("• The minimum down payment is ₱3,500.00.", size=14, color=INK),
            ]),
        ])

    def profile_card(p):
        info = [ft.Text(p["name"], size=16, weight=ft.FontWeight.BOLD, color=INK),
                ft.Text(p["course"], size=13, color=INK),
                ft.Text(p["school"], size=13, color=MUTED)]
        if p["birthday"]:
            info.append(ft.Text(f"Birthday: {p['birthday']}", size=13, color=MUTED))
        photo = ft.Container(
            content=ft.Image(src=p["photo"], width=88, height=88,
                             fit=IMG_COVER,
                             error_content=ft.Icon(ft.Icons.PERSON, size=48, color=ORANGE)),
            width=88, height=88, border_radius=44, bgcolor=PALE_ORANGE,
            border=ft.border.all(2, ORANGE), clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            alignment=ft.alignment.center)
        return ft.Container(content=ft.Row([
            photo, ft.Column(info, spacing=3, expand=True),
        ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#FFFFFF", border=ft.border.all(1, BORDER), border_radius=16, padding=16)

    def profile_view():
        return sub_screen("PROGRAMMERS PROFILE",
                          [profile_card(p) for p in PROGRAMMERS] + [
            ft.Text("App created October 2026", size=11, color=MUTED, italic=True,
                    text_align=ft.TextAlign.CENTER),
        ])

    home = home_view()

    def render():
        page.controls.clear()
        views = {"home": lambda: home, "about": about_view,
                 "howto": howto_view, "profile": profile_view}
        page.add(views[nav["current"]]())
        page.scroll_to(offset=0)
        page.update()

    render()


if __name__ == "__main__":
    ft.app(target=main, assets_dir=BASE_DIR)
