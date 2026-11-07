import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

div[data-testid="metric-container"] {
    background-color: #1E3A8A;
    border: 1px solid #3B82F6;
    padding: 15px;
    border-radius: 10px;
}

div[data-testid="metric-container"] label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================

session = get_active_session()

# =====================================================
# TITLE
# =====================================================

st.title("🏨 Hotel Booking Analytics Dashboard")

st.markdown("---")

# =====================================================
# FILTERS
# =====================================================

f1, f2, f3, f4 = st.columns(4)

hotel_city_list = session.sql("""
SELECT DISTINCT HOTEL_CITY
FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
ORDER BY HOTEL_CITY
""").to_pandas()["HOTEL_CITY"].tolist()

room_type_list = session.sql("""
SELECT DISTINCT ROOM_TYPE
FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
ORDER BY ROOM_TYPE
""").to_pandas()["ROOM_TYPE"].tolist()

booking_status_list = session.sql("""
SELECT DISTINCT BOOKING_STATUS
FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
ORDER BY BOOKING_STATUS
""").to_pandas()["BOOKING_STATUS"].tolist()

with f1:
    selected_city = st.selectbox(
        "Hotel City",
        ["All"] + hotel_city_list
    )

with f2:
    selected_room = st.selectbox(
        "Room Type",
        ["All"] + room_type_list
    )

with f3:
    selected_status = st.selectbox(
        "Booking Status",
        ["All"] + booking_status_list
    )

with f4:

    start_date = st.date_input(
        "Start Date",
        value=None
    )

    # end_date = st.date_input(
    #     "End Date",
    #     value=None
    # )

# =====================================================
# DYNAMIC FILTER
# =====================================================

where_clause = " WHERE 1=1 "

if selected_city != "All":
    where_clause += f" AND HOTEL_CITY = '{selected_city}' "

if selected_room != "All":
    where_clause += f" AND ROOM_TYPE = '{selected_room}' "

if selected_status != "All":
    where_clause += f" AND BOOKING_STATUS = '{selected_status}' "

if start_date:
    where_clause += f"""
        AND TRY_TO_DATE(CHECK_IN_DATE,'MM/DD/YYYY')
            >= '{start_date}'
    """

# if end_date:
#     where_clause += f"""
#         AND TRY_TO_DATE(CHECK_IN_DATE,'MM/DD/YYYY')
#             <= '{end_date}'
#     """

try:

    # =====================================================
    # KPI SECTION
    # =====================================================

    avg_booking_value = session.sql(f"""
        SELECT AVG(TOTAL_AMOUNT) AS AVG_BOOKING_VALUE
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
    """).collect()[0]["AVG_BOOKING_VALUE"]

    total_guests = session.sql(f"""
        SELECT SUM(NUM_GUESTS) AS TOTAL_GUESTS
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
    """).collect()[0]["TOTAL_GUESTS"]

    total_bookings = session.sql(f"""
        SELECT COUNT(*) AS TOTAL_BOOKINGS
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
    """).collect()[0]["TOTAL_BOOKINGS"]

    total_revenue = session.sql(f"""
        SELECT SUM(TOTAL_AMOUNT) AS TOTAL_REVENUE
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
    """).collect()[0]["TOTAL_REVENUE"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Avg Booking Value",
            f"${float(avg_booking_value or 0):,.2f}"
        )

    with c2:
        st.metric(
            "Total Guests",
            f"{int(total_guests or 0):,}"
        )

    with c3:
        st.metric(
            "Total Bookings",
            f"{int(total_bookings or 0):,}"
        )

    with c4:
        st.metric(
            "Total Revenue",
            f"${float(total_revenue or 0):,.2f}"
        )

    st.markdown("---")

       # =====================================================
    # MONTHLY REVENUE
    # =====================================================

    monthly_revenue = session.sql(f"""
        SELECT
            DATE_TRUNC(
                'MONTH',
                TRY_TO_DATE(CHECK_IN_DATE,'MM/DD/YYYY')
            ) AS MONTH,
            SUM(TOTAL_AMOUNT) AS TOTAL_REVENUE
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        GROUP BY 1
        ORDER BY 1
    """).to_pandas()

    # =====================================================
    # MONTHLY BOOKINGS
    # =====================================================

    monthly_bookings = session.sql(f"""
        SELECT
            DATE_TRUNC(
                'MONTH',
                TRY_TO_DATE(CHECK_IN_DATE,'MM/DD/YYYY')
            ) AS MONTH,
            COUNT(*) AS TOTAL_BOOKINGS
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        GROUP BY 1
        ORDER BY 1
    """).to_pandas()

    # =====================================================
    # TOP CITY REVENUE
    # =====================================================

    top_city_revenue = session.sql(f"""
        SELECT
            HOTEL_CITY,
            SUM(TOTAL_AMOUNT) AS TOTAL_REVENUE
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        GROUP BY HOTEL_CITY
        ORDER BY TOTAL_REVENUE DESC
        LIMIT 5
    """).to_pandas()

    # =====================================================
    # BOOKING STATUS
    # =====================================================

    booking_status = session.sql(f"""
        SELECT
            BOOKING_STATUS,
            COUNT(*) AS TOTAL
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        GROUP BY BOOKING_STATUS
    """).to_pandas()

    # =====================================================
    # ROOM TYPE
    # =====================================================

    room_type = session.sql(f"""
        SELECT
            ROOM_TYPE,
            COUNT(*) AS TOTAL_BOOKINGS
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        GROUP BY ROOM_TYPE
        ORDER BY TOTAL_BOOKINGS DESC
    """).to_pandas()

    # =====================================================
    # CHARTS ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Revenue Trend")

        st.line_chart(
            monthly_revenue,
            x="MONTH",
            y="TOTAL_REVENUE"
        )


    with col2:
        st.subheader("Monthly Booking Trend")

        st.line_chart(
            monthly_bookings,
            x="MONTH",
            y="TOTAL_BOOKINGS"
        )

    # =====================================================
    # CHARTS ROW 2
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Cities by Revenue")

        st.bar_chart(
            top_city_revenue,
            x="HOTEL_CITY",
            y="TOTAL_REVENUE"
        )

    with col2:
        st.subheader("Bookings by Status")

        st.bar_chart(
            booking_status,
            x="BOOKING_STATUS",
            y="TOTAL"
        )

    # =====================================================
    # CHARTS ROW 3
    # =====================================================

    st.subheader("Bookings by Room Type")

    st.bar_chart(
        room_type,
        x="ROOM_TYPE",
        y="TOTAL_BOOKINGS"
    )

    # =====================================================
    # DETAIL GRID
    # =====================================================

    st.markdown("---")

    st.subheader("Booking Details")

    booking_data = session.sql(f"""
        SELECT *
        FROM HOTEL_DATABASE.DEV.GOLD_BOOKING_CLEAN
        {where_clause}
        LIMIT 100
    """).to_pandas()

    st.dataframe(
        booking_data,
        use_container_width=True,
        height=500
    )

except Exception as e:
    st.error(str(e))
