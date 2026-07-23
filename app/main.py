import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# Allow imports from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.insight_generator import generate_insight
from app.sql_generator import generate_sql
from database.query_database import execute_query


st.set_page_config(
    page_title="Product Analytics Copilot",
    page_icon="📊",
    layout="wide",
)


def choose_chart_type(question, dataframe):
    """
    Choose a chart type based on the question
    and the structure of the query results.
    """

    if len(dataframe.columns) < 2:
        return None

    category_column = dataframe.columns[0]
    value_column = dataframe.columns[1]

    if not pd.api.types.is_numeric_dtype(dataframe[value_column]):
        return None

    question_lower = question.lower()
    category_name = category_column.lower()

    time_keywords = [
        "over time",
        "trend",
        "daily",
        "weekly",
        "monthly",
        "yearly",
        "by day",
        "by week",
        "by month",
        "by year",
    ]

    time_column_keywords = [
        "date",
        "day",
        "week",
        "month",
        "year",
        "time",
    ]

    pie_keywords = [
        "share",
        "distribution",
        "percentage",
        "proportion",
        "breakdown",
        "composition",
    ]

    if (
        any(keyword in question_lower for keyword in time_keywords)
        or any(keyword in category_name for keyword in time_column_keywords)
    ):
        return "line"

    if (
        any(keyword in question_lower for keyword in pie_keywords)
        and len(dataframe) <= 6
    ):
        return "pie"

    return "bar"


def display_chart(dataframe, chart_type):
    """
    Display a chart using the first column as the category
    and the second column as the numeric value.
    """

    category_column = dataframe.columns[0]
    value_column = dataframe.columns[1]

    chart_dataframe = dataframe.copy()

    category_title = category_column.replace("_", " ").title()
    value_title = value_column.replace("_", " ").title()

    if chart_type == "line":
        chart = (
            alt.Chart(chart_dataframe)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    category_column,
                    title=category_title,
                    sort=None,
                ),
                y=alt.Y(
                    value_column,
                    type="quantitative",
                    title=value_title,
                ),
                tooltip=[
                    alt.Tooltip(
                        category_column,
                        title=category_title,
                    ),
                    alt.Tooltip(
                        value_column,
                        title=value_title,
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    elif chart_type == "pie":
        chart = (
            alt.Chart(chart_dataframe)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta(
                    value_column,
                    type="quantitative",
                ),
                color=alt.Color(
                    category_column,
                    type="nominal",
                    title=category_title,
                ),
                tooltip=[
                    alt.Tooltip(
                        category_column,
                        title=category_title,
                    ),
                    alt.Tooltip(
                        value_column,
                        title=value_title,
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

    elif chart_type == "bar":
        chart = (
            alt.Chart(chart_dataframe)
            .mark_bar()
            .encode(
                x=alt.X(
                    category_column,
                    type="nominal",
                    title=category_title,
                    sort="-y",
                ),
                y=alt.Y(
                    value_column,
                    type="quantitative",
                    title=value_title,
                ),
                tooltip=[
                    alt.Tooltip(
                        category_column,
                        title=category_title,
                    ),
                    alt.Tooltip(
                        value_column,
                        title=value_title,
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )


def parse_insight(insight_text):
    """
    Split Gemini's response into summary,
    insight, and recommendation sections.
    """

    sections = {
        "summary": "",
        "insight": "",
        "recommendation": "",
    }

    current_section = None

    for line in insight_text.splitlines():
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        upper_line = cleaned_line.upper()

        if upper_line.startswith("SUMMARY:"):
            current_section = "summary"
            sections[current_section] = cleaned_line.split(
                ":",
                1,
            )[1].strip()

        elif upper_line.startswith("INSIGHT:"):
            current_section = "insight"
            sections[current_section] = cleaned_line.split(
                ":",
                1,
            )[1].strip()

        elif upper_line.startswith("RECOMMENDATION:"):
            current_section = "recommendation"
            sections[current_section] = cleaned_line.split(
                ":",
                1,
            )[1].strip()

        elif current_section:
            sections[current_section] += f" {cleaned_line}"

    return sections


def display_insight_cards(insight_sections):
    """
    Display the AI analysis in three separate cards.
    """

    summary_col, insight_col, recommendation_col = st.columns(3)

    with summary_col:
        with st.container(border=True):
            st.markdown("#### Summary")
            st.write(
                insight_sections["summary"]
                or "No summary was generated."
            )

    with insight_col:
        with st.container(border=True):
            st.markdown("#### Key insight")
            st.write(
                insight_sections["insight"]
                or "No insight was generated."
            )

    with recommendation_col:
        with st.container(border=True):
            st.markdown("#### Recommendation")
            st.write(
                insight_sections["recommendation"]
                or "No recommendation was generated."
            )


st.title("📊 Product Analytics Copilot")

st.write(
    "Ask questions about trial and subscription performance "
    "using natural language."
)

st.divider()

st.subheader("Suggested questions")

suggested_questions = [
    "What is the conversion rate?",
    "Show subscribed users by device",
    "Show the distribution of trial users by country",
    "Show subscriptions over time",
]

col1, col2 = st.columns(2)

with col1:
    suggestion_1 = st.button(
        suggested_questions[0],
        use_container_width=True,
    )

    suggestion_2 = st.button(
        suggested_questions[1],
        use_container_width=True,
    )

with col2:
    suggestion_3 = st.button(
        suggested_questions[2],
        use_container_width=True,
    )

    suggestion_4 = st.button(
        suggested_questions[3],
        use_container_width=True,
    )

st.divider()

question = st.text_input(
    "Ask your data",
    placeholder="Example: Show subscribed users by device",
)

run_analysis = st.button(
    "Run Analysis",
    type="primary",
)

selected_question = question

if suggestion_1:
    selected_question = suggested_questions[0]

elif suggestion_2:
    selected_question = suggested_questions[1]

elif suggestion_3:
    selected_question = suggested_questions[2]

elif suggestion_4:
    selected_question = suggested_questions[3]


suggestion_clicked = any(
    [
        suggestion_1,
        suggestion_2,
        suggestion_3,
        suggestion_4,
    ]
)


if run_analysis or suggestion_clicked:
    if not selected_question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analyzing your data..."):
                sql = generate_sql(selected_question)
                results, column_names = execute_query(sql)

            st.session_state["selected_question"] = selected_question
            st.session_state["generated_sql"] = sql
            st.session_state["results"] = results
            st.session_state["column_names"] = column_names

        except Exception as error:
            st.error(f"Something went wrong: {error}")


if "results" in st.session_state:
    selected_question = st.session_state["selected_question"]
    sql = st.session_state["generated_sql"]
    results = st.session_state["results"]
    column_names = st.session_state["column_names"]

    st.caption(f"Question: {selected_question}")

    if not results:
        st.info("The query returned no results.")

    else:
        dataframe = pd.DataFrame(
            results,
            columns=column_names,
        )

        st.subheader("Result")

        if len(dataframe) == 1 and len(dataframe.columns) == 1:
            value = dataframe.iloc[0, 0]
            metric_name = dataframe.columns[0]

            st.metric(
                label=metric_name.replace("_", " ").title(),
                value=value,
            )

        else:
            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True,
            )

            chart_type = choose_chart_type(
                selected_question,
                dataframe,
            )

            if chart_type:
                st.subheader("Visualization")

                display_chart(
                    dataframe,
                    chart_type,
                )

                st.caption(
                    f"Chart selected automatically: "
                    f"{chart_type.title()} chart"
                )

        st.divider()

        st.subheader("💡 AI Insight")

        if st.button(
            "Generate AI Insight",
            type="secondary",
        ):
            try:
                with st.spinner("Generating business insight..."):
                    insight = generate_insight(
                        selected_question,
                        dataframe,
                    )

                st.session_state["insight"] = insight

            except Exception as insight_error:
                st.warning(str(insight_error))

        if "insight" in st.session_state:
            insight_sections = parse_insight(
                st.session_state["insight"]
            )

            display_insight_cards(insight_sections)

    with st.expander("View generated SQL"):
        st.code(
            sql,
            language="sql",
        )