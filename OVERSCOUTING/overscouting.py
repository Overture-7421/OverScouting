import csv
import os

filename = "data_backup.csv"
data_list = []

print("""
                                          _   _             
                                         | | (_)            
   _____   _____ _ __ ___  ___ ___  _   _| |_ _ _ __   __ _ 
  / _ \ \ / / _ \ '__/ __|/ __/ _ \| | | | __| | '_ \ / _` |
 | (_) \ V /  __/ |  \__ \ (_| (_) | |_| | |_| | | | | (_| |
  \___/ \_/ \___|_|  |___/\___\___/ \__,_|\__|_|_| |_|\__, |
                                                       __/ |
                                                      |___/ 

by FIRST FRC Team Overture - 7421""")

print("\n Bienvenido a OverScouting, la herramienta de compilación de datos por QR para tu equipo de FRC. Agradecemos la aplicación de QRScout de Red Hawk Robotics 2713.\n")

def load_existing_data():
    """Cargando los datos existentes del archivo. Si existe."""
    if os.path.exists(filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data_list.append(row)
        print("Datos cargados exitosamente.")

def add_data():
    while True:
        new_data = input("Introduzca nuevos datos (escriba 'exit' para salir o 'undo' para borrar el último dato introducido.): ")
        if new_data.lower() == 'exit':
            post_entry_options()
            break
        elif new_data.lower() == 'undo':
            if data_list:
                removed_data = data_list.pop()
                remove_last_line()
                print(f"Último dato introducido borrado: {removed_data}")
            else:
                print("No hay datos para borrar.")
        else:
            data_fields = new_data.split('\t')
            data_list.append(data_fields)
            autosave_data(data_fields)
            print("Datos cargados exitosamente.")

def autosave_data(data_fields):
    """Autosave los nuevos datos al archivo."""
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_fields)
    print("Datos autosaved.")

def remove_last_line():
    """Remove the last line from the CSV file."""
    with open(filename, 'r+', newline='') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[:-1])

def post_entry_options():
    print("\n¿Qué te gustaría hacer?:")
    print("1. Crear un CSV con los datos generados")
    print("2. Salir del programa")
    choice = input("Introducir tu decisión (1-2): ")

    if choice == "1":
        create_csv()
    print("Saliendo del programa.")

def create_csv():
    with open("data_final.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for item in data_list:
            writer.writerow(item)
    print("Datos exportados a data_final.csv exitosamente.")

if __name__ == "__main__":
    load_existing_data()
    add_data()
