# ============================================================
# FitCom - UI Components
# Author: Anand Kumar
#
# Purpose:
# Centralized reusable UI components to ensure consistency
# across all pages (headers, sections, cards, etc.)
#
# Why this matters:
# - Avoid repeated UI code
# - Maintain consistent look & feel
# - Easier future updates (change once, reflect everywhere)
# ============================================================

import streamlit as st


# ------------------------------------------------------------
# PAGE HEADER
# ------------------------------------------------------------
def page_header(title: str, subtitle: str = ""):
    """
    Renders a clean page title with optional subtitle.

    Usage:
    page_header("Dashboard", "Overview of performance")
    """
    st.markdown(f"<h2 style='margin-bottom:4px;'>{title}</h2>", unsafe_allow_html=True)

    if subtitle:
        st.markdown(
            f"<p style='color:#6c757d; font-size:13px; margin-top:0;'>{subtitle}</p>",
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# SECTION TITLE
# ------------------------------------------------------------
def section(title: str):
    """
    Renders section heading.

    Usage:
    section("Body Composition")
    """
    st.markdown(
        f"<h3 style='margin-bottom:10px;'>{title}</h3>",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CARD WRAPPER (FOR STREAMLIT COMPONENTS)
# ------------------------------------------------------------
def card_start():
    """
    Start a card container.

    Must be paired with card_end()

    Usage:
    card_start()
    st.metric(...)
    card_end()
    """
    st.markdown("<div class='card'>", unsafe_allow_html=True)


def card_end():
    """
    Ends a card container.
    """
    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# SIMPLE CARD (FOR HTML CONTENT ONLY)
# ------------------------------------------------------------
def card(content: str):
    """
    Render a card with HTML content (tables, formatted text).

    Usage:
    card(table_df.to_html(...))
    """
    st.markdown(
        f"""
        <div class='card'>
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# METRIC CARD (COMMON USE CASE)
# ------------------------------------------------------------
def metric_card(label: str, value, delta=None):
    """
    Pre-styled metric inside a card.

    Usage:
    metric_card("BMI", 24.5)
    """
    card_start()
    st.metric(label, value, delta)
    card_end()


# ------------------------------------------------------------
# TWO COLUMN CARD LAYOUT
# ------------------------------------------------------------
def two_column_card(left_content, right_content):
    """
    Creates a two-column layout inside a card.

    Usage:
    two_column_card(lambda: st.write("A"), lambda: st.write("B"))
    """
    card_start()

    col1, col2 = st.columns(2)

    with col1:
        left_content()

    with col2:
        right_content()

    card_end()


# ------------------------------------------------------------
# THREE COLUMN CARD LAYOUT
# ------------------------------------------------------------
def three_column_card(c1, c2, c3):
    """
    Creates a 3-column layout inside a card.

    Usage:
    three_column_card(
        lambda: st.metric("A", 10),
        lambda: st.metric("B", 20),
        lambda: st.metric("C", 30)
    )
    """
    card_start()

    col1, col2, col3 = st.columns(3)

    with col1:
        c1()

    with col2:
        c2()

    with col3:
        c3()

    card_end()


# ------------------------------------------------------------
# DIVIDER (CONSISTENT SPACING)
# ------------------------------------------------------------
def divider():
    """
    Adds consistent spacing divider.
    """
    st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)