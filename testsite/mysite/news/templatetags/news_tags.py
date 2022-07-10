from django import template
from django.db.models import *

from news.models import Category

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    # return Category.objects.all()
    # return Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    q = '''select 
                cat.id as id,
                cat.title as title,
                count(*) as cnt		
            from news_category cat
            inner join news_news nw on nw.category_id=cat.id 
            where nw.is_published<>0
            group by cat.id
            order by cat.title
    '''
    return Category.objects.raw(q)


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    categories = get_categories()
    return {'categories': categories}
