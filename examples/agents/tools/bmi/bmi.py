from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field


class BMIInput(BaseModel):
    height: float = Field(description="Height in centimeters (cm). e.g. 170.0")
    weight: float = Field(description="Weight in kilograms (kg). e.g. 70.0")


def calculate_bmi(
    arg: BMIInput, bot: BotModel | None, model: type_model_name | None
) -> dict:
    height = arg.height
    weight = arg.weight
    if height <= 0 or weight <= 0:
        return "Error: Height and weight must be positive numbers."

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

    # You can select the return type you prefer.
    # - str: Plain text.
    # - dict: Treated as a JSON object, and rendered as a JSON object in the frontend.
    #   The following fields are treated specially:
    #   - source_id: If 'Retrieved Context Citation' is enabled, used as the ID of the source.
    #   - source_name: If 'Retrieved Context Citation' is enabled, used as the name of the source.
    #   - source_link: If 'Retrieved Context Citation' is enabled, used as the reference link of the source.
    #   - content: If present, given to the LLM as the content of the tool result.
    # - app.repositories.models.conversation.ToolResultModel: Union of the following types.
    #   Given to the LLM as-is.
    #   - TextToolResultModel: Plain text.
    #   - JsonToolResultModel: JSON object.
    #   - ImageToolResultModel: Image file.
    #   - DocumentToolResultModel: Document file.
    # - list: List of the above types.
    return {
        "bmi": bmi_rounded,
        "category": category,
    }
    # return f"Your BMI is {bmi_rounded}, which falls within the {category} range."


bmi_tool = AgentTool(
    name="calculate_bmi",
    description="Calculate the Body Mass Index (BMI) from height and weight",
    args_schema=BMIInput,
    function=calculate_bmi,
)
