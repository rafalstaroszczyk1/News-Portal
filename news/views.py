import json
import random
from datetime import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import View

dane = 'Coming soon'

def get_json():
    with open("hypernews/news.json", 'r') as json_file:
        data_json = json.load(json_file)
    return data_json


def update_json(data):
    with open("hypernews/news.json", 'w') as json_file:
        json.dump(data, json_file)


class HomeView(View):
    def get(self, requests, *args, **kwargs):
        return HttpResponse(dane)


class MainView(View):
    def get(self, request, *args, **kwargs):
        news_json = get_json()
        query_string = request.GET.get('q')
        if query_string is not None:
            articles_filtered = list(filter(lambda x: query_string in x['title'], news_json))
            news_json = articles_filtered
        news_json.sort(key=lambda x: x["created"], reverse=True)
        context = {"articles": news_json}
        return render(request, "news/main.html", context=context)


class NewsDetail(View):
    def get(self, request, link, *args, **kwargs):
        news = get_json()
        context = {}
        for n in news:
            if n['link'] == link:
                context = n
                break
        if not context:
            raise Http404
        return render(request, 'news/index.html', context)


class NewsCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html", context={})

    def post(self, request, *args, **kwargs):
        art_title = request.POST.get('title')
        art_text = request.POST.get('text')
        art_link = random.randint(1, 1000)
        art_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_article = {'created': art_created,
                       'text': art_text,
                       'title': art_title,
                       'link': art_link}
        articles_list = get_json()
        articles_list.append(new_article)
        update_json(articles_list)

        return redirect("/news/")


class DeleteView(View):
    def get(self, request, link, *args, **kwargs):
        articles_lista = get_json()
        for i in articles_lista:
            if i['link'] == link:
                articles_lista.remove(i)
        update_json(articles_lista)
        return redirect("/news/")


class UpdateView(View):
    def get(self, request, link, *args, **kwargs):
        news = get_json()
        context = {}
        for n in news:
            if n['link'] == link:
                context = n
                break
        if not context:
            raise Http404
        return render(request, 'news/update.html', context)

    def post(self, request, link, *args, **kwargs):
        updat_title = request.POST.get('title')
        update_text = request.POST.get('text')
        print(update_text, updat_title, link)
        update_post = get_json()
        for n in update_post:
            if n['link'] == link:
                n['title'] = updat_title
                n['text'] = update_text
        update_json(update_post)
        return redirect("/news/")
