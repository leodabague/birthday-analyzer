import streamlit as st
from annotated_text import annotated_text
from datetime import date, datetime
import plotly.graph_objects as go

st.set_page_config(page_icon="🎂", page_title="Not Google")

def calculate_age_stats(birth_date):
    today = date.today()
    years = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1

    days_lived = (today - birth_date).days
    months_lived = days_lived // 30
    weeks_lived = days_lived // 7

    next_birthday = birth_date.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_until_next_birthday = (next_birthday - today).days

    return {
        "years": years,
        "months": months_lived,
        "weeks": weeks_lived,
        "days": days_lived,
        "days_until_next_birthday": days_until_next_birthday
    }

def calculate_weekday_occurrences(birth_date, language=False):
    # Dicionário de tradução dos dias da semana
    weekdays_translation = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekdays_pt = [weekdays_translation[day] for day in weekdays]
    
    # Usar os dias em português ou inglês dependendo da linguagem
    display_weekdays = weekdays_pt if language else weekdays
    occurrences = {day: 0 for day in display_weekdays}
    years_map = {day: [] for day in display_weekdays}

    start_year = birth_date.year
    end_year = date.today().year

    for year in range(start_year, end_year + 1):
        current_date = birth_date.replace(year=year)
        weekday_name = current_date.strftime("%A")
        # Traduzir o nome do dia se necessário
        if language:
            weekday_name = weekdays_translation[weekday_name]
        occurrences[weekday_name] += 1
        years_map[weekday_name].append(year)

    return occurrences, years_map

# Personalizar a cor do toggle
st.markdown("""
    <style>
    /* Cor quando o toggle está ativado */
    .stToggle > div[data-baseweb="toggle"] > div {
        background-color: purple !important;
    }
    
    /* Cor quando o toggle está desativado */
    .stToggle > div[data-baseweb="toggle"] {
        background-color: #4a4a4a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.write("🇺🇸  |  🇧🇷")
language = st.toggle("")

# Set text labels based on language
if language:
    title = "Analisador de Aniversário"
    select_birthday_label = "Selecione sua data de nascimento:"
    age_stats_label = "Mais sobre você"
    years_label = "Anos:"
    months_label = "Meses:"
    weeks_label = "Semanas:"
    days_label = "Dias:"
    days_until_next_birthday_label = "Dias até o próximo aniversário:"
    weekday_distribution_label = "Em quais dias você fez mais aniversários?"
    weekday_select_label = "Selecione um dia da semana para ver os anos específicos:"
    years_on_day_label = "Anos em que seu aniversário caiu em um(a)"
else:
    title = "Birthday Analyzer"
    select_birthday_label = "Select your birthday:"
    age_stats_label = "Statistics"
    years_label = "Years:"
    months_label = "Months:"
    weeks_label = "Weeks:"
    days_label = "Days:"
    days_until_next_birthday_label = "Days until next party:"
    weekday_distribution_label = "Weekday Distribution of Your Birthday"
    weekday_select_label = "Select a weekday to see specific years:"
    years_on_day_label = "Years when your birthday falls on a"

st.title(title)

# Birthday input
birth_date_str = st.text_input(select_birthday_label, value="01/01/2000")

try:
    birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
except ValueError:
    st.error("Please enter the date in DD/MM/YYYY format.")
    birth_date = date(2000, 1, 1)

# Calculate age stats
age_stats = calculate_age_stats(birth_date)

st.subheader(age_stats_label)
annotated_text(
    (years_label, "", "purple"),
    f" {age_stats['years']}"
)
annotated_text(
    (months_label, "", "purple"),
    f" {age_stats['months']}"
)
annotated_text(
    (weeks_label, "", "purple"),
    f" {age_stats['weeks']:,}"
)
annotated_text(
    (days_label, "", "purple"),
    f" {age_stats['days']:,}"
)
annotated_text(
    (days_until_next_birthday_label, "", "white", "black"),  # vermelho
    f" {age_stats['days_until_next_birthday']}"
)

# Calculate weekday occurrences with language parameter
occurrences, years_map = calculate_weekday_occurrences(birth_date, language)

# Visualize weekday data
st.subheader(weekday_distribution_label)

# Criar o gráfico com Plotly
fig = go.Figure()

# Adicionar as barras
fig.add_trace(
    go.Bar(
        x=list(occurrences.keys()),
        y=list(occurrences.values()),
        marker_color='purple',  # Mesma cor dos textos anotados
        opacity=0.8,
        hovertemplate="Dia: %{x}<br>Ocorrências: %{y}<extra></extra>"
    )
)

# Customizar o layout
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
    plot_bgcolor='rgba(0,0,0,0)',   # Área do plot transparente
    font_color='white',
    showlegend=False,
    xaxis_title=("Weekday" if not language else "Dia da Semana"),
    yaxis_title=("Occurrences" if not language else "Ocorrências"),
    xaxis=dict(
        gridcolor='#333333',
        showgrid=False
    ),
    yaxis=dict(
        gridcolor='#333333',
        showgrid=True
    ),
    hoverlabel=dict(
        bgcolor="black",
        font_size=16,
        font_family="Arial"
    ),
    margin=dict(t=30)  # Reduz a margem superior
)

# Mostrar o gráfico
st.plotly_chart(fig, use_container_width=True)

# Interactive dropdown for weekday analysis
selected_day = st.selectbox(weekday_select_label, list(years_map.keys()))

st.write(f"{years_on_day_label} {selected_day}:")
st.write(", ".join(map(str, years_map[selected_day])))

# Esconder menu e footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden; }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
