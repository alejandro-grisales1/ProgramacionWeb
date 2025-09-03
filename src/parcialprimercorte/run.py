from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  

# Estructura para eventos
events = [
    {
        'id': 1,
        'title': 'Conferencia de Python',
        'slug': 'conferencia-python',
        'description': 'Descripción del evento...',
        'date': '2025-09-15',
        'time': '14:00',
        'location': 'Auditorio Principal',
        'category': 'Tecnología',
        'max_attendees': 50,
        'attendees': [
            {'name': 'Juan Pérez', 'email': 'juan@example.com'}
        ],
        'featured': True
    }
]
 
# Categorías de eventos
categories = ['Tecnología', 'Académico', 'Cultural', 'Deportivo', 'Social']

@app.route("/")
def index():
    return render_template("index.html", events=events)

@app.route("/event/<slug>")
def event_detail(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if event:
        return render_template("event_detail.html", event=event)
    return "Evento no encontrado", 404

@app.route("/admin/event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        events.append({
            "id": len(events) + 1,
            "title": title,
            "slug": title.lower().replace(" ", "-"),
            "description": description,
            "date": request.form["date"],
            "time": request.form["time"],
            "location": request.form["location"],
            "category": request.form["category"],
            "max_attendees": int(request.form["max_attendees"]),
            "attendees": [],
            "featured": True
        })
        return redirect("/") 
    return render_template("add.html", categories=categories)

#formulario para registrar evento
@app.route("/event/<slug>/register/", methods=["GET", "POST"])
def register_event(slug):
    event = next((e for e in events if e['slug'] == slug), None)
    if request.method == "POST":
        if event:
            name = request.form["name"]
            email = request.form["email"]
            event['attendees'].append({'name': name, 'email': email})
            return redirect(f"/event/{slug}")
    return render_template("register.html", event=event)