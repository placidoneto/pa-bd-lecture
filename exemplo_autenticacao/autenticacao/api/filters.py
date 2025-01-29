import django_filters
from .models import *

class DisciplinaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')  # Busca parcial (case-insensitive)
    carga_horaria_min = django_filters.NumberFilter(field_name='carga_horaria', lookup_expr='gte')

    class Meta:
        model = Disciplina
        fields = ['nome', 'carga_horaria']  # Campos para filtragem exata

class AlunoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')  # Busca parcial (case-insensitive)

