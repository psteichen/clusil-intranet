from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, cl):
  return field.as_widget(attrs={"class" : cl,})

