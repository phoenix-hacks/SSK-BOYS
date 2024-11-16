import streamlit as st


st.set_page_config(page_title="Maternal Nutritional Planner", page_icon="🍎", layout="wide")


st.markdown("""
    <style>
    .header {
        font-size: 40px;
        font-weight: bold;
        color: 
        text-align: center;
        margin-top: 50px;
    }
    .subheader {
        font-size: 30px;
        font-weight: bold;
        color: 
    }
    .section {
        margin-bottom: 40px;
    }
    .meal-container {
        background-color: 
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .meal-title {
        font-size: 20px;
        font-weight: bold;
        color: 
    }
    .meal-info {
        font-size: 16px;
        color: 
    }
    .comparison {
        background-color: 
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        color: 
    }
    </style>
""", unsafe_allow_html=True)


if 'bmr' not in st.session_state:
    st.session_state.bmr = 0
if 'tdee' not in st.session_state:
    st.session_state.tdee = 0
if 'total_calories' not in st.session_state:
    st.session_state.total_calories = 0


st.markdown('<div class="header">Maternal Nutritional Planner</div>', unsafe_allow_html=True)


age = st.number_input("Enter Age (years)", min_value=18, max_value=100, value=25, step=1)
height = st.number_input("Enter Height (cm)", min_value=140, max_value=200, value=160, step=1)
weight = st.number_input("Enter Weight (kg)", min_value=40, max_value=150, value=60, step=1)
activity_level = st.selectbox(
    "Select Activity Level", 
    ["Sedentary (little or no exercise)", "Lightly active", "Moderately active", "Very active", "Super active"]
)


def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age - 161


activity_multiplier = {
    "Sedentary (little or no exercise)": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725,
    "Super active": 1.9
}


if st.session_state.bmr == 0:
    
    st.session_state.bmr = calculate_bmr(weight, height, age)
    st.session_state.tdee = st.session_state.bmr * activity_multiplier[activity_level]


st.markdown(f'<div class="subheader">BMR and TDEE Information</div>', unsafe_allow_html=True)
st.write(f"Your Basal Metabolic Rate (BMR) is: **{st.session_state.bmr:.2f} kcal/day**")
st.write(f"Your Total Daily Energy Expenditure (TDEE) is: **{st.session_state.tdee:.2f} kcal/day**")


meal_data = [
    {"Meal": "Oatmeal with fruits", "Calories": 300, "Protein": 10, "Carbs": 50, "Fats": 10},
    {"Meal": "Grilled chicken salad", "Calories": 450, "Protein": 40, "Carbs": 20, "Fats": 25},
    {"Meal": "Salmon with steamed vegetables", "Calories": 500, "Protein": 35, "Carbs": 30, "Fats": 30}
]


if st.session_state.total_calories == 0:
    st.session_state.total_calories = sum(meal["Calories"] for meal in meal_data)


st.markdown(f'<div class="subheader">Meal Plan and Nutritional Breakdown</div>', unsafe_allow_html=True)
for meal in meal_data:
    st.markdown(f'<div class="meal-container">'
                f'<div class="meal-title">{meal["Meal"]}</div>'
                f'<div class="meal-info">Calories: {meal["Calories"]} kcal | Protein: {meal["Protein"]}g | Carbs: {meal["Carbs"]}g | Fats: {meal["Fats"]}g</div>'
                f'</div>', unsafe_allow_html=True)

st.write(f"**Total Calories from Meals**: {st.session_state.total_calories} kcal")


st.markdown(f'<div class="comparison">'
            f'<b>TDEE vs Total Calories from Meals</b><br>'
            f'TDEE: {st.session_state.tdee} kcal<br>'
            f'Total Calories from Meals: {st.session_state.total_calories} kcal'
            f'</div>', unsafe_allow_html=True)
