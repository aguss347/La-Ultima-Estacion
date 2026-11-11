from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO


def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")
    if request.method == "POST":
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            messages.success(request, "Tu cuenta fue creada correctamente.")
            return redirect("inicio")
    else:
        formulario = UserCreationForm()
    return render(request, "app1/registro.html", {"formulario": formulario})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("inicio")
    if request.method == "POST":
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            login(request, formulario.get_user())
            return redirect("inicio")
    else:
        formulario = AuthenticationForm(request)
    return render(request, "app1/login.html", {"formulario": formulario})


def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("inicio")


@login_required
def inicio(request):
    return render(request, "app1/index.html")


@login_required
def mecanicas(request):
    return render(request, "app1/mecanicas.html")


@login_required
def pagina(request):
    return render(request, "app1/pagina.html")


@login_required
def contacto(request):
    return render(request, "app1/contacto.html")


@user_passes_test(lambda usuario: usuario.is_superuser)
def descargar_usuarios_pdf(request):
    Usuario = get_user_model()
    usuarios = Usuario.objects.all().order_by("date_joined")
    buffer = BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=35, bottomMargin=35)
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("La Última Estación - Usuarios registrados", estilos["Title"]),
        Spacer(1, 14),
        Paragraph(f"Cantidad de usuarios registrados: {usuarios.count()}", estilos["Normal"]),
        Spacer(1, 12),
    ]
    filas = [["Usuario", "Correo electrónico", "Fecha de registro", "Staff"]]
    for usuario in usuarios:
        filas.append([
            usuario.username,
            usuario.email or "-",
            usuario.date_joined.strftime("%d/%m/%Y %H:%M"),
            "Sí" if usuario.is_staff else "No",
        ])
    tabla = Table(filas, repeatRows=1, colWidths=[115, 180, 120, 55])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#514477")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1eef8")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elementos.append(tabla)
    documento.build(elementos)
    respuesta = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    respuesta["Content-Disposition"] = 'attachment; filename="usuarios_registrados.pdf"'
    return respuesta
