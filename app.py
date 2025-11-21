import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------
# Helper Physics Functions
# -----------------------------------

def mosfet_iv(Vg, Vd, tox, mobility, Vth):
    Cox = 3.45e-11 / tox  # F/m^2
    k = mobility * Cox
    if Vg < Vth:
        return 0
    if Vd < (Vg - Vth):
        return k * ((Vg - Vth) * Vd - 0.5 * Vd**2)
    else:
        return 0.5 * k * (Vg - Vth)**2

def dg_threshold(thickness, tox):
    return 0.2 + 0.5 * np.exp(-thickness / (5e-9)) + (tox * 1e9) * 0.01

def cnt_bandgap(n, m):
    d = 0.0783 * np.sqrt(n**2 + m**2 + n*m)
    Eg = 0.82 / d
    return d, Eg

def mobility_degradation(Efield, mu0):
    return mu0 / (1 + (Efield / 1e6))

# -----------------------------------
# Streamlit UI
# -----------------------------------

st.title("IQ-MOS: Interactive Quantum-Aware Multigate MOSFET Simulator")
st.caption("No datasets. No ML. 100% physics-based nanoscale device simulator.")

st.sidebar.header("Select Simulation Mode")
mode = st.sidebar.selectbox("Mode", 
                            ["MOSFET I-V", 
                             "Double Gate MOS Threshold",
                             "CNT Bandgap Explorer",
                             "Mobility Degradation",
                             "Radiation TID Threshold Shift"])

# -----------------------------------
# Mode 1: MOSFET I–V
# -----------------------------------

if mode == "MOSFET I-V":
    st.header("MOSFET I–V Simulator (Single Gate / Rule-Based)")
    
    Vg = st.slider("Gate Voltage Vg (V)", 0.0, 2.0, 1.0)
    tox = st.slider("Oxide Thickness tox (nm)", 0.5, 5.0, 1.5) * 1e-9
    mobility = st.slider("Mobility (cm²/Vs)", 50.0, 500.0, 200.0) * 1e-4
    Vth = st.slider("Threshold Voltage (V)", 0.1, 1.0, 0.4)

    Vd_values = np.linspace(0, 1.5, 200)
    Id_values = [mosfet_iv(Vg, Vd, tox, mobility, Vth) for Vd in Vd_values]

    fig, ax = plt.subplots()
    ax.plot(Vd_values, Id_values)
    ax.set_xlabel("Drain Voltage (V)")
    ax.set_ylabel("Drain Current (A)")
    ax.set_title("MOSFET I-V Characteristics")
    st.pyplot(fig)

# -----------------------------------
# Mode 2: Double Gate Threshold
# -----------------------------------

elif mode == "Double Gate MOS Threshold":
    st.header("Double Gate MOSFET Threshold Voltage Predictor")

    thickness = st.slider("Silicon Body Thickness (nm)", 2.0, 20.0, 10.0) * 1e-9
    tox = st.slider("Oxide Thickness tox (nm)", 0.5, 5.0, 1.0) * 1e-9

    Vth = dg_threshold(thickness, tox)
    st.success(f"Predicted Double Gate MOSFET Vth = {Vth:.3f} V")

# -----------------------------------
# Mode 3: CNT Bandgap
# -----------------------------------

elif mode == "CNT Bandgap Explorer":
    st.header("Carbon Nanotube Bandgap & Diameter Explorer")

    n = st.slider("n index", 1, 30, 10)
    m = st.slider("m index", 1, 30, 10)

    d, Eg = cnt_bandgap(n, m)

    st.write(f"**CNT Diameter**: {d:.3f} nm")
    st.write(f"**Bandgap**: {Eg:.3f} eV")

    if abs((n - m) % 3) == 0:
        st.warning("This CNT is metallic!")
    else:
        st.success("This CNT is semiconducting.")

# -----------------------------------
# Mode 4: Mobility degradation
# -----------------------------------

elif mode == "Mobility Degradation":
    st.header("Mobility vs Electric Field (Velocity Saturation Effect)")
    
    mu0 = st.slider("Low-field mobility (cm²/Vs)", 10.0, 500.0, 300.0) * 1e-4
    E = np.linspace(1e4, 1e7, 200)
    mu = mobility_degradation(E, mu0)

    fig, ax = plt.subplots()
    ax.plot(E, mu)
    ax.set_xlabel("Electric Field (V/m)")
    ax.set_ylabel("Mobility (m²/Vs)")
    ax.set_title("Mobility Degradation Curve")
    st.pyplot(fig)

# -----------------------------------
# Mode 5: Radiation Effects
# -----------------------------------

elif mode == "Radiation TID Threshold Shift":
    st.header("Radiation-Induced Threshold Voltage Shift")

    dose = st.slider("Total Ionizing Dose (krad)", 0.0, 500.0, 50.0)
    shift = 0.001 * dose

    st.write(f"**ΔVth due to radiation** = {shift:.3f} V")

    fig, ax = plt.subplots()
    ax.plot([0, dose], [0, shift])
    ax.set_xlabel("Dose (krad)")
    ax.set_ylabel("Threshold Shift (V)")
    ax.set_title("Radiation-Induced ΔVth")
    st.pyplot(fig)
