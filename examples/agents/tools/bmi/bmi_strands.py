from strands import tool
from app.repositories.models.custom_bot import BotModel


def create_bmi_tool(bot: BotModel | None = None):
    """Create BMI calculation tool with bot context closure."""

    @tool
    def calculate_bmi(height: float, weight: float) -> dict:
        """
        Calculate the Body Mass Index (BMI) from height and weight.

        Args:
            height: Height in centimeters (cm). e.g. 170.0
            weight: Weight in kilograms (kg). e.g. 70.0

        Returns:
            dict: BMI calculation result in Strands format
        """
        # Access bot context if needed
        if bot:
            print(f"BMI calculation for bot: {bot.id}")

        try:
            if height <= 0 or weight <= 0:
                return {
                    "toolUseId": "placeholder",
                    "status": "error",
                    "content": [{"text": "Error: Height and weight must be positive numbers."}]
                }

            height_in_meters = height / 100
            bmi = weight / (height_in_meters**2)
            bmi_rounded = round(bmi, 1)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"

            result_data = {
                "bmi": bmi_rounded,
                "category": category,
                "height_cm": height,
                "weight_kg": weight
            }

            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"json": result_data}]
            }

        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"BMI calculation error: {str(e)}"}]
            }

    return calculate_bmi
