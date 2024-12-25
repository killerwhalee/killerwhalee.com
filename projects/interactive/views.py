from django.shortcuts import render, redirect

from uuid import uuid4


def index(request):
    if request.method == "POST":
        room_name: str = request.POST.get("room")

        # Generate random room name if invalid
        if not room_name.isalnum():
            room_name = uuid4().hex[:8]

        return redirect("projects:interactive:room", room_name)

    return render(request, "interactive/index.html")


def room(request, room_name):
    return render(request, "interactive/room.html", {"room_name": room_name})
