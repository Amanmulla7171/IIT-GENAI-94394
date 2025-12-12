from geometry import rectangle, circle, triangle, square
from weather import get_weather_info
from placeholderdata import data_placeholder, save_to_json


def geometry_menu():
    while True:
        print("\n=== GEOMETRY MENU ===")
        print("1. Area of Rectangle")
        print("2. Area of Circle")
        print("3. Area of Triangle")
        print("4. Area of Square")
        print("5. Back to Main Menu")

        choice = input("Choose an option (1–5): ")

        match choice:
            case "1":
                l = float(input("Enter length: "))
                w = float(input("Enter width: "))
                print("Area of Rectangle:", rectangle(l, w))

            case "2":
                r = float(input("Enter radius: "))
                print("Area of Circle:", circle(r))

            case "3":
                b = float(input("Enter base: "))
                h = float(input("Enter height: "))
                print("Area of Triangle:", triangle(b, h))

            case "4":
                s = float(input("Enter side length: "))
                print("Area of Square:", square(s))

            case "5":
                return   # Go back to main menu

            case _:
                print("Invalid choice. Try again.")


def main_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Weather")
        print("2. Geometry")
        print("3. Placeholder Data")
        print("4. Exit")

        choice = input("Choose an option (1–4): ")

        match choice:
            case "1":
                city = input("Enter city name: ")
                weather = get_weather_info(city)
                print("\nWeather Info:", weather)

            case "2":
                geometry_menu()

            case "3":
                file = "placeholder_data.json"
                save_to_json(data_placeholder, file)
                print(f"Placeholder API data saved to {file}")

            case "4":
                print("Exiting the application...")
                break

            case _:
                print("Invalid option. Try again.")


if __name__ == "__main__":
    main_menu()
