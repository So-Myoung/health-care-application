from pyexpat.errors import messages

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import *
from .models import *


def home(request):
    return render(request, 'base1.html')


def board(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        board = Board(
            title=title,
            content=content,
            user=user,
        )
        board.save()

        return redirect('board')
    else:
        boardForm = BoardForm
        board = Board.objects.all()
        context = {
            'boardForm': boardForm,
            'board': board,
        }
        return render(request, 'board.html', context)


def boardEdit(request, pk):
    board = Board.objects.get(id=pk)

    if request.user != board.user:
        messages.warning(request, '권한 없음')
        return redirect('board')
    if request.method == "POST":
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.user = request.user
        board.save()
        return redirect('board')

    else:
        boardForm = BoardForm
        return render(request, 'update.html', {'boardForm': boardForm})


def boardDelete(request, pk):

    board = Board.objects.get(id=pk)

    if request.user != board.user:
        messages.warning(request, '권한 없음')
        return redirect('board')
    elif request.method == "POST":
        board.delete()
        return redirect('board')

    else:
        boardForm = BoardForm
        return render(request, 'delete.html',{'boardForm': boardForm})
