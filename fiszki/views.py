from django.shortcuts import render, redirect
from .models import FlashcardSet
from django.contrib.auth.decorators import login_required

@login_required
def add_set(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
            FlashcardSet.objects.create(owner=request.user, title=title, description=description)
            return redirect('home')
    return render(request, "fiszki/add_set.html")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FlashcardSet

@login_required
def home(request):
    sets = FlashcardSet.objects.filter(owner=request.user)
    return render(request, 'fiszki/home.html', {'sets': sets})

from .models import FlashcardSet, Flashcard

@login_required
def add_flashcard(request, set_id):
    flashcard_set = FlashcardSet.objects.get(id=set_id, owner=request.user)
    if request.method == 'POST':
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        if question and answer:
            Flashcard.objects.create(
                set=flashcard_set,
                question=question,
                answer=answer
            )
            return redirect('view_set', set_id=flashcard_set.id)
    return render(request, 'fiszki/add_flashcard.html', {'set': flashcard_set})

@login_required
def view_set(request, set_id):
    flashcard_set = FlashcardSet.objects.get(id=set_id, owner=request.user)
    flashcards = flashcard_set.flashcards.all()
    return render(request, 'fiszki/view_set.html', {'set': flashcard_set, 'flashcards': flashcards})


from django.utils import timezone


from django.utils import timezone

@login_required
def review_flashcards(request, set_id):
    flashcard_set = FlashcardSet.objects.get(id=set_id, owner=request.user)
    # Pobieramy wszystkie fiszki, opanowane i nieopanowane, sortujemy od „najmniej opanowanych”
    all_flashcards = list(flashcard_set.flashcards.all())
    # sortujemy: najpierw te z lowest interval (najmniej opanowane)
    all_flashcards.sort(key=lambda x: (x.interval, x.next_review))
    # Chcesz, możesz dodać losowanie/przemieszanie opanowanych

    # Indeks przerabianej fiszki trzymamy w sesji
    idx = int(request.GET.get('idx', '0'))
    session_length = len(all_flashcards)
    if session_length == 0:
        return render(request, 'fiszki/review_done.html', {'set': flashcard_set, 'mastered': [], 'to_review': [], 'all_cards': []})

    if idx < session_length:
        card = all_flashcards[idx]
        show_answer = request.GET.get('show', '') == '1'
        if request.method == 'POST':
            quality = int(request.POST.get('quality', 5))
            card.schedule_next_review(quality)
            return redirect(f'{request.path}?idx={idx+1}')
        return render(request, 'fiszki/review_flashcards.html', {
            'card': card, 'set': flashcard_set, 'show_answer': show_answer, 'idx': idx, 'total': session_length
        })
    else:
        # Raport na koniec przebiegu przez wszystkie fiszki
        mastered = [c for c in all_flashcards if c.interval >= 14]
        to_review = [c for c in all_flashcards if c.interval < 14]
        return render(request, 'fiszki/review_done.html', {
            'set': flashcard_set,
            'mastered': mastered,
            'to_review': to_review,
            'all_cards': all_flashcards,
        })
