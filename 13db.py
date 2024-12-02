import sqlite3
import matplotlib.pyplot as plt

# create and connect to the database
database_name = "population.db"
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# create the population table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS population (
        city TEXT,
        year INTEGER,
        population INTEGER
    )
""")

# insert initial data for 2023 for 10 cities in Florida
cities = [
    ("Miami", 2023, 478251),
    ("Orlando", 2023, 307573),
    ("Tampa", 2023, 399700),
    ("Jacksonville", 2023, 955915),
    ("Tallahassee", 2023, 197102),
    ("St. Petersburg", 2023, 261338),
    ("Fort Lauderdale", 2023, 182437),
    ("Cape Coral", 2023, 204510),
    ("Gainesville", 2023, 143484),
    ("Sarasota", 2023, 57791),
]

cursor.executemany("INSERT INTO population (city, year, population) VALUES (?, ?, ?)", cities)


# function to simulate population growth for the next 20 years
def simulate_population_growth():
    growth_rate = 0.02  # 2% annual growth rate
    cursor.execute("SELECT DISTINCT city, population FROM population WHERE year=2023")
    city_data = cursor.fetchall()
    for city, population in city_data:
        current_population = population
        for year in range(2024, 2044):
            current_population = int(current_population * (1 + growth_rate))
            cursor.execute("INSERT INTO population (city, year, population) VALUES (?, ?, ?)",
                           (city, year, current_population))


# run the simulation
simulate_population_growth()
conn.commit()


# function to display population growth for a selected city
def display_population_growth():
    while True:
        cursor.execute("SELECT DISTINCT city FROM population")
        cities = [row[0] for row in cursor.fetchall()]
        print("\nCities:")
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city}")

        choice = input("Select a city by number (or type 'exit' to quit): ")
        if choice.lower() == "exit":
            break

        try:
            city_index = int(choice) - 1
            if 0 <= city_index < len(cities):
                selected_city = cities[city_index]
                cursor.execute("SELECT year, population FROM population WHERE city = ? ORDER BY year", (selected_city,))
                data = cursor.fetchall()
                years, populations = zip(*data)

                # Plot the population growth
                plt.figure()
                plt.plot(years, populations, marker="o")
                plt.title(f"Population Growth for {selected_city}")
                plt.xlabel("Year")
                plt.ylabel("Population")
                plt.grid(True)
                plt.show()
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'exit'.")


# call the function to display population growth
display_population_growth()

# close the database connection
conn.close()
