import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Caching der Berechnungen
@st.cache_data
def calculate_payoff(underlying_price, strike_price, premium, option_type):
    if option_type == "Long Call":
        return np.maximum(underlying_price - strike_price, 0) - premium
    elif option_type == "Short Call":
        return np.minimum(strike_price - underlying_price, 0) + premium
    elif option_type == "Long Put":
        return np.maximum(strike_price - underlying_price, 0) - premium
    elif option_type == "Short Put":
        return np.minimum(underlying_price - strike_price, 0) + premium
    else:
        return np.zeros_like(underlying_price)

@st.cache_data
def get_underlying_prices(start, stop, num):
    return np.linspace(start, stop, num)

def plot_options_graphs(underlying_prices, payoffs, strike_prices, labels, title, x_bounds, y_bounds, premium_values, amounts):
    plt.figure(figsize=(10, 6))

    plt.xlabel('Underlying Price')
    plt.ylabel('Payoff')
    plt.title(title)
    plt.xlim(*x_bounds)
    plt.ylim(*y_bounds)

    for payoff, label, strike_price, premium, amount in zip(payoffs, labels, strike_prices, premium_values, amounts):
        plt.plot(underlying_prices, payoff, label=label)

        # Berechnung des Payoffs am Strike-Preis für die y-Achse
        strike_payoff = calculate_payoff(strike_price, strike_price, premium, label) * amount

        # Setze die y-Ticks für den Payoff
        if strike_payoff not in plt.yticks()[0]:  # Überprüfe, ob der Tick bereits existiert
            plt.yticks(list(plt.yticks()[0]) + [strike_payoff])

    # Füge die Strike-Preise als zusätzliche x-Ticks hinzu
    unique_strikes = list(set(strike_prices))
    plt.xticks(list(plt.xticks()[0]) + unique_strikes)

    plt.legend()
    plt.grid()
    return plt

# Hauptfunktion für die Streamlit-App
def main():
    st.title('Option Tool')

    # Sidebar für Eingaben
    st.sidebar.header('Option Parameters')

    # Allgemeine Einstellungen
    st.sidebar.subheader("Graph Bounds")
    x_lower = st.sidebar.number_input("Lower X (Underlying Price):", min_value=0.0, value=0.0, step=1.0)
    x_upper = st.sidebar.number_input("Upper X (Underlying Price):", min_value=0.0, value=100.0, step=1.0)
    y_lower = st.sidebar.number_input("Lower Y (Payoff):", value=0.0, step=1.0)
    y_upper = st.sidebar.number_input("Upper Y (Payoff):", value=100.0, step=1.0)

    # Berechnung von Underlying Prices
    underlying_prices = get_underlying_prices(0, x_upper, 1000)

    # Eingaben für verschiedene Optionen
    option_types = ["Long Call", "Short Call", "Long Put", "Short Put", "Asset"]
    payoffs = []
    labels = []
    amounts = []
    strike_prices = []
    premium_values = []

    for option_type in option_types:
        with st.sidebar.expander(f"{option_type} Parameters", expanded=False):
            # Einschaltknopf
            is_enabled = st.checkbox(f"Enable {option_type}", value=False)
            if is_enabled:
                if option_type != "Asset":  # Normale Optionen
                    strike_price = st.number_input(f"{option_type} Strike Price:", min_value=0, value=50, step=1)
                    # Dynamischer Slider für den Strike Price mit Bereich +-50
                    strike_price = st.slider(
                        f"{option_type} Strike Price Range:",
                        min_value=np.maximum(0,strike_price - 50),
                        max_value=strike_price + 50,
                        value=strike_price,
                        step=1
                    )
                    strike_prices.append(strike_price)

                    # Number input für den Premium
                    premium = st.number_input(f"{option_type} Premium:", min_value=0, value=0, step=1)
                    # Dynamischer Slider für den Premium mit Bereich +-50
                    premium = st.slider(
                        f"{option_type} Premium Range:",
                        min_value=np.maximum(0,premium - 50),
                        max_value=premium + 50,
                        value=premium,
                        step=1
                    )
                    premium_values.append(premium)
                    amount = st.number_input(f"{option_type} Amount:", min_value=0.1, value=1.0, step=1.0)

                    payoff = (
                        calculate_payoff(underlying_prices, strike_price, premium, option_type) * amount
                    )

                    payoffs.append(payoff)
                    labels.append(option_type)
                    amounts.append(amount)
                else:
                    amount = st.number_input("Asset Amount:", min_value=0.1, value=1.0, step=1.0)
                    payoff = underlying_prices * amount
                    payoffs.append(payoff)
                    labels.append("Asset")
                    strike_prices.append(0)
                    premium_values.append(0)
                    amounts.append(amount)

    # Kombinierter Payoff nur berechnen, wenn mehr als ein Graph aktiviert ist
    if len(payoffs) > 1:
        combined_payoff = np.sum(payoffs, axis=0)
        payoffs.append(combined_payoff)
        labels.append("Combined Payoff")
        strike_prices.append(0)
        premium_values.append(0)
        amounts.append(1)

    # Dynamische Darstellung
    if payoffs:
        plot = plot_options_graphs(
            underlying_prices, payoffs, strike_prices, labels,
            "Option Payoff Graphs", (x_lower, x_upper), (y_lower, y_upper), premium_values, amounts
        )
        st.pyplot(plot)
    else:
        st.info("Enable at least one option type to visualize the graph.")

if __name__ == "__main__":
    main()
