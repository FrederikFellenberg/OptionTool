import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Funktionen zum Berechnen der Auszahlung
def calculate_payoff(underlying_price, strike_price, premium, option_type):
    if option_type == "Long Call":
        return np.maximum(underlying_price - strike_price, 0) - premium
    elif option_type == "Short Call":
        return np.minimum(strike_price - underlying_price, 0) + premium
    elif option_type == "Long Put":
        return np.maximum(strike_price - underlying_price, 0) - premium
    elif option_type == "Short Put":
        return np.minimum(underlying_price - strike_price, 0) + premium

# Funktion zur Berechnung der kombinierten Auszahlung
def calculate_combined_payoff(option_amounts, payoffs):
    total_amount = sum(option_amounts)
    if total_amount > 0:
        combined_payoff = sum((amount / total_amount) * payoff for amount, payoff in zip(option_amounts, payoffs))
    else:
        combined_payoff = 0
    return combined_payoff

# Funktion zum Zeichnen des Graphen
def plot_options_graphs(long_call_strike, long_call_premium, long_call_amount,
                         long_put_strike, long_put_premium, long_put_amount,
                         short_call_strike, short_call_premium, short_call_amount,
                         short_put_strike, short_put_premium, short_put_amount,
                         factor_long_call, factor_long_put, factor_short_call, factor_short_put,
                         lower_bound_x, upper_bound_x, lower_bound_y, upper_bound_y):
    underlying_prices = np.linspace(lower_bound_x, upper_bound_x, 1000)

    # Berechnung der Auszahlungen
    long_call_payoff = calculate_payoff(underlying_prices, long_call_strike, long_call_premium, "Long Call") * factor_long_call
    long_put_payoff = calculate_payoff(underlying_prices, long_put_strike, long_put_premium, "Long Put") * factor_long_put
    short_call_payoff = calculate_payoff(underlying_prices, short_call_strike, short_call_premium, "Short Call") * factor_short_call
    short_put_payoff = calculate_payoff(underlying_prices, short_put_strike, short_put_premium, "Short Put") * factor_short_put

    # Combined Payoff berechnen
    combined_payoff = calculate_combined_payoff(
        [long_call_amount, long_put_amount, short_call_amount, short_put_amount],
        [long_call_payoff, long_put_payoff, short_call_payoff, short_put_payoff]
    )

    # Darstellung des Graphen
    plt.figure(figsize=(10, 6))
    plt.plot(underlying_prices, long_call_payoff, label='Long Call', color='blue')
    plt.plot(underlying_prices, long_put_payoff, label='Long Put', color='green')
    plt.plot(underlying_prices, short_call_payoff, label='Short Call', color='red')
    plt.plot(underlying_prices, short_put_payoff, label='Short Put', color='orange')
    plt.plot(underlying_prices, combined_payoff, label='Combined Payoff', color='purple', linestyle='--')

    plt.axhline(0, color='black', linewidth=0.5)
    plt.xlabel('Underlying Price')
    plt.ylabel('Payoff')
    plt.title('Options Payoff Graphs')
    plt.xlim(lower_bound_x, upper_bound_x)
    plt.ylim(lower_bound_y, upper_bound_y)
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Hauptfunktion für die Streamlit-App
def main():
    st.title('Option Tool')

    # Sidebar für Eingaben
    st.sidebar.header('Options Parameters')

    # Eingaben für Long Call
    st.sidebar.subheader("Long Call")
    long_call_strike = st.sidebar.number_input("Strike Price:", min_value=0.0, value=10.0)
    long_call_premium = st.sidebar.number_input("Premium:", min_value=0.0, value=1.0)
    long_call_amount = st.sidebar.number_input("Amount:", min_value=0, value=1, step=1)

    # Eingaben für Short Call
    st.sidebar.subheader("Short Call")
    short_call_strike = st.sidebar.number_input("Strike Price:", min_value=0.0, value=15.0)
    short_call_premium = st.sidebar.number_input("Premium:", min_value=0.0, value=0.5)
    short_call_amount = st.sidebar.number_input("Amount:", min_value=0, value=1, step=1)

    # Eingaben für Long Put
    st.sidebar.subheader("Long Put")
    long_put_strike = st.sidebar.number_input("Strike Price:", min_value=0.0, value=10.0)
    long_put_premium = st.sidebar.number_input("Premium:", min_value=0.0, value=1.0)
    long_put_amount = st.sidebar.number_input("Amount:", min_value=0, value=1, step=1)

    # Eingaben für Short Put
    st.sidebar.subheader("Short Put")
    short_put_strike = st.sidebar.number_input("Strike Price:", min_value=0.0, value=5.0)
    short_put_premium = st.sidebar.number_input("Premium:", min_value=0.0, value=0.5)
    short_put_amount = st.sidebar.number_input("Amount:", min_value=0, value=1, step=1)

    # Erweiterte Einstellungen
    st.sidebar.header('Advanced Settings')
    factor_long_call = st.sidebar.number_input("Factor for Long Call:", value=1.0)
    factor_long_put = st.sidebar.number_input("Factor for Long Put:", value=1.0)
    factor_short_call = st.sidebar.number_input("Factor for Short Call:", value=1.0)
    factor_short_put = st.sidebar.number_input("Factor for Short Put:", value=1.0)

    lower_bound_x = st.sidebar.number_input("Lower Bound X (Abszisse):", value=0.0)
    upper_bound_x = st.sidebar.number_input("Upper Bound X (Abszisse):", value=50.0)
    lower_bound_y = st.sidebar.number_input("Lower Bound Y (Ordinate):", value=-20.0)
    upper_bound_y = st.sidebar.number_input("Upper Bound Y (Ordinate):", value=20.0)

    # Plot der Optionsgraphen
    if st.sidebar.button("Plot Options Graphs"):
        plot_options_graphs(long_call_strike, long_call_premium, long_call_amount,
                             long_put_strike, long_put_premium, long_put_amount,
                             short_call_strike, short_call_premium, short_call_amount,
                             short_put_strike, short_put_premium, short_put_amount,
                             factor_long_call, factor_long_put, factor_short_call, factor_short_put,
                             lower_bound_x, upper_bound_x, lower_bound_y, upper_bound_y)

if __name__ == "__main__":
    main()