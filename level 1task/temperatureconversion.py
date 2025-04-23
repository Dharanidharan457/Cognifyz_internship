def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9
def temperature_converter():

    print("Temperature Conversion Program")
    try:
        temp = float(input("Enter the temperature value: "))
        unit = input("Enter the unit (C for Celsius, F for Fahrenheit): ").upper()
        
        if unit == 'C':
            converted = celsius_to_fahrenheit(temp)
            print(f"{temp}°C is equal to {converted:.2f}°F")
        elif unit == 'F':
            converted = fahrenheit_to_celsius(temp)
            print(f"{temp}°F is equal to {converted:.2f}°C")
        else:
            print("Invalid unit. Please enter 'C' or 'F'.")
    except ValueError:
        print("Please enter a valid number for temperature.")

if __name__ == "__main__":
    temperature_converter()
    
   #output
     #Temperature Conversion Program
     #Enter the temperature value: 100
     #Enter the unit (C for Celsius, F for Fahrenheit): F
     #100.0°F is equal to 37.78°C)