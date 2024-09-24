from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def _get_topics(user):
    topics = Topic.objects.filter(owner=user).order_by('date_add')
    return topics

def index(request):
    """Домашняя страница Main App"""
    return render(request, 'index.html')
@login_required
def topics(request):
    """Выводит список папок."""
    topics = _get_topics(request.user)
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну папку и все ее заметки."""
    topics = _get_topics(request.user)
    current_topic = Topic.objects.get(id=topic_id)
    if current_topic.owner != request.user:
        raise Http404
    entries = current_topic.entry_set.order_by('-date_add')
    context = {'topics': topics, 'current_topic': current_topic, 'entries': entries}
    return render(request, 'topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему."""
    topics = _get_topics(request.user)
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('main_app:topics')
    context = {'form': form, 'topics': topics}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Добавление новой заметки в конкретную папку"""
    topics = _get_topics(request.user)
    current_topic = Topic.objects.get(id=topic_id)
    entries = current_topic.entry_set.order_by('-date_add')
    if current_topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = current_topic
            new_entry.save()
            return redirect('main_app:topic', topic_id=topic_id)
    context = {'form': form, 'topics': topics, 'entries': entries, 'current_topic': current_topic}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Изменение заметки"""
    current_entry = Entry.objects.get(id=entry_id)
    current_topic = current_entry.topic
    topics = _get_topics(request.user)
    entries = current_topic.entry_set.order_by('-date_add')
    if current_topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=current_entry)
    else:
        form = EntryForm(instance=current_entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_app:topic', topic_id=current_topic.id)
    context = {'current_entry': current_entry, 'current_topic': current_topic, 'form': form, 'topics': topics, 'entries': entries}
    return render(request, 'edit_entry.html', context)

