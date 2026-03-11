
one_championship_types = [
  'Water', 'Fire', 'Grass', 'Flying', 'Rock',
  'Ground', 'Steel', 'Electric', 'Fairy', 'Ghost',
  'Dark', 'Dragon', 'Ice', 'Bug', 'Fighting', 'Poison',
  'Psychic', 'Normal'
]

from one_championship.models import Type
types = [Type(name=type) for type in one_championship_types]