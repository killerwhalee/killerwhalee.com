from django.shortcuts import render, redirect


def index(request):
    if request.method == "POST":
        room_name = request.POST.get("room")

        return redirect("projects:interactive:room", room_name)

    from django import urls

    url_resolver = urls.get_resolver(urls.get_urlconf())
    print(url_resolver.namespace_dict.keys())

    return render(request, "interactive/index.html")


def room(request, room_name):
    return render(request, "interactive/room.html", {"room_name": room_name})
