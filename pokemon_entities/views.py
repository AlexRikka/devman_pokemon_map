import folium

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transprevious_evolution'
)


def get_pokemon_image(pokemon, request):
    if not pokemon.image:
        return request.build_absolute_uri(DEFAULT_IMAGE_URL)
    return request.build_absolute_uri(pokemon.image.url)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_datetime = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_pokemon_image(pokemon_entity.pokemon, request)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_pokemon_image(pokemon, request),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_datetime = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime,
        pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_pokemon_image(pokemon_entity.pokemon, request)
        )

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'img_url': get_pokemon_image(requested_pokemon, request),
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }

    previous_evolution_pokemon = requested_pokemon.previous_evolution
    if previous_evolution_pokemon:
        pokemon['previous_evolution'] = {
            'pokemon_id': previous_evolution_pokemon.id,
            'img_url': get_pokemon_image(previous_evolution_pokemon, request),
            'title_ru': previous_evolution_pokemon.title,
        }

    next_evolution_pokemon = requested_pokemon.next_evolutions.first()
    if next_evolution_pokemon:
        pokemon['next_evolution'] = {
            'pokemon_id': next_evolution_pokemon.id,
            'img_url': get_pokemon_image(next_evolution_pokemon, request),
            'title_ru': next_evolution_pokemon.title,
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
