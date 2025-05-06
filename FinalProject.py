from abc import ABC, abstractmethod

# Abstract basee class
class AthleteProfile(ABC):
    def __init__(self, name, age, height_cm, weight_kg):
        self.name = name
        self.age = age
        self.height_cm = height_cm
        self.weight_kg = weight_kg

    @abstractmethod
    def calculate_performance_score(self):
        pass

# Supporting Classses
class Nutrition:
    def __init__(self, calories, protein_g, carbs_g, fats_g):
        self.calories = calories
        self.protein_g = protein_g
        self.carbs_g = carbs_g
        self.fats_g = fats_g

class Sleep:
    def __init__(self, avg_hours):
        self.avg_hours = avg_hours

class MentalState:
    def __init__(self, focus_level, injury_status):
        self.focus_level = focus_level
        self.injury_status = injury_status

class CourseConditions:
    def __init__(self, difficulty, temperature_c, humidity_percent, altitude_m, wind_speed_kph, surface_type):
        self.difficulty = difficulty
        self.temperature_c = temperature_c
        self.humidity_percent = humidity_percent
        self.altitude_m = altitude_m
        self.wind_speed_kph = wind_speed_kph
        self.surface_type = surface_type.lower()

# Athlete Class
class D3Athlete(AthleteProfile):
    def __init__(self, name, age, height_cm, weight_kg, nutrition, sleep, training_load, mental_state, pr_8k_seconds):
        super().__init__(name, age, height_cm, weight_kg)
        self.nutrition = nutrition
        self.sleep = sleep
        self.training_load = training_load
        self.mental_state = mental_state
        self.pr_8k_seconds = pr_8k_seconds

    def calculate_bmi(self):
        return self.weight_kg / ((self.height_cm / 100) ** 2)

    def calculate_performance_score(self):
        bmi = self.calculate_bmi()
        score = 100
        score += (self.sleep.avg_hours - 7) * 3
        score += (self.training_load - 5) * 4
        score += (self.nutrition.protein_g - 100) * 0.2
        score += (self.mental_state.focus_level - 5) * 2
        if self.mental_state.injury_status:
            score -= 15
        score -= abs(21.5 - bmi) * 2
        return max(0, min(score, 150))

class RaceSimulator:
    def __init__(self, athlete, course_conditions):
        self.athlete = athlete
        self.course_conditions = course_conditions

    def predict_8k_time(self):
        score = self.athlete.calculate_performance_score()
        base_time = self.athlete.pr_8k_seconds if self.athlete.pr_8k_seconds else 32 * 60

        score_adjustment = (100 - score) * 2
        difficulty_penalty = (self.course_conditions.difficulty - 5) * 10
        temp_penalty = max(0, self.course_conditions.temperature_c - 18) * 1.5
        humidity_penalty = max(0, self.course_conditions.humidity_percent - 50) * 0.5
        altitude_penalty = self.course_conditions.altitude_m * 0.01
        wind_penalty = self.course_conditions.wind_speed_kph * 1.2

        surface_penalty = 0
        if self.course_conditions.surface_type == 'grass':
            surface_penalty = 15
        elif self.course_conditions.surface_type == 'dirt':
            surface_penalty = 8

        total_adjustment = sum([
            score_adjustment,
            difficulty_penalty,
            temp_penalty,
            humidity_penalty,
            altitude_penalty,
            wind_penalty,
            surface_penalty
        ])

        predicted_time = base_time + total_adjustment

        # Limit range: can't exceed 4 mins slower or go more than 2 mins faster than PR
        predicted_time = max(base_time - 120, min(predicted_time, base_time + 240))

        minutes = int(predicted_time // 60)
        seconds = int(predicted_time % 60)
        return f"{minutes}:{seconds:02d}"

# Unit conversions
def inches_to_cm(inches): return inches * 2.54
def pounds_to_kg(pounds): return pounds * 0.453592
def fahrenheit_to_celsius(f): return (f - 32) * 5 / 9
def feet_to_meters(feet): return feet * 0.3048
def mph_to_kph(mph): return mph * 1.60934

# User Input
def get_user_input():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    height_in = float(input("Enter your height (in inches): "))
    weight_lb = float(input("Enter your weight (in pounds): "))
    sleep_hours = float(input("Enter your average sleep per night (hours): "))
    training_load = int(input("Enter your training load (1-10): "))

    pr_minutes = int(input("Enter your 8k PR - minutes: "))
    pr_seconds = int(input("Enter your 8k PR - seconds: "))
    pr_8k_seconds = pr_minutes * 60 + pr_seconds

    calories = int(input("Enter your daily calorie intake: "))
    protein = int(input("Enter your daily protein intake (grams): "))
    carbs = int(input("Enter your daily carbs intake (grams): "))
    fats = int(input("Enter your daily fats intake (grams): "))

    focus_level = int(input("Enter your mental focus level (1-10): "))
    injury = input("Are you currently injured? (yes/no): ").strip().lower() == "yes"

    difficulty = int(input("Enter the course difficulty (1-10): "))
    temperature_f = float(input("Enter the race temperature (°F): "))
    humidity_percent = int(input("Enter the humidity percentage: "))
    altitude_ft = float(input("Enter the course altitude (feet): "))
    wind_speed_mph = float(input("Enter the wind speed (mph, headwind positive, tailwind negative): "))
    surface_type = input("Enter the surface type (grass/dirt/road): ")

    # Convert units
    height_cm = inches_to_cm(height_in)
    weight_kg = pounds_to_kg(weight_lb)
    temperature_c = fahrenheit_to_celsius(temperature_f)
    altitude_m = feet_to_meters(altitude_ft)
    wind_speed_kph = mph_to_kph(wind_speed_mph)

    nutrition = Nutrition(calories, protein, carbs, fats)
    sleep = Sleep(sleep_hours)
    mental_state = MentalState(focus_level, injury)
    course_conditions = CourseConditions(difficulty, temperature_c, humidity_percent, altitude_m, wind_speed_kph, surface_type)
    athlete = D3Athlete(name, age, height_cm, weight_kg, nutrition, sleep, training_load, mental_state, pr_8k_seconds)

    return athlete, course_conditions

# Run it
if __name__ == "__main__":
    athlete, course_conditions = get_user_input()
    simulator = RaceSimulator(athlete, course_conditions)
    print(f"\nPredicted 8k time for {athlete.name}: {simulator.predict_8k_time()}")

def simulate_multiple_athletes():
    results = []
    num_athletes = int(input("How many athletes do you want to simulate? "))

    for i in range(num_athletes):
        print(f"\n--- Athlete {i + 1} ---")
        athlete, course_conditions = get_user_input()
        simulator = RaceSimulator(athlete, course_conditions)
        predicted_time = simulator.predict_8k_time()
        results.append((athlete.name, predicted_time))

    # Sort leaderboard by predicted time
    sorted_results = sorted(results, key=lambda x: int(x[1].split(":")[0]) * 60 + int(x[1].split(":")[1]))
    
    print("\n Leaderboard:")
    for place, (name, time) in enumerate(sorted_results, 1):
        print(f"{place}. {name} – {time}")

# Run leaderboard or single
if __name__ == "__main__":
    mode = input("Simulate single athlete or leaderboard? (single/leaderboard): ").strip().lower()
    if mode == "leaderboard":
        simulate_multiple_athletes()
    else:
        athlete, course_conditions = get_user_input()
        simulator = RaceSimulator(athlete, course_conditions)
        print(f"\nPredicted 8k time for {athlete.name}: {simulator.predict_8k_time()}")
cd /path/to/your/project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/d3-athlete-simulator.git
git branch -M main
git push -u origin main


