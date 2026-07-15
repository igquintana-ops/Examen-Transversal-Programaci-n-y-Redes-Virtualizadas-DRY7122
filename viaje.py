import requests
import urllib.parse

API_KEY = "0348db0d-3853-42e0-845e-e0bcc373d832"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"


def geocodificar(ciudad):
    """Obtiene lat/lng de una ciudad usando la API de geocoding."""
    url = GEOCODE_URL + urllib.parse.urlencode(
        {"q": ciudad, "limit": "1", "key": API_KEY}
    )
    respuesta = requests.get(url)
    datos = respuesta.json()

    if respuesta.status_code == 200 and datos.get("hits"):
        punto = datos["hits"][0]["point"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        print(f"  -> Ubicacion encontrada: {nombre}, {pais}")
        return punto["lat"], punto["lng"]
    else:
        print(f"  -> No se encontro la ciudad: {ciudad}")
        return None, None


def calcular_ruta(origen, destino, vehiculo):
    """Calcula la ruta entre dos puntos y muestra los resultados."""
    lat_o, lng_o = geocodificar(origen)
    lat_d, lng_d = geocodificar(destino)

    if lat_o is None or lat_d is None:
        return

    parametros = {
        "key": API_KEY,
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "points_encoded": "false",
    }
    url = (
        ROUTE_URL
        + urllib.parse.urlencode(parametros)
        + f"&point={lat_o},{lng_o}&point={lat_d},{lng_d}"
    )
    respuesta = requests.get(url)
    datos = respuesta.json()

    if respuesta.status_code != 200:
        print("Error al calcular la ruta:", datos.get("message", respuesta.status_code))
        return

    ruta = datos["paths"][0]
    distancia_km = ruta["distance"] / 1000
    distancia_millas = distancia_km / 1.60934
    duracion_ms = ruta["time"]

    horas = int(duracion_ms / 1000 / 60 / 60)
    minutos = int(duracion_ms / 1000 / 60 % 60)
    segundos = int(duracion_ms / 1000 % 60)

    print("\n===== RESULTADOS DEL VIAJE =====")
    print(f"Origen:              {origen}")
    print(f"Destino:             {destino}")
    print(f"Medio de transporte: {vehiculo}")
    print(f"Distancia:           {distancia_km:.1f} km / {distancia_millas:.1f} millas")
    print(f"Duracion del viaje:  {horas:02d}:{minutos:02d}:{segundos:02d} (hh:mm:ss)")

    print("\n===== NARRATIVA DEL VIAJE =====")
    for paso in ruta["instructions"]:
        print(f" - {paso['text']} ({paso['distance']/1000:.1f} km)")
    print("=" * 40)


def main():
    print("=" * 55)
    print(" CALCULO DE DISTANCIA ENTRE CIUDAD DE CHILE Y ARGENTINA")
    print(" API Graphhopper - Examen Transversal DRY7122")
    print("=" * 55)

    vehiculos = {"1": "car", "2": "bike", "3": "foot"}

    while True:
        origen = input("\nCiudad de Origen (o 's' para salir): ")
        if origen.lower() == "s":
            print("Saliendo del programa...")
            break

        destino = input("Ciudad de Destino (o 's' para salir): ")
        if destino.lower() == "s":
            print("Saliendo del programa...")
            break

        print("Medio de transporte: 1) Auto  2) Bicicleta  3) A pie")
        opcion = input("Seleccione una opcion (o 's' para salir): ")
        if opcion.lower() == "s":
            print("Saliendo del programa...")
            break

        vehiculo = vehiculos.get(opcion, "car")
        calcular_ruta(origen, destino, vehiculo)


if __name__ == "__main__":
    main()